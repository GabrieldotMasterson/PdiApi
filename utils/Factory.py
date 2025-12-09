from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from spectree import SecurityScheme, SpecTree

from utils.Config import Config

db = SQLAlchemy()
migrate = Migrate()

api = SpecTree(
    "flask",
    title="PDI API",
    version="v.0.1",
    path="docs",
    security_schemes=[
        SecurityScheme(
            name="api_key",
            data={"type": "apiKey", "name": "Authorization", "in": "header"},
        )
    ],
    security={"api_key": []},
)

def Create_app():
    app = Flask(__name__)

    app.config.from_object(Config)
    
    db.init_app(app)

    from models import UserModel
    migrate.init_app(app, db)

    from controllers.AuthController import auth_controller
    from controllers.UserController import user_controller
    from controllers.PdiController import pdi_controller
    from controllers.ProjectController import project_controller
    from controllers.TaskController import task_controller
    from controllers.GoalController import goal_controller  

    app.register_blueprint(goal_controller)
    app.register_blueprint(task_controller)
    app.register_blueprint(project_controller)
    app.register_blueprint(pdi_controller)
    app.register_blueprint(auth_controller)
    app.register_blueprint(user_controller)

    api.register(app)

    return app

