from app import db
from app.models.tag_model import Tag
from flask import Blueprint, request, jsonify

tag_bp = Blueprint("tag", __name__, url_prefix="/tag")

@tag_bp.route("/", methods=["POST"])
def create_tag():
    data = request.json

    if not data or not data.get("nome") or not data.get("descricao") or not data.get("id_tatuador"):
        return jsonify({"error": "Dados inválidos"}), 400

    tag = Tag(
        nome=data["nome"],
        descricao=data["descricao"],
        id_tatuador=data["id_tatuador"]
    )

    db.session.add(tag)
    db.session.commit()

    return jsonify({"message": "Tag criada com sucesso!"}), 201
