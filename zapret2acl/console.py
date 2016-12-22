# -*- coding: utf8 -*-
from optparse import OptionParser
from pyquery import PyQuery as pq
import telnetlib
import ipaddr
from pyramid.settings import aslist
from urlparse import urlparse

def getOption(config,option):
    if hasattr(config,'__getitem__'):
        return config.get(option,'')
    else:
        return config.__dict__.get(option,'')

def get_interfaces(options):
    interfaces=None
    interfaces_str=options.get('interfaces')
    if interfaces_str:
        interfaces = aslist(interfaces_str,False)
    return interfaces

def is_ip(str):
    parts=str.split('.')
    if len(parts)==4:
        for x in parts:
            if not x.isdigit():
                return False
        return True
    return False

def parse_dns_data(data):

    found={}
    
    doc=pq(data)

    yield """;RPZ
$TTL 10
@      IN SOA rpz.zone. rpz.zone. (
       5;
       3600;
       300;
       86400;
       60 )
       IN      NS      localhost.
    
"""

    for x in doc('domain'):
        domain=x.text
        if domain in found:
            continue
        found[domain]=1
        yield "%s CNAME .\n"%domain

    for x in doc('url'):
        parsed_uri = urlparse(x.text)
        domain=parsed_uri.netloc
        if parsed_uri.port:
            domain=domain[:-(len(str(parsed_uri.port))+1)]
        if is_ip(domain):
            continue
        if domain in found:
            continue
        found[domain]=1
        yield "%s CNAME .\n"%domain

    yield "\n"


def parse_data(data,options):
    try:
        acl=int(getOption(options,'acl'))
    except:
        raise Exception('acl mast be int')
    interfaces=get_interfaces(options)

    doc=pq(data)

    if interfaces:
        for interface in interfaces:
            yield "interface %s"%interface
            yield "no ip access-group %s out"%acl
        yield "exit"

    yield "no access-list %s"%acl
    for x in doc('ip'):
        yield "access-list %s deny ip any host %s"%(acl, x.text)
    for x in doc('ipSubnet'):
        ip=ipaddr.ip_network(x)
        net=str(ip.ip)
        wildcard=str(ip.hostmask)
        yield "access-list %s deny ip any %s %s"%(acl, net, wildcard)
    yield "access-list %s permit ip any any"%acl

    if interfaces:
        for interface in interfaces:
            yield "interface %s"%interface
            yield "ip access-group %s out"%acl
        yield "exit"

def send_line(session,line):
    session.write(line.encode('utf-8')+'\r') 

def send_acl(acl,options):
    user=getOption(options,'user')
    password=getOption(options,'password')
    host=getOption(options,'cisco')

    if not host:
        raise Exception('Please enter a host')
    telnet  = telnetlib.Telnet(host)
    if user: 
        telnet.read_until('Username: ', 3) 
        send_line(telnet,user)
    if password:
        telnet.read_until('Password: ', 3)  
        send_line(telnet,password)

    send_line(telnet,'ena')# to-do: add enable password
    send_line(telnet,'conf t')

    for line in acl:
        send_line(telnet,line)
        yield "loading... "
    send_line(telnet,'end')

    #send_line(telnet,'wr')
    send_line(telnet,'exit')
    yield telnet.read_all()

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

    new_acl=parse_data(data,options)
    send_acl(new_acl,options)
