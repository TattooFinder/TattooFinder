from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    # Substitua pela sua string de conexão real
    app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://user:password@host/dbname" 
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    from app.views.user_view import user_bp
    app.register_blueprint(user_bp)

    return app