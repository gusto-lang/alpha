import os
from flask import Flask, jsonify
from .extensions import db, migrate, cors, jwt, mail
from .api.routes import api
from src.admin import setup_admin
from src.utils import APIException, generate_sitemap

def create_app():
    app = Flask(__name__)
    app.url_map.strict_slashes = False

    # Configuración
    db_url = os.getenv("DATABASE_URL")
    if db_url is not None:
        app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///db.sqlite"
    
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['FLASK_APP_KEY'] = os.environ.get('FLASK_APP_KEY', 'sample key')
    app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET_KEY", "super-secret")

    # Inicializar Extensiones
    db.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(app)
    jwt.init_app(app)
    mail.init_app(app)

    # Registrar Blueprints
    app.register_blueprint(api, url_prefix='/api')

    # Configurar Admin
    setup_admin(app)

    # Manejadores de Errores y Ruta Raíz
    @app.errorhandler(APIException)
    def handle_invalid_usage(error):
        return jsonify(error.to_dict()), error.status_code

    @app.route('/')
    def sitemap():
        return generate_sitemap(app)

    return app