# -*- coding: utf8 -*-
from optparse import OptionParser
from pyquery import PyQuery as pq
import telnetlib

def before_hook(options):
    yield "no access list %s"%options.acl

acl_template="access-list %s deny ip any host %s"

def after_hook(options):
    yield "wr"

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

    doc=pq(filename=options.filename)
    
    new_acl=[acl_template%(options.acl,x.text) for x in doc('ip')]
    
    telnet  = telnetlib.Telnet(options.cisco)
    if options.user: 
        telnet.read_until('Username: ', 3) 
        telnet.write(options.user + '\r')
    if options.password:
        telnet.read_until('Password: ', 3)  
        telnet.write(options.password + '\r') 

    for block in [before_hook(options),new_acl,after_hook(options)]:
        for line in block:
            telnet.write(line + '\r')
    telnet.write('exit' + '\r')
    print telnet.read_all()
