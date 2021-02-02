from pyramid.httpexceptions import HTTPFound
from pyramid.response import Response
from pyramid.view import view_config


@view_config(route_name='home', renderer='index.html')
def home(request):
    return {}

@view_config(route_name='demo1', renderer='demo1.html')
def demo1(request):
    return {}