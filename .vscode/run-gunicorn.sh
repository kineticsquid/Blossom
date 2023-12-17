#!/bin/bash
cd ..
gunicorn --workers 4 wsgi_server:app -b :8080