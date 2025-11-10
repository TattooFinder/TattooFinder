import os
from flask import Flask
from flask_jwt_extended import JWTManager
from flasgger import Swagger

def create_app():
    app = Flask(__name__, template_folder="../frontEnd")

    app.config["JWT_SECRET_KEY"] = "super-secret"

    jwt = JWTManager(app)
    swagger = Swagger(app)

    from app.views.user_view import user_bp
    from app.views.main_view import main_bp
    from app.views.cliente_view import cliente_bp
    from app.views.tatuador_view import tatuador_bp
    from app.views.publicacao_view import publicacao_bp
    from app.views.tag_view import tag_bp
    from app.views.feedback_view import feedback_bp
    app.register_blueprint(user_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(cliente_bp)
    app.register_blueprint(tatuador_bp)
    app.register_blueprint(publicacao_bp)
    app.register_blueprint(tag_bp)
    app.register_blueprint(feedback_bp)

    return app