#!/bin/sh
# Run database migrations
uv run manage.py migrate
# Start the Django development server
uv run manage.py runserver 0.0.0.0:8000