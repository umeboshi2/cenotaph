from pyramid.config import Configurator
from sqlalchemy import engine_from_config
from sqlalchemy.orm import sessionmaker

from .models import (
    DBSession,
    Base,
    )


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession = sessionmaker()
    settings['db.sessionmaker'] = DBSession
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    request_factory = 'cenotaph.request.AlchemyRequest'
    config = Configurator(settings=settings,
                          request_factory=request_factory,)
    config.include('cornice')
    config.include('pyramid_mako')
    serve_static_assets = False
    if 'serve_static_assets' in settings and settings['serve_static_assets'].lower() == 'true':
        serve_static_assets = True
    if serve_static_assets:
        print "Serving static assets from pyramid.", serve_static_assets
        config.add_static_view(name='client',
                               path=settings['static_assets_path'])

    config.add_static_view(name='images',
                           path='/freespace/urlrepos')
    config.add_route('home', '/')
    config.add_view('cenotaph.views.client.ClientView',
                    route_name='home',)
    config.add_route('main_calendar', '/calendar/{caltype}')
    config.add_view('cenotaph.views.main.MainCalendarViewer',
                    route_name='main_calendar',
                    renderer='json',)
    
    config.scan()
    return config.make_wsgi_app()
