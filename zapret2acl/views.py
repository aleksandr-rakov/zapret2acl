from pyramid.view import view_config
from pyramid.httpexceptions import HTTPTemporaryRedirect
from .console import parse_data,send_acl

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

    try:
        new_acl=parse_data(data,request.POST.get('acl'))
    except:
        status='Error parsing data'

    try:
        status = send_acl(new_acl,request.POST.get('cisco'),request.POST.get('options.user'),request.POST.get('options.password')
    except:
        status='Error sending acl to cisco'

    return HTTPTemporaryRedirect(request.route_url('dash',_query={'status':status}))
