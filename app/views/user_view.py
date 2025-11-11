from app.db import execute_query, fetch_one
from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token

user_bp = Blueprint("user", __name__, url_prefix="/user")

@user_bp.route("/login", methods=["POST"])
def login():
    """
    Logs a user in and returns a JWT token.
    """
    data = request.json

    if not data or not data.get("email") or not data.get("senha"):
        return jsonify({"error": "Email ou senha inválidos"}), 400

    query_user = "SELECT id, senha FROM usuario WHERE email = %s"
    user = fetch_one(query_user, (data["email"],))

    if not user or not check_password_hash(user['senha'], data["senha"]):
        return jsonify({"error": "Email ou senha inválidos"}), 401

    access_token = create_access_token(identity=user['id'])
    return jsonify(access_token=access_token)

@user_bp.route("/register", methods=["POST"])
def register():
    """
    Registers a new user as a client or tattoo artist.
    """
    data = request.json

    if not data.get("nome") or not data.get("email") or not data.get("senha") or not data.get("role"):
        return jsonify({"error": "Dados inválidos"}), 400
    
    if data["role"] not in ["cliente", "tatuador"]:
        return jsonify({"error": "Role inválido"}), 400

    query_email = "SELECT id FROM usuario WHERE email = %s"
    if fetch_one(query_email, (data["email"],)):
        return jsonify({"error": "Email já cadastrado"}), 400
    
    hashed_password = generate_password_hash(data["senha"])

    query_insert_user = "INSERT INTO usuario (email, senha) VALUES (%s, %s)"
    execute_query(query_insert_user, (data["email"], hashed_password))
    
    query_user_id = "SELECT id FROM usuario WHERE email = %s"
    user = fetch_one(query_user_id, (data["email"],))
    user_id = user['id']

    if data["role"] == "cliente":
        if not data.get("cidade"):
            return jsonify({"error": "Cidade é obrigatória para clientes"}), 400
        
        query_insert_cliente = "INSERT INTO cliente (nome, cidade, id_usuario) VALUES (%s, %s, %s)"
        execute_query(query_insert_cliente, (data["nome"], data["cidade"], user_id))

    elif data["role"] == "tatuador":
        if not data.get("cidade"):
            return jsonify({"error": "Cidade é obrigatória para tatuadores"}), 400

        query_insert_tatuador = "INSERT INTO tatuador (nome, cidade, id_usuario) VALUES (%s, %s, %s)"
        execute_query(query_insert_tatuador, (data["nome"], data["cidade"], user_id))
    
    return jsonify({"message": "Usuário cadastrado com sucesso!"}), 201