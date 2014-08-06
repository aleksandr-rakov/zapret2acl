# -*- coding: utf8 -*-
import os
import subprocess
from mako.template import Template
from datetime import datetime
from suds.client import Client
import base64

################# Отредактируйте эти параметры #################################
openssl='/path/to/openssl/bin/openssl'
key = '/path/to/sertificate/p12.pem'
operatorName =u"Название оператора"
inn=u"1231231231"
ogrn=u"1231231231231"
email=u"test@mail.ru"
store_files_to=''
################################################################################

template="""<?xml version="1.0" encoding="windows-1251"?>
<request>
<requestTime>${requestTime}</requestTime>
<operatorName>${operatorName}</operatorName>
<inn>${inn}</inn>
<ogrn>${ogrn}</ogrn>
<email>${email}</email>
</request>"""
cmd = '%s smime -sign -binary -signer %s -outform DER' % (openssl,key)
WSDL = 'http://www.zapret-info.gov.ru/services/OperatorRequest/?wsdl'

def create_request():
    requestTime=datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%f+00:00")
    request_str=Template(template,input_encoding='utf-8',output_encoding='cp1251').render(requestTime=requestTime,operatorName=operatorName,inn=inn,ogrn=ogrn,email=email)
    return request_str

def sign_request(request_str):
    p = subprocess.Popen(cmd,
                         stdin = subprocess.PIPE,
                         stdout=subprocess.PIPE,
                         shell=True)
    return p.communicate(input=request_str)[0]

def get_LastDumpDate():
    client = Client(WSDL)
    result = client.service.getLastDumpDate()
    return result

def send_request(req,req_signed):
    client = Client(WSDL)
    result = client.service.sendRequest(
        base64.standard_b64encode(req),
        base64.standard_b64encode(req_signed),
        '2.0' #use 2.0 version format
    )
    return result

def request_status(result):
    if result['result']:
        return result['code']
    return False

def get_result(request_id):
    client = Client(WSDL)
    result = client.service.getResult(request_id)
    return result

def result_status(result):
    if result['result']:
        return True
    return False

def decode_result(result):
    return base64.standard_b64decode(result['registerZipArchive'])

def store_file(result,prefix=store_files_to):
    filename=datetime.now().strftime("%Y-%m-%d_%H:%M:%S")+'.zip'
    f=open(prefix+filename,'w')
    f.write(decode_result(result))
    f.close()
