#!/bin/bash

# keep sending data until interrupt
while true;
do
	curl -v -k "https://localhost:8088/services/collector" \
		 -H "Authorization: Splunk d117233f-987f-48a0-9667-bfb7dce6c587" \
		 -d '{"event": "Hello, Bootcamp2020!", "sourcetype": "manual", "source": "testsrc"}'
	# "Hello, world!" sent every second
	sleep 1
done