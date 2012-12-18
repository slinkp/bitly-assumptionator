from pyramid.view import view_config
import bitly_api
import logging
import requests
import urlparse

api_root = 'https://api-ssl.bitly.com/v3/'

THUMBNAIL_SIZE = 140


@view_config(route_name='home', renderer='templates/index.pt')
def my_view(request):
    data = bitly_api.fetch(api_root + 'user/info')
    return {'project': 'assumptionator', 'bitly': data}


@view_config(route_name='link_info', renderer='json')
def link_info(request):
    urls = request.GET.getall('shortUrl')
    params = {'shortUrl': urls}
    data = bitly_api.fetch(api_root + 'info', params=params)['data']['info']
    # TODO: fewer API calls?
    for info in data:
        short_url = info['short_url']
        # For now, clicks for all time.
        clicks = bitly_api.fetch(api_root + 'link/clicks', params={'link': short_url})
        info['clicks'] = clicks['data']['link_clicks']
        # Get long URL and hostname.
        try:
            expanded = bitly_api.fetch(api_root + 'expand', params={'shortUrl': short_url})
            long_url = expanded['data']['expand'][0]['long_url']
            info['long_url'] = long_url
            parsed = urlparse.urlparse(long_url)
            info['domain'] = parsed.hostname or ''
        except (requests.HTTPError, KeyError, IndexError):
            logging.exception("Error fetching long url for %r" % short_url)
            info['domain'] = ''
            info['long_url'] = ''
        # Get embedly preview thumbnail.
        info['preview'] = ''
        try:
            preview = bitly_api.fetch(api_root + 'link/preview',
                                      params={'link': short_url,
                                              'thumbnail_width': THUMBNAIL_SIZE,
                                              'thumbnail_height': THUMBNAIL_SIZE})
            info['preview'] = preview['data']['images'][0]['thumbnail_url']
        except (requests.HTTPError, KeyError):
            logging.exception("Error fetching embedly preview for %r" % short_url)

    return {'data': data}
