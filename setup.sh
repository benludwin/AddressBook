#!/bin/sh

echo "[Installation]: checking neccesary dependancies"
curl  https://bootstrap.pypa.io/get-pip.py -o get-pip.py
sudo python get-pip.py
find -name 'requirements.txt'
sudo -H pip install -r requirements.txt
chmod +x run.sh
