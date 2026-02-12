# Note: You may get an HTTP 429 (too many requests) if you test this too much within a certain time period
echo "pwd = $PWD"
echo "doing ls"
ls

# Get the server-list.csv file

SERVER_LIST="./docs/server-list.csv"

while IFS =, read -r server
do
    echo "Server = $server"
done < "$INPUT_FILE"

# http_status_code=$(curl -s -o /dev/null -w "%{http_code}" https://example.com)
# echo "http_status_code = $http_status_code"