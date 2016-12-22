#!/bin/bash

SERVER=$1
PORT=$2
FNAME=$3

scp -P $PORT $FNAME $SERVER:/home/doggy/dns

ssh -p $PORT $SERVER "sudo cp /home/doggy/dns /etc/bind/db.rpz.zone; sudo /dns-restart.sh"
