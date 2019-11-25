from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from data.models import db
from run import create_app

app = create_app('dev')

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()


# Run migrations initialization
# python migrate.py db init

# Run the migration
# python migrate.py db migrate

# Then apply the migration to the database
# python migrate.py db upgrade
