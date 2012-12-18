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
    for info in data:
        # TODO: fewer API calls?
        # For now, clicks for all time.
        short_url = info['short_url']
        clicks = bitly_api.fetch(api_root + 'link/clicks', params={'link': short_url})
        info['clicks'] = clicks['data']['link_clicks']
        try:
            expanded = bitly_api.fetch(api_root + 'expand', params={'shortUrl': short_url})
            parsed = urlparse.urlparse(expanded['data']['expand'][0]['long_url'])
            info['domain'] = parsed.hostname or ''
        except (requests.HTTPError, KeyError, IndexError):
            logging.exception("Error fetching long url for %r" % short_url)
            info['domain'] = ''
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
