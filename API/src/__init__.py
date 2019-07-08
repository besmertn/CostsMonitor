from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

from config import Config


cors = CORS()
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()


def create_app(config_object=Config):
    app = Flask(__name__)
    app.config.from_object(config_object)

    cors.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    from .users.routes import bp as users_bp

    app.register_blueprint(users_bp, url_prefix='/api')

    return app


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    from .entities.revoked_token import RevokedToken
    jti = decrypted_token['jti']

    return RevokedToken.is_jti_blacklisted(jti)
