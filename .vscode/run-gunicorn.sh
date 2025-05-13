#!/bin/bash
export DICTIONARY_API_KEY=a0e166af-a0d3-4220-bb35-249b45dd2073
cd ..
gunicorn --workers 4 wsgi_server:app -b :8080