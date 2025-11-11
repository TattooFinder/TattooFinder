from app.db import execute_query, fetch_one
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

tag_bp = Blueprint("tag", __name__, url_prefix="/tag")

@tag_bp.route("/", methods=["POST"])
@jwt_required()
def create_tag():
    """
    Creates a new tag.
    """
    current_user_id = get_jwt_identity()
    data = request.json

    if not data or not data.get("nome") or not data.get("descricao"):
        return jsonify({"error": "Dados inválidos"}), 400

    query_tatuador = "SELECT id_tatuador FROM tatuador WHERE id_usuario = %s"
    tatuador = fetch_one(query_tatuador, (current_user_id,))

    if not tatuador:
        return jsonify({"error": "Tatuador não encontrado"}), 404

    query_insert = """
        INSERT INTO tag (nome, descricao, id_tatuador)
        VALUES (%s, %s, %s)
    """
    params = (data["nome"], data["descricao"], tatuador["id_tatuador"])
    execute_query(query_insert, params)

    return jsonify({"message": "Tag criada com sucesso!"}), 201