from pyramid.config import Configurator
from sqlalchemy import engine_from_config
from sqlalchemy.orm import sessionmaker


from trumpet.security import authn_policy, authz_policy
from trumpet.config import add_static_views

#from cenotaph.models.base import DBSession, Base
from trumpet.models.base import DBSession, Base
from trumpet.models.usergroup import User

import cenotaph.models.sitecontent

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    settings['db.sessionmaker'] = DBSession
    settings['db.usermodel'] = User
    settings['db.usernamefield'] = 'username'
    
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    Base.metadata.create_all(engine)
    root_factory = 'trumpet.resources.RootGroupFactory'
    request_factory = 'trumpet.request.AlchemyRequest'
    config = Configurator(settings=settings,
                          root_factory=root_factory,
                          request_factory=request_factory,
                          authentication_policy=authn_policy,
                          authorization_policy=authz_policy)
    config.include('cornice')
    config.include('pyramid_beaker')
    #config.add_static_view('static', 'static', cache_max_age=3600)
    client_view = 'cenotaph.views.client.ClientView'
    config.add_route('home', '/')
    config.add_route('apps', '/app/{appname}')
    config.add_view(client_view, route_name='home')
    config.add_view(client_view, route_name='apps')
    config.add_view(client_view, name='login')
    config.add_view(client_view, name='logout')
    # FIXME - get client view to understand it hit forbidden
    config.add_view('cenotaph.views.client.forbidden_view',
                    context='pyramid.httpexceptions.HTTPForbidden')
    config.add_view(client_view, name='admin', permission='admin')
    # static assets
    serve_static_assets = False
    if 'serve_static_assets' in settings and settings['serve_static_assets'].lower() == 'true':
        serve_static_assets = True

    if serve_static_assets:
        add_static_views(config, settings)
        
    config.scan('cenotaph.views.currentuser')
    config.scan('cenotaph.views.useradmin')
    config.scan('cenotaph.views.sitetext')
    return config.make_wsgi_app()
