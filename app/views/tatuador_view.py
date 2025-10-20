from app import db
from app.models.tatuador_model import Tatuador
from app.models.telefone_tatuador_model import TelefoneTatuador
from app.models.publicacao_model import Publicacao
from app.models.feedback_model import Feedback
from app.models.cliente_model import Cliente
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

tatuador_bp = Blueprint("tatuador", __name__, url_prefix="/tatuador")

@tatuador_bp.route("/<int:tatuador_id>", methods=["GET"])
def get_tatuador(tatuador_id):
    """
    Gets a tattoo artist's profile.
    ---
    parameters:
      - name: tatuador_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Tattoo artist's profile
      404:
        description: Tattoo artist not found
    """
    tatuador = Tatuador.query.get_or_404(tatuador_id)

    telefones = [
        telefone.numero for telefone in tatuador.telefones
    ]

    publicacoes = [
        {
            "id": publicacao.id_publicacao,
            "titulo": publicacao.titulo,
            "data_publicacao": publicacao.data_publicacao.isoformat(),
            "descricao": publicacao.descricao
        }
        for publicacao in tatuador.publicacoes
    ]

    result = {
        "id": tatuador.id_tatuador,
        "nome": tatuador.nome,
        "cidade": tatuador.cidade,
        "descricao": tatuador.descricao,
        "telefones": telefones,
        "publicacoes": publicacoes
    }

    return jsonify(result), 200

@tatuador_bp.route("/<int:tatuador_id>/feedback", methods=["GET"])
def get_tatuador_feedback(tatuador_id):
    """
    Gets a tattoo artist's feedback.
    ---
    parameters:
      - name: tatuador_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Tattoo artist's feedback
      404:
        description: Tattoo artist not found
    """
    tatuador = Tatuador.query.get_or_404(tatuador_id)

    feedbacks = Feedback.query.filter_by(id_tatuador=tatuador.id_tatuador).all()

    results = [
        {
            "id": feedback.id_feedback,
            "titulo": feedback.titulo,
            "data_publicacao": feedback.data_publicacao.isoformat(),
            "descricao": feedback.descricao,
            "nota_avaliativa": feedback.nota_avaliativa,
            "cliente": {
                "id": feedback.cliente.id_cliente,
                "nome": feedback.cliente.nome
            }
        }
        for feedback in feedbacks
    ]

    return jsonify(results), 200

@tatuador_bp.route("/search", methods=["GET"])
def search_tatuador():
    """
    Searches for tattoo artists.
    ---
    parameters:
      - name: nome
        in: query
        type: string
      - name: cidade
        in: query
        type: string
      - name: descricao
        in: query
        type: string
    responses:
      200:
        description: A list of tattoo artists
    """
    nome = request.args.get("nome")
    cidade = request.args.get("cidade")
    descricao = request.args.get("descricao")

    query = Tatuador.query

    if nome:
        query = query.filter(Tatuador.nome.ilike(f"%{nome}%"))
    
    if cidade:
        query = query.filter(Tatuador.cidade.ilike(f"%{cidade}%"))

    if descricao:
        query = query.filter(Tatuador.descricao.ilike(f"%{descricao}%"))

    tatuadores = query.all()

    results = [
        {
            "id": tatuador.id_tatuador,
            "nome": tatuador.nome,
            "cidade": tatuador.cidade,
            "descricao": tatuador.descricao
        }
        for tatuador in tatuadores
    ]

    return jsonify(results), 200

@tatuador_bp.route("/<int:tatuador_id>/edit", methods=["PUT"])
@jwt_required()
def edit_tatuador(tatuador_id):
    """
    Edits a tattoo artist's profile.
    ---
    parameters:
      - name: tatuador_id
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
            nome:
              type: string
            cidade:
              type: string
            descricao:
              type: string
    responses:
      200:
        description: Profile updated successfully
      400:
        description: Invalid data
      401:
        description: Unauthorized
      403:
        description: Forbidden
      404:
        description: Tattoo artist not found
    """
    current_user_id = get_jwt_identity()
    tatuador = Tatuador.query.get_or_404(tatuador_id)

    if tatuador.id_usuario != current_user_id:
        return jsonify({"error": "Não autorizado"}), 403

    data = request.json

    if not data:
        return jsonify({"error": "Dados inválidos"}), 400

    if "nome" in data:
        tatuador.nome = data["nome"]
    
    if "cidade" in data:
        tatuador.cidade = data["cidade"]

    if "descricao" in data:
        tatuador.descricao = data["descricao"]

    db.session.commit()

    return jsonify({"message": "Perfil atualizado com sucesso!"}), 200

@tatuador_bp.route("/<int:tatuador_id>/telefone", methods=["POST"])
@jwt_required()
def add_telefone_tatuador(tatuador_id):
    """
    Adds a phone number to a tattoo artist's profile.
    ---
    parameters:
      - name: tatuador_id
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
            numero:
              type: string
    responses:
      201:
        description: Phone number added successfully
      400:
        description: Invalid phone number
      401:
        description: Unauthorized
      403:
        description: Forbidden
      404:
        description: Tattoo artist not found
    """
    current_user_id = get_jwt_identity()
    tatuador = Tatuador.query.get_or_404(tatuador_id)

    if tatuador.id_usuario != current_user_id:
        return jsonify({"error": "Não autorizado"}), 403

    data = request.json

    if not data or not data.get("numero"):
        return jsonify({"error": "Número de telefone inválido"}), 400

    telefone = TelefoneTatuador(id_tatuador=tatuador.id_tatuador, numero=data["numero"])
    db.session.add(telefone)
    db.session.commit()

    return jsonify({"message": "Telefone adicionado com sucesso!"}), 201

@tatuador_bp.route("/<int:tatuador_id>/telefone/<string:numero>", methods=["DELETE"])
@jwt_required()
def delete_telefone_tatuador(tatuador_id, numero):
    """
    Deletes a phone number from a tattoo artist's profile.
    ---
    parameters:
      - name: tatuador_id
        in: path
        type: integer
        required: true
      - name: numero
        in: path
        type: string
        required: true
      - name: Authorization
        in: header
        type: string
        required: true
        description: Bearer token
    responses:
      200:
        description: Phone number deleted successfully
      401:
        description: Unauthorized
      403:
        description: Forbidden
      404:
        description: Tattoo artist or phone number not found
    """
    current_user_id = get_jwt_identity()
    tatuador = Tatuador.query.get_or_404(tatuador_id)

    if tatuador.id_usuario != current_user_id:
        return jsonify({"error": "Não autorizado"}), 403

    telefone = TelefoneTatuador.query.filter_by(id_tatuador=tatuador_id, numero=numero).first_or_404()
    db.session.delete(telefone)
    db.session.commit()

    return jsonify({"message": "Telefone removido com sucesso!"}), 200
