from pyramid.renderers import render
from pyramid.response import Response

from pyramid.httpexceptions import HTTPNotFound
from pyramid.httpexceptions import HTTPFound

from pyramid.security import remember, forget

from trumpet.views.base import BaseUserViewCallable

from cenotaph.models.usergroup import User
from cenotaph.views.util import check_login_form

def make_page(appname, settings):
    template = 'cenotaph:templates/mainview.mako'
    basecolor = settings.get('default.css.basecolor', 'BlanchedAlmond')
    csspath = settings.get('default.css.path', '/client/stylesheets')
    jspath = settings.get('default.js.path', '/client/javascripts')
    requirejs = settings.get('default.js.requirejs')
    env = dict(appname=appname,
               basecolor=basecolor,
               csspath=csspath,
               jspath=jspath,
               requirejs=requirejs)
    return render(template, env)
    
class ClientView(BaseUserViewCallable):
    def __init__(self, request):
        self.usermodel = User
        super(ClientView, self).__init__(request)
        if request.method == 'POST':
            self.handle_post()
        else:
            self.handle_get()

    def handle_get(self):
        request = self.request
        view = request.view_name
        subpath = request.subpath
        if not view:
            route = request.matched_route.name
            if route == 'home':
                self.get_main()
                return
            elif route == 'apps':
                self.get_main(appname=request.matchdict['appname'])
                return
            else:
                raise HTTPNotFound, "no such animal"
        elif view in ['login', 'logout']:
            if view == 'logout':
                return self.handle_logout()
            
        
    def get_main(self, appname=None):
        settings = self.get_app_settings()
        if appname is None:
            appname = settings.get('default.js.mainapp', 'frontdoor')
        content = make_page(appname, settings)
        self.response = Response(body=content)
        self.response.encode_content()
        
    def handle_login(self, post):
        if check_login_form(self.request):
            username = post['username']
            headers = remember(self.request, username)
        self.response = HTTPFound('/')


    def handle_logout(self):
        headers = forget(self.request)
        if 'user' in self.request.session:
            del self.request.session['user']
        while self.request.session.keys():
            key = self.request.session.keys()[0]
            del  self.request.session[key]
        location = self.request.route_url('home')
        self.response = HTTPFound(location=location, headers=headers)

    def handle_post(self):
        request = self.request
        view = request.view_name
        post = request.POST
        if view == 'login':
            return self.handle_login(post)
        elif view == 'logout':
            return self.handle_logout()
        else:
            raise HTTPNotFound, 'nope'
        
        
        

