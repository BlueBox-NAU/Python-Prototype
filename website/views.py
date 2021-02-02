from pyramid.httpexceptions import HTTPFound
from pyramid.response import Response
from pyramid.view import view_config

membersVar = [
    {'id': 1,
    'email': 'jdh553@nau.edu',
    'password': 'abc123'},
    {'id': 2,
    'email': 'zsw23@nau.edu',
    'password': 'password'}
]

@view_config(route_name='home', renderer='index.html')
def home(request):
    return {}

#Actually a sign up
@view_config(route_name='demo1', renderer='demo1/index.html')
def demo1(request):
    if request.method == 'POST':
        for member in membersVar:
            if(request.params['email'] == member['email']):
                print("\nFOUND\n")
                url = request.route_url('demo1')
                return HTTPFound(location=url)
        print("\nNOT FOUND\n")
        url = request.route_url('demo1')
        return HTTPFound(location=url)
    else:
        return{'members': membersVar} # display members in membersVar at bottom of page

# Actually a sign up
@view_config(route_name='register', renderer='demo1/register.html')
def register(request):
    if request.method == 'POST':
        membersVar.append({'id': 99, 
                        'email':request.params['email'],
                        'password':request.params['password']})
        url = request.route_url('demo1')
        return HTTPFound(location=url)
    else:
        return{'members': membersVar} # display members in membersVar at bottom of page
    


# Actually a sign up
# @view_config(route_name='signup', renderer='demo1.html')
# def demo1(request):
#     if request.method == 'POST':
#         print("BEFORE\n==========\n", members, "\n")
#         members.append({'id': 99, 
#                         'email':request.params['email'],
#                         'password':request.params['password']})
#         print("AFTER\n==========\n", members, "\n")
#         return{}
#     else:
#         return{}


