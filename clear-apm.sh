#!/bin/bash

cd kytos/
sudo docker-compose -p kytos-apm -f docker-compose.es.yml down -v
cd ..
