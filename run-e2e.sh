#!/bin/bash

cd kytos-docker

sudo docker build . -t amlight/kytos --no-cache

cd ../kytos-end-to-end-tests

sudo docker-compose -p kytos-tests up -d

sudo docker-compose -p kytos-tests logs -f kytos | tee ../e2e-results.log

sudo docker-compose -p kytos-tests down -v

cd ..
