#!/bin/bash

cd services
python3 stream.py &
python3 listener.py &
cd ..
python3 hello.py