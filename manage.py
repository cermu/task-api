import os

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from main.app import create_app, db


config_name = os.getenv('APP_SETTINGS')
app = create_app(config_name or 'dev')
app.app_context().push()

manager = Manager(app)

migrate = Migrate(app, db)

manager.add_command('database', MigrateCommand)


@manager.command
def run():
    app.run()


if __name__ == '__main__':
    manager.run()

# Run dev server with the below command
# COMMAND: python manage.py run

# Initiate a migration folder using
# COMMAND: python manage.py database init

# Create a migration script from the detected changes in the model using
# COMMAND: python manage.py database migrate --message 'initial database migration'

# Apply the migration script to the database by using
# COMMAND: python manage.py database upgrade
