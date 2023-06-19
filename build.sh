#!/bin/bash
# Install dependencies
pip install -r requirements.txt
# Run database migrations
if [[ $CREATE_SUPERUSER ]];
then
  python manage.py createsuperuser --no-input
fi
