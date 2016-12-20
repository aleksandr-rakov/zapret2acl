# -*- coding: utf8 -*-
from pyramid.view import view_config
from .console import parse_data,send_acl
from pyramid.response import Response

def _view_streamed(iterator):
    headers = [('Content-Type', 'text/plain'),
               ('Cache-Control', 'no-cache')]
    response = Response(headerlist=headers)
    response.app_iter = iterator
    return response

@view_config(route_name='home', renderer='main.mako')
def home_view(request):
    status=''
    error=''

    show_params= request.registry.settings.get('show_params_in_form')!='false'

    if request.method=='POST':
        try:
            input_file = request.POST['file'].file
            input_file.seek(0)
            data=input_file.read()
            input_file.close()
        except Exception,error:
            status='Error reading file'

        if show_params:
            options=request.POST
        else:
            options=request.registry.settings

        if not status:
            try:
                new_acl=parse_data(data,options)
            except Exception,error:
               status='Error parsing data'

        if not status:
            try:
                return _view_streamed(send_acl(new_acl,options))
            except Exception,error:
                status='Error sending acl to cisco'

    return {'request': request,'status':status,'show_params':show_params,'error':error}
