from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_marshmallow import Marshmallow
from config import Config

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
ma = Marshmallow()
login_manager.login_view = 'auth_api.login'

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Habilita CORS para permitir que o frontend (em localhost:3000) acesse o backend (em localhost:5000)
    CORS(app, supports_credentials=True)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    ma.init_app(app)

    with app.app_context():
        # Importar e Registrar Blueprints
        from app.api.clients import clients_api
        from app.api.dashboard import dashboard_api
        from app.api.files import files_api
        from app.api.auth import auth_api
        from app.api.notes import notes_api
        from app.api.tasks import tasks_api

        app.register_blueprint(clients_api, url_prefix='/api')
        app.register_blueprint(dashboard_api, url_prefix='/api')
        app.register_blueprint(files_api, url_prefix='/api')
        app.register_blueprint(auth_api, url_prefix='/api/auth')
        app.register_blueprint(notes_api, url_prefix='/api')
        app.register_blueprint(tasks_api, url_prefix='/api')

        # Importa os modelos para que o Flask-Migrate os reconheça
        from app.models import user, client, file, note, task

    return app