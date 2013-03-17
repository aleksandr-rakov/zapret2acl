# -*- coding: utf8 -*-
from gevent import monkey
monkey.patch_all()
import gevent
import service

last_update=None
need_send_request=False
last_request_code=''

def live_forever(func):
    """декоратор для автоперезапуска гринлетов"""
    def wrapper():
        sleep=30
        while True:
            try:
                return func()
            except Exception,e:
                print "Exception %s in bg grenlet: %s\n \
                    Greenlet target will be relaunched after %s seconds"%(e,repr(func),sleep)
                gevent.sleep(sleep)
    return wrapper

@live_forever
def check_updates():
    global last_update
    global need_send_request
    sleep=60*60
    while True:
        print "Checking registry updates"
        tmp = service.get_LastDumpDate()
        if tmp and (last_update==None or tmp>last_update):
            need_send_request=True
            last_update=tmp
            print "Last update=%s"%last_update
        gevent.sleep(sleep)

@live_forever
def send_request():
    global need_send_request
    global last_request_code
    sleep=2*60
    while True:
        if need_send_request:
            print "Sending request"
            request=service.create_request()
            request_signed=service.sign_request(request)
            result=service.send_request(request,request_signed)
            code=service.request_status(result)
            if code:
                print "request sent"
                need_send_request=False
                last_request_code=code
        gevent.sleep(sleep)

@live_forever
def get_result():
    global last_request_code
    sleep=2*60
    while True:
        if last_request_code:
            print "getting result"
            result=service.get_result(last_request_code)
            if service.result_status(result):
                print "stornig result"
                last_request_code=''
                service.store_file(result)
        gevent.sleep(sleep)

if __name__ == '__main__':
    g1 = gevent.spawn(check_updates)
    g2 = gevent.spawn(send_request)
    g3 = gevent.spawn(get_result)
       
    gevent.joinall([g1,g2,g3])
