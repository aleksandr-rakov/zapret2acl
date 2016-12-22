#!/bin/bash

SERVER=$1
PORT=$2
FNAME=$3

echo $SERVER $PORT
echo $FNAME
scp -P $PORT $FNAME $SERVER:/home/doggy/dns 