from app import db
from app.models.feedback_model import Feedback
from flask import Blueprint, request, jsonify
import datetime

feedback_bp = Blueprint("feedback", __name__, url_prefix="/feedback")

@feedback_bp.route("/", methods=["POST"])
def create_feedback():
    data = request.json

    if not data or not data.get("titulo") or not data.get("descricao") or not data.get("nota_avaliativa") or not data.get("id_cliente"):
        return jsonify({"error": "Dados inválidos"}), 400

    feedback = Feedback(
        titulo=data["titulo"],
        descricao=data["descricao"],
        nota_avaliativa=data["nota_avaliativa"],
        id_cliente=data["id_cliente"],
        data_publicacao=datetime.date.today()
    )

    db.session.add(feedback)
    db.session.commit()

    return jsonify({"message": "Feedback criado com sucesso!"}), 201

@feedback_bp.route("/<int:feedback_id>", methods=["PUT"])
def edit_feedback(feedback_id):
    feedback = Feedback.query.get_or_404(feedback_id)
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
def delete_feedback(feedback_id):
    feedback = Feedback.query.get_or_404(feedback_id)
    db.session.delete(feedback)
    db.session.commit()

    return jsonify({"message": "Feedback removido com sucesso!"}), 200
