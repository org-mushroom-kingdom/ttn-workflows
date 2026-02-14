#!/bin/bash

# Note: You may get an HTTP 429 (too many requests) if you test this too much within a certain time period

# Uncomment these to get context of where the runner is pointed (/home/runner/work/ttn-workflows/ttn-workflows). 
# Note: For PWD, you'll see your repo name twice at the end. This is because the workspace folder is /home/runner/work/<repo-name>
# We then checkout the repo in a subfolder that is named after the repo being checked out (ttn-workflows). We cd to that subfolder so pwd is /home/runner/work/ttn-workflows/ttn-workflows
# echo "pwd = $PWD"

# echo "doing ls"
# ls

# Get the server-list.csv file

SERVER_LIST="./deploys/server-list.csv"
# Workflow logs supports ANSI color escape sequences like the ones below.  
RED='\033[0;31m'
GREEN='\033[0;32m'
ENDCOLOR='\033[0m' 
msg_color=""
msg=""
# TODO: COMMENT ABOUT $ NEWLINE THING
# cat -A $SERVER_LIST

# TODO: Break this down. IFS,read -r,>SERVER_LIST
while IFS="," read -r server description
do
    # Skip the header (continue to next iteration)
    [[ $server = "server" ]] && continue
    # TODO: break this down
    http_status_code=$(curl -s -o /dev/null -w "%{http_code}" "${server}")
    # if-else shorthand: [[Conditional]] && if-true-do-this || if-false-do-this
    # For this we set the var 'msg_color' to $GREEN if we get a 200. If not 200, set msg_colorcolor to $RED
    [[ $http_status_code = "200" ]] && msg_color=$GREEN || msg_color=$RED
    # Just like above, but for the content of 'msg'
    [[ $http_status_code = "200" ]] && msg="(SUCCESS)" || msg="(FAILURE)"
    
    echo -e "${server} : ${msg_color}${http_status_code} ${msg}${ENDCOLOR}"
done < "$SERVER_LIST"
