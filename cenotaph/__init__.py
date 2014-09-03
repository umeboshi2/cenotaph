from pyramid.config import Configurator
from sqlalchemy import engine_from_config

from cenotaph.models.base import DBSession, Base

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    settings['db.sessionmaker'] = DBSession
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    Base.metadata.create_all(engine)
    request_factory = 'trumpet.request.AlchemyRequest'
    config = Configurator(settings=settings,
                          request_factory=request_factory,)
    config.include('cornice')
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_view('cenotaph.views.client.ClientView',
                    route_name='home',)
    config.add_route('apps', '/app/{appname}')
    config.add_view('cenotaph.views.client.ClientView',
                    route_name='apps',)

    # static assets
    serve_static_assets = False
    if 'serve_static_assets' in settings and settings['serve_static_assets'].lower() == 'true':
        serve_static_assets = True
    if serve_static_assets:
        print "Serving static assets from pyramid.", serve_static_assets
        config.add_static_view(name='client',
                               path=settings['static_assets_path'])

    
    #config.scan()
    return config.make_wsgi_app()
