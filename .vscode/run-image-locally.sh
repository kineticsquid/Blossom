#!/bin/bash

# Now run locally. Use "rm" to remove the container once it finishes
docker run --rm -p 8080:8080 \
    --env DICTIONARY_API_KEY=a0e166af-a0d3-4220-bb35-249b45dd2073 \
    kineticsquid/blossom:latest



