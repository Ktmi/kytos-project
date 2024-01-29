#!/bin/bash
export MONGO_USERNAME=napp_user
export MONGO_PASSWORD=napp_pw

kytosd -f -E --database mongodb --apm es
