from pyramid.config import Configurator
from sqlalchemy import engine_from_config
from sqlalchemy.orm import sessionmaker

#from trumpet.security import make_authn_authz_policies


from cenotaph.models.base import DBSession, Base
from cenotaph.models.usergroup import User

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
    request_factory = 'trumpet.request.AlchemyRequest'
    config = Configurator(settings=settings,
                          request_factory=request_factory,)
    config.include('cornice')
    config.include('pyramid_beaker')
    #config.add_static_view('static', 'static', cache_max_age=3600)
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

        for asset in ['stylesheets', 'javascripts', 'images',
                     'components', 'coffee']:
            print "Adding asset", asset
            config.add_static_view(name=asset,
                                   path=settings['static.%s' % asset])

    #config.scan()
    config.scan('cenotaph.views.currentuser')
    return config.make_wsgi_app()
