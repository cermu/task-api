import os
from flask import Flask
from utils.settings import config_by_name


def create_app(config_name):
    app = Flask(__name__)
    config_obj = config_by_name[config_name]
    app.config.from_object(config_obj)

    from main.app import api_bp
    app.register_blueprint(api_bp, url_prefix='/api/v1')

    from data.models import db
    db.init_app(app)

    return app


if __name__ == '__main__':
    config_name = os.getenv('APP_SETTINGS')
    app = create_app(config_name or 'dev')
    app.run()

# Run dev server with the below command
# python run.py

