#!/usr/bin/env bash
# deploy script — only in folder2
echo "Deploying..."
docker build -t myapp .
docker push myapp
