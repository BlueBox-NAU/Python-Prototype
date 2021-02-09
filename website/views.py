from pyramid.httpexceptions import HTTPFound, HTTPForbidden
from pyramid.response import Response
from pyramid.view import forbidden_view_config, view_config
from pyramid.security import remember, forget

# TEMP - Variable to contain members to act as our database
from website.models import members
from website.models import USERS

from website.login.models.Hub import Hub
from website.login.models.Member import Member

# Handles home page rendering
@view_config(route_name='home', renderer='index.html')
def home(request):
    return {}

@forbidden_view_config()
def forbidden_view(request):
    # do not allow a user to login if they are already logged in
    if request.authenticated_userid is not None:
        return HTTPForbidden()

    url = request.route_url('login', _query=(('next', request.path),))
    return HTTPFound(location=url)

# SIGN IN -- Handles /login/ and attemp sign in
@view_config(route_name='login', renderer='login/index.html')
def loginPage(request):
    return {'users':USERS}

@view_config(route_name='login', request_method='POST')
def login(request):
    login = request.params.get('email', '')
    passwd = request.POST.get('passwd', '')

    print(USERS)
    user = USERS.get(login, None)
    print(user)
    if user:
        print("\nFOUND\n")
        headers = remember(request, login)
        url = request.route_url('user')
        return HTTPFound(location=url, headers=headers)      
    # for member in members:
    #     if(useremail == member['email']):
    #         print("\nFOUND\n")
    #         url = request.route_url('success')
    #         return HTTPFound(location=url)
    print("\nNOT FOUND\n")
    url = request.route_url('login')
    return HTTPFound(location=url)

@view_config(route_name='logout', request_method='POST')
def logout(request):
    headers = forget(request)
    url = request.route_url('login')
    return HTTPFound(location=url)

@view_config(route_name='user', renderer='login/user.html')
def userPage(request):
    user = request.context
    return {'users':USERS,
            'User': user}

@view_config(route_name='user', request_method='POST')
def user(request):
    url = request.route_url('login')
    return HTTPFound(location=url)


# CREATE ACCOUNT -- Handles /register/ and create account form data
@view_config(route_name='register', renderer='login/register.html')
def registerPage(request):
    return{'users': USERS} # display members in membersVar at bottom of page

@view_config(route_name='register', request_method='POST')
def register(request):
    members.append({'id': 99, 
                    'email':request.params['email'],
                    'password':request.params['password']})
    url = request.route_url('login')
    return HTTPFound(location=url)

# USER AUTHENTICATION
