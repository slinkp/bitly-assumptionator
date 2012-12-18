from pyramid.view import view_config
import bitly_api

api_root = 'https://api-ssl.bitly.com/v3/'


@view_config(route_name='home', renderer='templates/index.pt')
def my_view(request):
    data = bitly_api.fetch(api_root + 'user/info')
    return {'project': 'assumptionator', 'bitly': data}
