from app import db
from app.models.publicacao_model import Publicacao
from app.models.publicacao_tag_model import PublicacaoTag
from flask import Blueprint, request, jsonify
import datetime

publicacao_bp = Blueprint("publicacao", __name__, url_prefix="/publicacao")

@publicacao_bp.route("/", methods=["POST"])
def create_publicacao():
    data = request.json

    if not data or not data.get("titulo") or not data.get("descricao") or not data.get("id_tatuador"):
        return jsonify({"error": "Dados inválidos"}), 400

    publicacao = Publicacao(
        titulo=data["titulo"],
        descricao=data["descricao"],
        id_tatuador=data["id_tatuador"],
        data_publicacao=datetime.date.today()
    )

    db.session.add(publicacao)
    db.session.commit()

    return jsonify({"message": "Publicação criada com sucesso!"}), 201

@publicacao_bp.route("/<int:publicacao_id>", methods=["PUT"])
def edit_publicacao(publicacao_id):
    publicacao = Publicacao.query.get_or_404(publicacao_id)
    data = request.json

    if not data:
        return jsonify({"error": "Dados inválidos"}), 400

    if "titulo" in data:
        publicacao.titulo = data["titulo"]
    
    if "descricao" in data:
        publicacao.descricao = data["descricao"]

    db.session.commit()

    return jsonify({"message": "Publicação atualizada com sucesso!"}), 200

@publicacao_bp.route("/<int:publicacao_id>", methods=["DELETE"])
def delete_publicacao(publicacao_id):
    publicacao = Publicacao.query.get_or_404(publicacao_id)
    db.session.delete(publicacao)
    db.session.commit()

    return jsonify({"message": "Publicação removida com sucesso!"}), 200

@publicacao_bp.route("/<int:publicacao_id>/tag", methods=["POST"])
def add_tag_to_publicacao(publicacao_id):
    data = request.json

    if not data or not data.get("id_tag") or not data.get("q_publicacao"):
        return jsonify({"error": "Dados inválidos"}), 400

    publicacao_tag = PublicacaoTag(
        id_publicacao=publicacao_id,
        id_tag=data["id_tag"],
        q_publicacao=data["q_publicacao"]
    )

    db.session.add(publicacao_tag)
    db.session.commit()

    return jsonify({"message": "Tag associada com sucesso!"}), 201
