import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flasgger import Swagger

db = SQLAlchemy()

def create_app():
    app = Flask(__name__, template_folder="../frontEnd")

    # Configura a URI do banco de dados a partir das variáveis de ambiente
    db_host = os.getenv("DB_HOST")
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")
    db_name = os.getenv("DB_NAME")
    
    app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_SECRET_KEY"] = "super-secret"

    db.init_app(app)
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
