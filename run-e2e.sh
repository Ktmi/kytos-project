#!/bin/bash

cd kytos-docker

sudo docker build . -t amlight/kytos --no-cache

cd ../kytos-end-to-end-tests

sudo docker-compose up -d

sudo docker-compose logs -f kytos | tee ../e2e-results.log

sudo docker-compose down -v

cd ..
