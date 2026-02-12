#!/bin/bash

# Note: You may get an HTTP 429 (too many requests) if you test this too much within a certain time period
# echo "pwd = $PWD"
# echo "doing ls"
# ls

# Get the server-list.csv file

SERVER_LIST="./docs/server-list.csv"
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m' 

while IFS="," read -r server description
do
    echo "Server = $server"
    http_status_code=$(curl -s -o /dev/null -w "%{http_code}" https://example.com)
    if [[ $http_status_code = "200" ]]
    then
        echo "HOORAY"
    fi
    echo "http_status_code = $http_status_code"
done < "$SERVER_LIST"
