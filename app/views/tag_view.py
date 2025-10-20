from app import db
from app.models.tag_model import Tag
from app.models.tatuador_model import Tatuador
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

tag_bp = Blueprint("tag", __name__, url_prefix="/tag")

@tag_bp.route("/", methods=["POST"])
@jwt_required()
def create_tag():
    """
    Creates a new tag.
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
            nome:
              type: string
            descricao:
              type: string
    responses:
      201:
        description: Tag created successfully
      400:
        description: Invalid data
      401:
        description: Unauthorized
      404:
        description: Tattoo artist not found
    """
    current_user_id = get_jwt_identity()
    data = request.json

    if not data or not data.get("nome") or not data.get("descricao"):
        return jsonify({"error": "Dados inválidos"}), 400

    tatuador = Tatuador.query.filter_by(id_usuario=current_user_id).first_or_404()

    tag = Tag(
        nome=data["nome"],
        descricao=data["descricao"],
        id_tatuador=tatuador.id_tatuador
    )

    db.session.add(tag)
    db.session.commit()

    return jsonify({"message": "Tag criada com sucesso!"}), 201
