#!/bin/bash

docker rmi kineticsquid/blossom:latest
docker build --rm --no-cache --pull -t kineticsquid/blossom:latest -f Dockerfile .
docker push kineticsquid/blossom:latest

# list the current images
echo "Docker Images..."
docker images

echo "Now running..."
./.vscode/run-image-locally.sh
