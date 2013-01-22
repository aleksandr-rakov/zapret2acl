from pyramid.view import view_config
from pyramid.httpexceptions import HTTPTemporaryRedirect

@view_config(route_name='dash', renderer='main.mako')
def dash_view(request):
    status=request.params.get('status')
    return {'request': request,'status':status}

@view_config(route_name='form',request_method='POST')
def form_view(request):
    status=''
    
    try:
        input_file = request.POST['file'].file
        input_file.seek(0)
        data=input_file.read()
        input_file.close()
    except:
        status='Error reading file'

    return HTTPTemporaryRedirect(request.route_url('dash',_query={'status':status}))
