#!/bin/bash


# Apply Django migrations
python manage.py makemigrations
python manage.py migrate
uvicorn learngpt.asgi:application --host 0.0.0.0 --port 9000 --reload --reload-include '*.html' --reload-delay 1