import os

from main.app import create_app


config_name = os.getenv('APP_SETTINGS')
app = create_app(config_name or 'prod')

# gunicorn --bind 0.0.0.0:5000 wsgi:app
