#!/bin/bash
# Install dependencies
pip install -r requirements.txt
# Run database migrations
python manage.py createsuperuser --username admin --password devsinc99
