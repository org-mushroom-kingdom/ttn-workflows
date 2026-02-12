#!/bin/bash

# Note: You may get an HTTP 429 (too many requests) if you test this too much within a certain time period
# echo "pwd = $PWD"
# echo "doing ls"
# ls

# Get the server-list.csv file

SERVER_LIST="./docs/server-list.csv"
RED='\033[0;31m'
GREEN='\033[0;32m'
ENDCOLOR='\033[0m' 

cat $SERVER_LIST
# while IFS="," read -r server description
# do
#     http_status_code=$(curl -s -o /dev/null -w "%{http_code}" "${server}")
#     [[ $server = "server" ]] && continue
#     [[ $http_status_code = "200" ]] && color=$GREEN || color=$RED
#     echo -e "${color}${server} : ${http_status_code}${ENDCOLOR}"
# done < "$SERVER_LIST"
