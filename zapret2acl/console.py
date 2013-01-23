# -*- coding: utf8 -*-
from optparse import OptionParser
from pyquery import PyQuery as pq
import telnetlib

def before_hook():
    yield "no access list %s"%options.acl

acl_template="access-list %s deny ip any host %s"

def after_hook():
    yield "wr"

def parse_data(data,acl):
    doc=pq(data)
    yield before_hook()
    for x in doc('ip'):
        yield acl_template%(acl,x.text)
    yield after_hook()

def send_acl(acl,host,user=None,password=None):
    telnet  = telnetlib.Telnet(host)
    if user: 
        telnet.read_until('Username: ', 3) 
        telnet.write(user + '\r')
    if password:
        telnet.read_until('Password: ', 3)  
        telnet.write(password + '\r') 

    for line in acl:
        telnet.write(line + '\r')
    telnet.write('exit' + '\r')
    return telnet.read_all()
    
def main():
    parser = OptionParser()
    parser.add_option("-f", "--file", dest="filename",
                      help="read data from FILE", metavar="FILE")
    parser.add_option("-a", "--acl", dest="acl",
                      help="acl number", metavar="ACL")
    parser.add_option("-c", "--cisco", dest="cisco",
                      help="connect to CISCO", metavar="CISCO")
    parser.add_option("-u", "--user", dest="user",
                      help="Username", metavar="USER")
    parser.add_option("-p", "--password", dest="password",
                      help="Password", metavar="PASSWORD")
    (options, args) = parser.parse_args()

    for x in ['filename','acl','cisco']:
        if not getattr(options,x):
            parser.print_help()
            exit()

    fd=open(options.filename)
    data=fd.read()
    fd.close()

    new_acl=parse_data(data,acl)

    send_acl(new_acl,options.cisco,options.user,options.password)
