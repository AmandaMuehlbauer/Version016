#!/usr/bin/env bash
# exit on error
set -o errexit


# Determine the deployment environment based on an environment variable (e.g., DEPLOY_ENV)
if [ "$DEPLOY_ENV" = "production" ]; then
    # Production settings
    DJANGO_SETTINGS_MODULE=blog.production_settings
else
    # Development settings
    DJANGO_SETTINGS_MODULE=blog.settings
fi

# Export the DJANGO_SETTINGS_MODULE environment variable
export DJANGO_SETTINGS_MODULE

# Print the DJANGO_SETTINGS_MODULE environment variable
echo "DJANGO_SETTINGS_MODULE is set to: $DJANGO_SETTINGS_MODULE"

echo "you are here 1"
# Install project dependencies using Poetry
poetry install 

echo "you are here 2"
# Run other necessary commands
poetry run python3 manage.py collectstatic --no-input
poetry run python3 manage.py migrate

# Additional steps for the deployment process (e.g., starting the web server, configuring environment variables)

# Example: Start Gunicorn
export PORT=8000
#poetry run gunicorn blog.wsgi:application -b 0.0.0.0:$PORT

