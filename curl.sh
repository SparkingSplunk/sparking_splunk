#!/bin/bash

while true;
do
	curl -v -k "https://localhost:8088/services/collector" \
		 -H "Authorization: Splunk d70e9818-7474-47f6-90cd-84cd9d38704a" \
		 -d '{"event": "Hello, world!", "sourcetype": "manual"}'
	# "Hello, world!" sent every second
	sleep 1
done