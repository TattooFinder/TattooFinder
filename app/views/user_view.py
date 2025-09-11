from app import db
from app.models.user import User
from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash

user_bp = Blueprint("user", __name__)

@user_bp.route("/register", methods["POST"])

def register():
    data = request.json

    if not data.get("nome") or not data.get("email") or not data.get("senha"):
        return jsonify({"error": "Dados inválidos"}), 400
    
    if User.query.filter_by(email=data["email"]).first():
        return jsonify({"error": "Email já cadastrado"}), 400
    
    hashed_password =
    generate_password_hash(data["senha"])

    user = User(nome=data["nome"], email = data["email"],
    senha = hashed_password)
    db.session.add(user)
    db.session.commit()
    
    return jsonify({"message": "Usuário cadastrado com sucesso!"}), 201
