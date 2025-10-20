from app import db
from app.models.publicacao_model import Publicacao
from app.models.publicacao_tag_model import PublicacaoTag
from app.models.tatuador_model import Tatuador
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import datetime

publicacao_bp = Blueprint("publicacao", __name__, url_prefix="/publicacao")

@publicacao_bp.route("/", methods=["POST"])
@jwt_required()
def create_publicacao():
    """
    Creates a new publication.
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
    responses:
      201:
        description: Publication created successfully
      400:
        description: Invalid data
      401:
        description: Unauthorized
      404:
        description: Tattoo artist not found
    """
    current_user_id = get_jwt_identity()
    data = request.json

    if not data or not data.get("titulo") or not data.get("descricao"):
        return jsonify({"error": "Dados inválidos"}), 400

    tatuador = Tatuador.query.filter_by(id_usuario=current_user_id).first_or_404()

    publicacao = Publicacao(
        titulo=data["titulo"],
        descricao=data["descricao"],
        id_tatuador=tatuador.id_tatuador,
        data_publicacao=datetime.date.today()
    )

    db.session.add(publicacao)
    db.session.commit()

    return jsonify({"message": "Publicação criada com sucesso!"}), 201

@publicacao_bp.route("/<int:publicacao_id>", methods=["PUT"])
@jwt_required()
def edit_publicacao(publicacao_id):
    """
    Edits a publication.
    ---
    parameters:
      - name: publicacao_id
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
    responses:
      200:
        description: Publication updated successfully
      400:
        description: Invalid data
      401:
        description: Unauthorized
      403:
        description: Forbidden
      404:
        description: Publication not found
    """
    current_user_id = get_jwt_identity()
    publicacao = Publicacao.query.get_or_404(publicacao_id)
    tatuador = Tatuador.query.filter_by(id_usuario=current_user_id).first_or_404()

    if publicacao.id_tatuador != tatuador.id_tatuador:
        return jsonify({"error": "Não autorizado"}), 403

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
@jwt_required()
def delete_publicacao(publicacao_id):
    """
    Deletes a publication.
    ---
    parameters:
      - name: publicacao_id
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
        description: Publication deleted successfully
      401:
        description: Unauthorized
      403:
        description: Forbidden
      404:
        description: Publication not found
    """
    current_user_id = get_jwt_identity()
    publicacao = Publicacao.query.get_or_404(publicacao_id)
    tatuador = Tatuador.query.filter_by(id_usuario=current_user_id).first_or_404()

    if publicacao.id_tatuador != tatuador.id_tatuador:
        return jsonify({"error": "Não autorizado"}), 403

    db.session.delete(publicacao)
    db.session.commit()

    return jsonify({"message": "Publicação removida com sucesso!"}), 200

@publicacao_bp.route("/<int:publicacao_id>/tag", methods=["POST"])
@jwt_required()
def add_tag_to_publicacao(publicacao_id):
    """
    Associates a tag with a publication.
    ---
    parameters:
      - name: publicacao_id
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
            id_tag:
              type: integer
            q_publicacao:
              type: integer
    responses:
      201:
        description: Tag associated successfully
      400:
        description: Invalid data
      401:
        description: Unauthorized
      403:
        description: Forbidden
      404:
        description: Publication not found
    """
    current_user_id = get_jwt_identity()
    publicacao = Publicacao.query.get_or_404(publicacao_id)
    tatuador = Tatuador.query.filter_by(id_usuario=current_user_id).first_or_404()

    if publicacao.id_tatuador != tatuador.id_tatuador:
        return jsonify({"error": "Não autorizado"}), 403

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
