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

def extract_domain(uri):
    parsed_uri = urlparse(uri)
    domain=parsed_uri.netloc
    if parsed_uri.port:
        domain=domain[:-(len(str(parsed_uri.port))+1)]
    return domain

def load_white_list(options):
    if options.get('white_list_path'):
        return [x.strip().encode('utf8') for x in open(options['white_list_path']).readlines()]
    return []

def parse_dns_data(data,options):

    white_list=load_white_list(options)

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

    for x in doc('content'):
        el=pq(x)
        et=el.attr('blockType')
        if et in ('domain','domain-mask'):
            for x in el('domain'):
                domain=x.text
                if domain in white_list:
                    continue
                if domain in found:
                    continue
                found[domain]=1
                yield "%s CNAME .\n"%domain

        elif et in ('default',None):
            for x in el('url'):
                domain=extract_domain(x.text)
                if is_ip(domain):
                    continue
                if domain in white_list:
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

    white_list=load_white_list(options)

    doc=pq(data)

    yield "no access-list %s"%acl

    found={}
    for x in doc('content'):
        el=pq(x)
        et=el.attr('blockType')
        if et in ('default','ip',None):
            if et in ('default',None):
                url_found=False
                ip_found=False
                for x in el('url'):
                    url_found=True
                    domain=extract_domain(x.text)
                    if is_ip(domain):
                        ip_found=True

                if url_found and not ip_found:
                    continue

            for x in el('ip'):
                if x.text in white_list:
                    continue
                if x.text in found:
                    continue
                found[x.text]=True
                yield "access-list %s deny ip any host %s"%(acl, x.text)
            for x in el('ipSubnet'):
                if x.text in white_list:
                    continue
                if x.text in found:
                    continue
                ip=ipaddr.ip_network(x.text)
                net=str(ip.ip)
                wildcard=str(ip.hostmask)
                found[x.text]=True
                yield "access-list %s deny ip any %s %s"%(acl, net, wildcard)

    yield "access-list %s permit ip any any"%acl


def send_line(session,line):
    session.write(line.encode('utf-8')+'\r') 

def send_lines(session,lines):
    session.write('\r'.join(lines).encode('utf-8')+'\r') 

def send_acl(acl_data,options):
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

    try:
        acl=int(getOption(options,'acl'))
    except:
        raise Exception('acl mast be int')
    interfaces=get_interfaces(options)
    if interfaces:
        for interface in interfaces:
            yield "interface %s"%interface
            yield "no ip access-group %s out"%acl
        yield "exit"

    buf=[]
    for line in acl_data:
        buf.append(line)

        if len(buf)>100:
            send_lines(telnet,buf)
            buf=[]
            yield "loading... "

    if buf:
        send_lines(telnet,buf)
        yield "loading... "

    if interfaces:
        for interface in interfaces:
            yield "interface %s"%interface
            yield "ip access-group %s out"%acl
        yield "exit"

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
    parser.add_option("-w", "--white_list", dest="white_list",
                      help="Whitelist", metavar="WHITELIST")
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
