#!/bin/bash
# Install dependencies
pip install -r requirements.txt
# Run database migrations
python3 manage.py migrate --no-input
if [[ $CREATE_SUPERUSER ]];
then
  python manage.py createsuperuser --no-input
fi
