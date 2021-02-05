from pyramid.httpexceptions import HTTPFound
from pyramid.response import Response
from pyramid.view import view_config
from pyramid.security import remember

# TEMP - Variable to contain members to act as our database
from website.models import members


# Handles home page rendering
@view_config(route_name='home', renderer='index.html')
def home(request):
    return {}


# SIGN IN -- Handles /login/ and attemp sign in
@view_config(route_name='login', renderer='login/index.html')
def loginPage(request):
    return {'members':members}

@view_config(route_name='login', request_method='POST')
def login(request):
    for member in members:
        if(request.params['email'] == member['email']):
            print("\nFOUND\n")
            url = request.route_url('success')
            return HTTPFound(location=url)
    print("\nNOT FOUND\n")
    url = request.route_url('login')
    return HTTPFound(location=url)

@view_config(route_name='success', renderer='login/success.html', permission='validUser')
def successPage(request):
    return {'members':members}

@view_config(route_name='success', request_method='POST')
def success(request):
    url = request.route_url('login')
    return HTTPFound(location=url)


# CREATE ACCOUNT -- Handles /register/ and create account form data
@view_config(route_name='register', renderer='login/register.html')
def registerPage(request):
    return{'members': members} # display members in membersVar at bottom of page

@view_config(route_name='register', request_method='POST')
def register(request):
    members.append({'id': 99, 
                    'email':request.params['email'],
                    'password':request.params['password']})
    url = request.route_url('login')
    return HTTPFound(location=url)
# USER AUTHENTICATION
