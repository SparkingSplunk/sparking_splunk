#!/bin/bash

cd services
python3 stream.py
wait(1)
python3 listener.py
wait(3)
cd ..
python3 hello.py