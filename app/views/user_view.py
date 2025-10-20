from app import db
from app.models.user_model import Usuario
from app.models.cliente_model import Cliente
from app.models.tatuador_model import Tatuador
from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash

user_bp = Blueprint("user", __name__)

@user_bp.route("/register", methods=["POST"])

def register():
    data = request.json

    if not data.get("nome") or not data.get("email") or not data.get("senha") or not data.get("role"):
        return jsonify({"error": "Dados inválidos"}), 400
    
    if data["role"] not in ["cliente", "tatuador"]:
        return jsonify({"error": "Role inválido"}), 400

    if Usuario.query.filter_by(email=data["email"]).first():
        return jsonify({"error": "Email já cadastrado"}), 400
    
    hashed_password = generate_password_hash(data["senha"])

    user = Usuario(email = data["email"],
    senha = hashed_password)
    db.session.add(user)
    db.session.commit()

    if data["role"] == "cliente":
        if not data.get("cidade"):
            return jsonify({"error": "Cidade é obrigatória para clientes"}), 400
        
        cliente = Cliente(nome=data["nome"], cidade=data["cidade"], id_usuario=user.id)
        db.session.add(cliente)

    elif data["role"] == "tatuador":
        if not data.get("cidade"):
            return jsonify({"error": "Cidade é obrigatória para tatuadores"}), 400

        tatuador = Tatuador(nome=data["nome"], cidade=data["cidade"], id_usuario=user.id)
        db.session.add(tatuador)

    db.session.commit()
    
    return jsonify({"message": "Usuário cadastrado com sucesso!"}), 201
