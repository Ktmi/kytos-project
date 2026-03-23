#!/bin/bash

sudo docker run -it --network kytos-db_default --rm mongo:7.0 mongosh -u napp_user -p napp_pw mongodb://mongo1/napps
