from app.db import execute_query, fetch_one
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import datetime

feedback_bp = Blueprint("feedback", __name__, url_prefix="/feedback")

@feedback_bp.route("/", methods=["POST"])
@jwt_required()
def create_feedback():
    """
    Creates a new feedback.
    """
    current_user_id = get_jwt_identity()
    data = request.json

    if not data or not data.get("titulo") or not data.get("descricao") or not data.get("nota_avaliativa") or not data.get("id_tatuador"):
        return jsonify({"error": "Dados inválidos"}), 400

    query_cliente = "SELECT id_cliente FROM cliente WHERE id_usuario = %s"
    cliente = fetch_one(query_cliente, (current_user_id,))

    if not cliente:
        return jsonify({"error": "Cliente não encontrado"}), 404

    query_insert = """
        INSERT INTO feedback (titulo, descricao, nota_avaliativa, id_cliente, id_tatuador, data_publicacao)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    params = (data["titulo"], data["descricao"], data["nota_avaliativa"], cliente["id_cliente"], data["id_tatuador"], datetime.date.today())
    execute_query(query_insert, params)

    return jsonify({"message": "Feedback criado com sucesso!"}), 201

@feedback_bp.route("/<int:feedback_id>", methods=["PUT"])
@jwt_required()
def edit_feedback(feedback_id):
    """
    Edits a feedback.
    """
    current_user_id = get_jwt_identity()
    
    query_feedback = "SELECT id_cliente FROM feedback WHERE id_feedback = %s"
    feedback = fetch_one(query_feedback, (feedback_id,))

    if not feedback:
        return jsonify({"error": "Feedback não encontrado"}), 404

    query_cliente = "SELECT id_cliente FROM cliente WHERE id_usuario = %s"
    cliente = fetch_one(query_cliente, (current_user_id,))

    if not cliente or feedback['id_cliente'] != cliente['id_cliente']:
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

    if "nota_avaliativa" in data:
        update_fields.append("nota_avaliativa = %s")
        params.append(data["nota_avaliativa"])

    if not update_fields:
        return jsonify({"error": "Nenhum campo para atualizar"}), 400

    query_update = f"UPDATE feedback SET {', '.join(update_fields)} WHERE id_feedback = %s"
    params.append(feedback_id)
    
    execute_query(query_update, tuple(params))

    return jsonify({"message": "Feedback atualizado com sucesso!"}), 200

@feedback_bp.route("/<int:feedback_id>", methods=["DELETE"])
@jwt_required()
def delete_feedback(feedback_id):
    """
    Deletes a feedback.
    """
    current_user_id = get_jwt_identity()
    
    query_feedback = "SELECT id_cliente FROM feedback WHERE id_feedback = %s"
    feedback = fetch_one(query_feedback, (feedback_id,))

    if not feedback:
        return jsonify({"error": "Feedback não encontrado"}), 404

    query_cliente = "SELECT id_cliente FROM cliente WHERE id_usuario = %s"
    cliente = fetch_one(query_cliente, (current_user_id,))

    if not cliente or feedback['id_cliente'] != cliente['id_cliente']:
        return jsonify({"error": "Não autorizado"}), 403

    query_delete = "DELETE FROM feedback WHERE id_feedback = %s"
    execute_query(query_delete, (feedback_id,))

    return jsonify({"message": "Feedback removido com sucesso!"}), 200