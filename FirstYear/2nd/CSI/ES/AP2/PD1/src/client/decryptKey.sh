#!/bin/bash

openssl rsautl -decrypt -in "$1" -oaep -out "$2" -inkey "$3"
