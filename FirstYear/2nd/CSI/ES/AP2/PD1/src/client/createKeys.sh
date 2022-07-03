#!/bin/bash

for((i=$1; i <= $2; i++))
do
    openssl genrsa -out privateKey"${i}".pem 2048
    openssl rsa -in privateKey"${i}".pem -pubout -out publickey"${i}".crt
done
