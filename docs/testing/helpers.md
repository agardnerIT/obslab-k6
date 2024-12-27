``` { "name": "check env vars exist"}
if [ -z "${DT_URL}" ]; then
  exit 1
fi
if [ -z "${DT_K6_TOKEN}" ]; then
  exit 1
fi
```

``` {"name": "wait for docker to start"}
until docker ps | grep -q "CONTAINER ID";
do 
  sleep 1; 
done
```