http_status_code=$(curl -s -o /dev/null -w "%{http_code}" https://bored-api.appbrewery.com/random)
echo "http_status_code = $http_status_code"