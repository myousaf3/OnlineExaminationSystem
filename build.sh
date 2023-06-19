#!/bin/bash
# Install dependencies
pip install -r requirements.txt
# Run database migrations
python manage.py createsuperuser --no-input
