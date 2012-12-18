from pyramid.view import view_config
import bitly_api


api_root = 'https://api-ssl.bitly.com/v3/'


@view_config(route_name='home', renderer='templates/index.pt')
def my_view(request):
    data = bitly_api.fetch(api_root + 'user/info')
    return {'project': 'assumptionator', 'bitly': data}


@view_config(route_name='link_info', renderer='json')
def link_info(request):
    urls = request.GET.getall('shortUrl')
    params = {'shortUrl': urls}
    data = bitly_api.fetch(api_root + 'info', params=params)['data']
    for info in data['info']:
        # For now, clicks for all time.
        clicks = bitly_api.fetch(api_root + 'link/clicks', params={'link': info['short_url']})
        info['clicks'] = clicks['data']['link_clicks']
    return {'data': data}

