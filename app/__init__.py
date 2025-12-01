import os
from flask import Flask
from flask_jwt_extended import JWTManager
from flasgger import Swagger

def create_app():
    app = Flask(__name__, 
                static_folder="../", 
                static_url_path="", 
                template_folder="../frontEnd")

    app.config["JWT_SECRET_KEY"] = "super-secret"
    # Configura o Flask-JWT-Extended para usar cookies
    app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
    app.config["JWT_COOKIE_CSRF_PROTECT"] = False # Simplificando por agora, idealmente seria True
    app.config['UPLOAD_FOLDER'] = 'frontEnd/pics/user_uploads'


    jwt = JWTManager(app)
    swagger = Swagger(app)

    from app.routes.auth_view import auth_bp
    from app.routes.perfil_view import perfil_bp
    from app.routes.main_view import main_bp
    from app.routes.tatuador_view import tatuador_bp
    from app.routes.publicacao_view import publicacao_bp
    from app.routes.tag_view import tag_bp
    from app.routes.feedback_view import feedback_bp
    from app.routes.search_view import search_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(perfil_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(tatuador_bp)
    app.register_blueprint(publicacao_bp)
    app.register_blueprint(tag_bp)
    app.register_blueprint(feedback_bp)
    app.register_blueprint(search_bp)

    return app