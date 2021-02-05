from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy

config = Configurator()
config.add_route('home', '')

# DEMO 1 Routes
config.add_route('login', '/login/')
config.add_route('logout', '/logout/')
config.add_route('success', '/success/')
config.add_route('register', '/register/')

config.add_route('members', '/members/')
# config.add_route('about', '/about/')
# config.add_route('jbrowse', '/jbrowse/')
# config.add_route('newHub', '/newHub/')
# config.add_route('tutorial', '/tutorial/')
# config.add_static_view(name='tutorial/static', path='website/static/tutorial')
# config.add_route('uploadHubUrl', '/uploadHubUrl/')
# config.add_route('jobs', '/jobs/')
# config.add_route('jobInfo', '/jobs/info/')
# config.add_route('api', '/api/')
# config.add_route('hubInfo', '/{user}/{hub}/info/')
# config.add_route('hubData', '/{user}/{hub}/data/{handler}')
# config.add_route('trackData', '/{user}/{hub}/{track}/{handler}/')
# config.add_static_view(name='/{user}/{hub}', path='jbrowse')
config.include('pyramid_jinja2')
config.add_jinja2_renderer('.html')
config.scan('website.views')

authn_policy = AuthTktAuthenticationPolicy('seekrit', hashalg='sha512')
authz_policy = ACLAuthorizationPolicy()
config.set_authentication_policy(authn_policy)
config.set_authorization_policy(authz_policy)

config.add_view('website.views.success',
                route_name='success',
                context='website.login.models.Member.Member',
                permission='validUser')

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
