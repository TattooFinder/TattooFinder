from app import db
from app.models.cliente_model import Cliente
from app.models.telefone_cliente_model import TelefoneCliente
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

cliente_bp = Blueprint("cliente", __name__, url_prefix="/cliente")

@cliente_bp.route("/<int:cliente_id>/edit", methods=["PUT"])
@jwt_required()
def edit_cliente(cliente_id):
    """
    Edits a client's profile.
    ---
    parameters:
      - name: cliente_id
        in: path
        type: integer
        required: true
      - name: Authorization
        in: header
        type: string
        required: true
        description: Bearer token
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            nome:
              type: string
            cidade:
              type: string
    responses:
      200:
        description: Profile updated successfully
      400:
        description: Invalid data
      401:
        description: Unauthorized
      403:
        description: Forbidden
      404:
        description: Client not found
    """
    current_user_id = get_jwt_identity()
    cliente = Cliente.query.get_or_404(cliente_id)

    if cliente.id_usuario != current_user_id:
        return jsonify({"error": "Não autorizado"}), 403

    data = request.json

    if not data:
        return jsonify({"error": "Dados inválidos"}), 400

    if "nome" in data:
        cliente.nome = data["nome"]
    
    if "cidade" in data:
        cliente.cidade = data["cidade"]

    db.session.commit()

    return jsonify({"message": "Perfil atualizado com sucesso!"}), 200

@cliente_bp.route("/<int:cliente_id>/telefone", methods=["POST"])
@jwt_required()
def add_telefone_cliente(cliente_id):
    """
    Adds a phone number to a client's profile.
    ---
    parameters:
      - name: cliente_id
        in: path
        type: integer
        required: true
      - name: Authorization
        in: header
        type: string
        required: true
        description: Bearer token
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            numero:
              type: string
    responses:
      201:
        description: Phone number added successfully
      400:
        description: Invalid phone number
      401:
        description: Unauthorized
      403:
        description: Forbidden
      404:
        description: Client not found
    """
    current_user_id = get_jwt_identity()
    cliente = Cliente.query.get_or_404(cliente_id)

    if cliente.id_usuario != current_user_id:
        return jsonify({"error": "Não autorizado"}), 403

    data = request.json

    if not data or not data.get("numero"):
        return jsonify({"error": "Número de telefone inválido"}), 400

    telefone = TelefoneCliente(id_cliente=cliente.id_cliente, numero=data["numero"])
    db.session.add(telefone)
    db.session.commit()

    return jsonify({"message": "Telefone adicionado com sucesso!"}), 201

@cliente_bp.route("/<int:cliente_id>/telefone/<string:numero>", methods=["DELETE"])
@jwt_required()
def delete_telefone_cliente(cliente_id, numero):
    """
    Deletes a phone number from a client's profile.
    ---
    parameters:
      - name: cliente_id
        in: path
        type: integer
        required: true
      - name: numero
        in: path
        type: string
        required: true
      - name: Authorization
        in: header
        type: string
        required: true
        description: Bearer token
    responses:
      200:
        description: Phone number deleted successfully
      401:
        description: Unauthorized
      403:
        description: Forbidden
      404:
        description: Client or phone number not found
    """
    current_user_id = get_jwt_identity()
    cliente = Cliente.query.get_or_404(cliente_id)

    if cliente.id_usuario != current_user_id:
        return jsonify({"error": "Não autorizado"}), 403

    telefone = TelefoneCliente.query.filter_by(id_cliente=cliente_id, numero=numero).first_or_404()
    db.session.delete(telefone)
    db.session.commit()

    return jsonify({"message": "Telefone removido com sucesso!"}), 200
