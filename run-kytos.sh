#!/bin/bash
export MONGO_USERNAME=napp_user
export MONGO_PASSWORD=napp_pw

cd kytos/
sudo docker-compose up -d
kytosd -f 
sudo docker-compose down
cd ..
