#!/bin/bash

# Build the project
echo "Building the project..."
python -V

echo "Make Migration..."
python3.10 manage.py makemigrations --noinput
python3.10 manage.py migrate --noinput

echo "Collect Static..."
python3.10 manage.py collectstatic --noinput --clear
