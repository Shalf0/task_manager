import os
from flask_script import Manager
from task_manager import create_app
from task_manager.db import db
from flask_migrate import Migrate, MigrateCommand


app = create_app()
app.config.from_object(os.environ['APP_SETTINGS'])
manager = Manager(app)
migrate = Migrate(app, db)


# Добавление комманд
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
