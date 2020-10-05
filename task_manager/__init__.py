import os
from flask import Flask
from .db import db


def create_app():
    app = Flask(__name__)
    app.config.from_object(os.environ["APP_SETTINGS"])

    db.init_app(app)
    with app.test_request_context():
        db.create_all()

    # Импортирование blueprints
    import task_manager.auth.views as auth_module
    import task_manager.tasks.views as task_module
    # Регистрация blueprints
    app.register_blueprint(auth_module.auth_module)
    app.register_blueprint(task_module.task_module)

    return app
