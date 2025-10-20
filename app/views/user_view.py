from app import db
from app.models.user_model import Usuario
from app.models.cliente_model import Cliente
from app.models.tatuador_model import Tatuador
from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token

user_bp = Blueprint("user", __name__, url_prefix="/user")

@user_bp.route("/login", methods=["POST"])
def login():
    """
    Logs a user in and returns a JWT token.
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            email:
              type: string
            senha:
              type: string
    responses:
      200:
        description: Login successful
        schema:
          type: object
          properties:
            access_token:
              type: string
      400:
        description: Invalid email or password
      401:
        description: Invalid email or password
    """
    data = request.json

    if not data or not data.get("email") or not data.get("senha"):
        return jsonify({"error": "Email ou senha inválidos"}), 400

    user = Usuario.query.filter_by(email=data["email"]).first()

    if not user or not check_password_hash(user.senha, data["senha"]):
        return jsonify({"error": "Email ou senha inválidos"}), 401

    access_token = create_access_token(identity=user.id)
    return jsonify(access_token=access_token)

@user_bp.route("/register", methods=["POST"])
def register():
    """
    Registers a new user as a client or tattoo artist.
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            nome:
              type: string
            email:
              type: string
            senha:
              type: string
            role:
              type: string
              enum: ["cliente", "tatuador"]
            cidade:
              type: string
    responses:
      201:
        description: User registered successfully
      400:
        description: Invalid data
    """
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
