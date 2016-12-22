#!/bin/bash

SERVER=$1
PORT=$2
FNAME=$3

scp -oStrictHostKeyChecking=no -P $PORT $FNAME $SERVER:/home/doggy/dns

ssh -oStrictHostKeyChecking=no -p $PORT $SERVER "sudo cp /home/doggy/dns /etc/bind/db.rpz.zone; sudo /dns-restart.sh"
