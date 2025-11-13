from app.db import execute_query, fetch_one
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

cliente_bp = Blueprint("cliente", __name__, url_prefix="/cliente")

@cliente_bp.route("/<int:cliente_id>/edit", methods=["PUT"])
@jwt_required()
def edit_cliente(cliente_id):
    """
    Edits a client's profile.
    """
    current_user_id = get_jwt_identity()
    
    query_auth = "SELECT id_usuario FROM cliente WHERE id_cliente = %s"
    cliente_auth = fetch_one(query_auth, (cliente_id,))
    
    if not cliente_auth:
        return jsonify({"error": "Cliente não encontrado"}), 404

    if cliente_auth['id_usuario'] != current_user_id:
        return jsonify({"error": "Não autorizado"}), 403

    data = request.json
    if not data:
        return jsonify({"error": "Dados inválidos"}), 400

    update_fields = []
    params = []
    
    if "nome" in data:
        update_fields.append("nome = %s")
        params.append(data["nome"])
    
    if "cidade" in data:
        update_fields.append("cidade = %s")
        params.append(data["cidade"])

    if not update_fields:
        return jsonify({"error": "Nenhum campo para atualizar"}), 400

    query_update = f"UPDATE cliente SET {', '.join(update_fields)} WHERE id_cliente = %s"
    params.append(cliente_id)
    
    execute_query(query_update, tuple(params))

    return jsonify({"message": "Perfil atualizado com sucesso!"}), 200

@cliente_bp.route("/<int:cliente_id>/telefone", methods=["POST"])
@jwt_required()
def add_telefone_cliente(cliente_id):
    """
    Adds a phone number to a client's profile.
    """
    current_user_id = get_jwt_identity()
    
    query_auth = "SELECT id_usuario FROM cliente WHERE id_cliente = %s"
    cliente_auth = fetch_one(query_auth, (cliente_id,))

    if not cliente_auth:
        return jsonify({"error": "Cliente não encontrado"}), 404

    if cliente_auth['id_usuario'] != current_user_id:
        return jsonify({"error": "Não autorizado"}), 403

    data = request.json

    if not data or not data.get("numero"):
        return jsonify({"error": "Número de telefone inválido"}), 400

    query_insert = "INSERT INTO telefone_cliente (id_cliente, numero) VALUES (%s, %s)"
    execute_query(query_insert, (cliente_id, data["numero"]))

    return jsonify({"message": "Telefone adicionado com sucesso!"}), 201

@cliente_bp.route("/<int:cliente_id>/telefone/<string:numero>", methods=["DELETE"])
@jwt_required()
def delete_telefone_cliente(cliente_id, numero):
    """
    Deletes a phone number from a client's profile.
    """
    current_user_id = get_jwt_identity()
    
    query_auth = "SELECT id_usuario FROM cliente WHERE id_cliente = %s"
    cliente_auth = fetch_one(query_auth, (cliente_id,))

    if not cliente_auth:
        return jsonify({"error": "Cliente não encontrado"}), 404

    if cliente_auth['id_usuario'] != current_user_id:
        return jsonify({"error": "Não autorizado"}), 403

    query_delete = "DELETE FROM telefone_cliente WHERE id_cliente = %s AND numero = %s"
    execute_query(query_delete, (cliente_id, numero))

    return jsonify({"message": "Telefone removido com sucesso!"}), 200