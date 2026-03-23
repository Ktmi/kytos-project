#!/bin/bash

cd ui
npm install
npm run build
rm -rfv ../kytos/kytos/web-ui/
mv -v web-ui/ ../kytos/kytos/web-ui/
cd ..
