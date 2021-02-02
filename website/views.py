from pyramid.httpexceptions import HTTPFound
from pyramid.response import Response
from pyramid.view import view_config


@view_config(route_name='home', renderer='index.html')
def home(request):
    return {}

@view_config(route_name='testroute', renderer='test.html')
def test(request):
    query = request.matchdict
    print("Query = ", query)
    print("Query type = ", type(query))
    if request.method == 'GET':
        print("Using Get request...")
        return query
    if request.method == 'POST':
        print("Testing Post Method...")
        print(type(request.json_body))
        print(request.json_body)
        return request.json_body