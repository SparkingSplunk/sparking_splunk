-- How to send data to Splunk and then send it to a specified port. Have a separate terminal for each of these steps and make sure you're in the correct directories --
1. Go to /Applications/Splunk/bin
   nc -lk 9997
   (Setting up the port listener so that we know that the port is receiving data)
2. Go to /Applications/Splunk/bin
   ./splunk restart
   (Starting Splunk)
3. Go to /sparking_splunk/dataGen
   bash curl.sh 
   (Sending data)



-- APPEND THESE LINES TO THE SPECIFIED FILES! -- 

props.conf: 
[source::testsrc]
TRANSFORMS-testsrc=group1transform


outputs.conf:
[tcpout]
defaultGroup=nothing

[tcpout:group1]
server=127.0.0.1:9997
sendCookedData = false


transforms.conf:
[group1transform]
REGEX = . 
DEST_KEY=_TCP_ROUTING
FORMAT=group1
