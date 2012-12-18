from pyramid.config import Configurator
import pyramid.renderers


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('link_info', '/link_info')
    config.add_renderer('json', pyramid.renderers.JSON())
    config.scan()
    return config.make_wsgi_app()
