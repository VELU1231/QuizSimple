from flask import Flask
from config import config_map


def create_app(env: str = "development") -> Flask:
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.config.from_object(config_map.get(env, config_map["development"]))

    from app.routes.main import main_bp
    from app.routes.api import api_bp
    from app.routes.auth import auth_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp, url_prefix="/api")
    app.register_blueprint(auth_bp, url_prefix="/api/auth")

    return app
