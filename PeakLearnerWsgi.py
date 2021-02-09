from wsgiref.simple_server import make_server
from pyramid.config import Configurator

from pyramid.security import ALL_PERMISSIONS
from pyramid.security import Allow
from pyramid.security import Authenticated
from pyramid.security import Everyone
from pyramid.security import forget
from pyramid.security import remember

from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy

from waitress import serve

from website.login.models.Hub import Hub
from website.login.models.Member import Member

from website.models import USERS

### INITIALIZE MODEL
HUBS = {}

def _create_user(login, **kw):
    kw.setdefault('password', login)
    USERS[login] = Member(login, **kw)
    return USERS[login]

_create_user('zsw23@nau.edu')
_create_user('editor', groups=['editor'])
_create_user('admin', groups=['admin'])

class RootFactory(object):
    __acl__ = [
        (Allow, 'g:admin', ALL_PERMISSIONS),
    ]

    def __init__(self, request):
        self.request = request

class MemberFactory(object):
    __acl__ = [
        (Allow, 'g:admin', ALL_PERMISSIONS),
    ]

    def __init__(self, request):
        self.request = request

    def __getitem__(self, key):
        member = USERS[key]
        member.__parent__ = self
        member.__name__ = key
        return member

def groupfinder(userid, request):
    user = USERS.get(userid)
    if user:
        return ['g:%s' % g for g in user.groups]



config = Configurator()
config.add_route('home', '')

# DEMO 1 Routes
config.add_route('login', '/login/')
config.add_route('logout', '/logout/')
#config.add_route('user', '/user/')
config.add_route('register', '/register/')

config.add_route('user', '/user/{login}', factory=MemberFactory,
                     traverse='/{login}')

config.add_route('members', '/members/')
config.include('pyramid_jinja2')
config.add_jinja2_renderer('.html')
config.scan('website.views')

authn_policy = AuthTktAuthenticationPolicy('seekrit', callback=groupfinder)
authz_policy = ACLAuthorizationPolicy()

config.set_authentication_policy(authn_policy)
config.set_authorization_policy(authz_policy)
config.set_root_factory(RootFactory)

config.add_view('website.views.user',
                route_name='user',
                context='website.login.models.Member.Member',
                permission='view')

# config.scan('api.views')
app = config.make_wsgi_app()

http_server = None


def startServer():
    global http_server
    http_server = make_server('0.0.0.0', 5500, app)
    http_server.serve_forever()


def shutdownServer():
    print('Shutting down PeakLearner')
    if http_server is not None:
        http_server.shutdown()
