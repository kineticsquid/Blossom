#!/bin/bash

# Run this to create or re-deploy the function
gcloud run deploy blossom --allow-unauthenticated --project cloud-run-stuff --region us-central1 \
  --source .././ \
  --set-env-vars=DICTIONARY_API_KEY=a0e166af-a0d3-4220-bb35-249b45dd2073