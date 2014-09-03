from pyramid.renderers import render
from pyramid.response import Response

from trumpet.views.base import BaseUserViewCallable
from trumpet.models.usergroup import User

class ClientView(BaseUserViewCallable):
    def __init__(self, request):
        self.usermodel = User
        super(ClientView, self).__init__(request)
        if self.request.matched_route.name == 'home':
            self.get_main()
        elif self.request.matched_route.name == 'apps':
            self.get_main(appname=self.request.matchdict['appname'])

    def get_main(self, appname=None):
        template = 'cenotaph:templates/mainview.mako'
        settings = self.get_app_settings()
        basecolor = settings.get('default.css.basecolor', 'BlanchedAlmond')
        csspath = settings.get('default.css.path', '/client/stylesheets')
        jspath = settings.get('default.js.path', '/client/javascripts')
        requirejs = settings.get('default.js.requirejs')
        if appname is None:
            appname = settings.get('default.js.mainapp', 'frontdoor')
        env = dict(appname=appname,
                   basecolor=basecolor,
                   csspath=csspath,
                   jspath=jspath,
                   requirejs=requirejs)
        content = render(template, env)
        self.response = Response(body=content)
        self.response.encode_content()
        
    

