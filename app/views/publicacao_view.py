from app.db import execute_query, fetch_one
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import datetime

publicacao_bp = Blueprint("publicacao", __name__, url_prefix="/publicacao")

@publicacao_bp.route("/", methods=["POST"])
@jwt_required()
def create_publicacao():
    """
    Creates a new publication.
    """
    current_user_id = get_jwt_identity()
    data = request.json

    if not data or not data.get("titulo") or not data.get("descricao"):
        return jsonify({"error": "Dados inválidos"}), 400

    query_tatuador = "SELECT id_tatuador FROM tatuador WHERE id_usuario = %s"
    tatuador = fetch_one(query_tatuador, (current_user_id,))

    if not tatuador:
        return jsonify({"error": "Tatuador não encontrado"}), 404

    query_insert = """
        INSERT INTO publicacao (titulo, descricao, id_tatuador, data_publicacao)
        VALUES (%s, %s, %s, %s)
    """
    params = (data["titulo"], data["descricao"], tatuador["id_tatuador"], datetime.date.today())
    execute_query(query_insert, params)

    return jsonify({"message": "Publicação criada com sucesso!"}), 201

@publicacao_bp.route("/<int:publicacao_id>", methods=["PUT"])
@jwt_required()
def edit_publicacao(publicacao_id):
    """
    Edits a publication.
    """
    current_user_id = get_jwt_identity()
    
    query_publicacao = "SELECT id_tatuador FROM publicacao WHERE id_publicacao = %s"
    publicacao = fetch_one(query_publicacao, (publicacao_id,))

    if not publicacao:
        return jsonify({"error": "Publicação não encontrada"}), 404

    query_tatuador = "SELECT id_tatuador FROM tatuador WHERE id_usuario = %s"
    tatuador = fetch_one(query_tatuador, (current_user_id,))

    if not tatuador or publicacao['id_tatuador'] != tatuador['id_tatuador']:
        return jsonify({"error": "Não autorizado"}), 403

    data = request.json
    if not data:
        return jsonify({"error": "Dados inválidos"}), 400

    update_fields = []
    params = []
    
    if "titulo" in data:
        update_fields.append("titulo = %s")
        params.append(data["titulo"])
    
    if "descricao" in data:
        update_fields.append("descricao = %s")
        params.append(data["descricao"])

    if not update_fields:
        return jsonify({"error": "Nenhum campo para atualizar"}), 400

    query_update = f"UPDATE publicacao SET {', '.join(update_fields)} WHERE id_publicacao = %s"
    params.append(publicacao_id)
    
    execute_query(query_update, tuple(params))

    return jsonify({"message": "Publicação atualizada com sucesso!"}), 200

@publicacao_bp.route("/<int:publicacao_id>", methods=["DELETE"])
@jwt_required()
def delete_publicacao(publicacao_id):
    """
    Deletes a publication.
    """
    current_user_id = get_jwt_identity()
    
    query_publicacao = "SELECT id_tatuador FROM publicacao WHERE id_publicacao = %s"
    publicacao = fetch_one(query_publicacao, (publicacao_id,))

    if not publicacao:
        return jsonify({"error": "Publicação não encontrada"}), 404

    query_tatuador = "SELECT id_tatuador FROM tatuador WHERE id_usuario = %s"
    tatuador = fetch_one(query_tatuador, (current_user_id,))

    if not tatuador or publicacao['id_tatuador'] != tatuador['id_tatuador']:
        return jsonify({"error": "Não autorizado"}), 403

    query_delete = "DELETE FROM publicacao WHERE id_publicacao = %s"
    execute_query(query_delete, (publicacao_id,))

    return jsonify({"message": "Publicação removida com sucesso!"}), 200

@publicacao_bp.route("/<int:publicacao_id>/tag", methods=["POST"])
@jwt_required()
def add_tag_to_publicacao(publicacao_id):
    """
    Associates a tag with a publication.
    """
    current_user_id = get_jwt_identity()
    
    query_publicacao = "SELECT id_tatuador FROM publicacao WHERE id_publicacao = %s"
    publicacao = fetch_one(query_publicacao, (publicacao_id,))

    if not publicacao:
        return jsonify({"error": "Publicação não encontrada"}), 404

    query_tatuador = "SELECT id_tatuador FROM tatuador WHERE id_usuario = %s"
    tatuador = fetch_one(query_tatuador, (current_user_id,))

    if not tatuador or publicacao['id_tatuador'] != tatuador['id_tatuador']:
        return jsonify({"error": "Não autorizado"}), 403

    data = request.json

    if not data or not data.get("id_tag") or not data.get("q_publicacao"):
        return jsonify({"error": "Dados inválidos"}), 400

    query_insert = "INSERT INTO publicacao_tag (id_publicacao, id_tag, q_publicacao) VALUES (%s, %s, %s)"
    params = (publicacao_id, data["id_tag"], data["q_publicacao"])
    execute_query(query_insert, params)

    return jsonify({"message": "Tag associada com sucesso!"}), 201