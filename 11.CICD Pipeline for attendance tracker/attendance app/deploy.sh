#!/bin/bash

cd /home/ec2-user/app

pkill node || true

npm install

nohup node app.js > output.log 2>&1 &