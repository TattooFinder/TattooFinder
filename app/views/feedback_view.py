from app import db
from app.models.feedback_model import Feedback
from app.models.cliente_model import Cliente
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import datetime

feedback_bp = Blueprint("feedback", __name__, url_prefix="/feedback")

@feedback_bp.route("/", methods=["POST"])
@jwt_required()
def create_feedback():
    """
    Creates a new feedback.
    ---
    parameters:
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
            titulo:
              type: string
            descricao:
              type: string
            nota_avaliativa:
              type: integer
            id_tatuador:
              type: integer
    responses:
      201:
        description: Feedback created successfully
      400:
        description: Invalid data
      401:
        description: Unauthorized
      404:
        description: Client not found
    """
    current_user_id = get_jwt_identity()
    data = request.json

    if not data or not data.get("titulo") or not data.get("descricao") or not data.get("nota_avaliativa") or not data.get("id_tatuador"):
        return jsonify({"error": "Dados inválidos"}), 400

    cliente = Cliente.query.filter_by(id_usuario=current_user_id).first_or_404()

    feedback = Feedback(
        titulo=data["titulo"],
        descricao=data["descricao"],
        nota_avaliativa=data["nota_avaliativa"],
        id_cliente=cliente.id_cliente,
        id_tatuador=data["id_tatuador"],
        data_publicacao=datetime.date.today()
    )

    db.session.add(feedback)
    db.session.commit()

    return jsonify({"message": "Feedback criado com sucesso!"}), 201

@feedback_bp.route("/<int:feedback_id>", methods=["PUT"])
@jwt_required()
def edit_feedback(feedback_id):
    """
    Edits a feedback.
    ---
    parameters:
      - name: feedback_id
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
            titulo:
              type: string
            descricao:
              type: string
            nota_avaliativa:
              type: integer
    responses:
      200:
        description: Feedback updated successfully
      400:
        description: Invalid data
      401:
        description: Unauthorized
      403:
        description: Forbidden
      404:
        description: Feedback not found
    """
    current_user_id = get_jwt_identity()
    feedback = Feedback.query.get_or_404(feedback_id)
    cliente = Cliente.query.filter_by(id_usuario=current_user_id).first_or_404()

    if feedback.id_cliente != cliente.id_cliente:
        return jsonify({"error": "Não autorizado"}), 403

    data = request.json

    if not data:
        return jsonify({"error": "Dados inválidos"}), 400

    if "titulo" in data:
        feedback.titulo = data["titulo"]
    
    if "descricao" in data:
        feedback.descricao = data["descricao"]

    if "nota_avaliativa" in data:
        feedback.nota_avaliativa = data["nota_avaliativa"]

    db.session.commit()

    return jsonify({"message": "Feedback atualizado com sucesso!"}), 200

@feedback_bp.route("/<int:feedback_id>", methods=["DELETE"])
@jwt_required()
def delete_feedback(feedback_id):
    """
    Deletes a feedback.
    ---
    parameters:
      - name: feedback_id
        in: path
        type: integer
        required: true
      - name: Authorization
        in: header
        type: string
        required: true
        description: Bearer token
    responses:
      200:
        description: Feedback deleted successfully
      401:
        description: Unauthorized
      403:
        description: Forbidden
      404:
        description: Feedback not found
    """
    current_user_id = get_jwt_identity()
    feedback = Feedback.query.get_or_404(feedback_id)
    cliente = Cliente.query.filter_by(id_usuario=current_user_id).first_or_404()

    if feedback.id_cliente != cliente.id_cliente:
        return jsonify({"error": "Não autorizado"}), 403

    db.session.delete(feedback)
    db.session.commit()

    return jsonify({"message": "Feedback removido com sucesso!"}), 200
