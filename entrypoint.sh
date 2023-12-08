#!/bin/sh

# Wait for the database to be ready
python manage.py wait_for_db

# Apply migrations
python manage.py migrate

# Create superuser
if [ "$DJANGO_SUPERUSER_USERNAME" ] && [ "$DJANGO_SUPERUSER_PASSWORD" ] && [ "$DJANGO_SUPERUSER_EMAIL" ]; then
    echo "Creating superuser"
    python manage.py createsuperuser --noinput
else
    echo "Superuser not created. Some environment variables are missing."
fi

# Start the Django development server
# python manage.py runserver 0.0.0.0:8000
