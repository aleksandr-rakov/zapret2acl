from pyramid.view import view_config


@view_config(route_name='home', renderer='main.mako')
def my_view(request):
    return {'project': 'zapret2acl'}
