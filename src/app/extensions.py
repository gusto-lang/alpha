import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from itsdangerous import URLSafeTimedSerializer

db = SQLAlchemy()
migrate = Migrate()
cors = CORS()
jwt = JWTManager()
mail = Mail()
serializer = URLSafeTimedSerializer(os.getenv("SECRET_KEY", "default-secret-key"))