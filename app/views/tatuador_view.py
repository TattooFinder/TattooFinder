from app import db
from app.models.tatuador_model import Tatuador
from app.models.telefone_tatuador_model import TelefoneTatuador
from app.models.publicacao_model import Publicacao
from app.models.feedback_model import Feedback
from app.models.cliente_model import Cliente
from flask import Blueprint, request, jsonify

tatuador_bp = Blueprint("tatuador", __name__, url_prefix="/tatuador")

@tatuador_bp.route("/<int:tatuador_id>", methods=["GET"])
def get_tatuador(tatuador_id):
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
    tatuador = Tatuador.query.get_or_404(tatuador_id)

    feedbacks = (
        db.session.query(Feedback)
        .join(Cliente, Cliente.id_cliente == Feedback.id_cliente)
        .filter(Cliente.id_usuario == tatuador.id_usuario)
        .all()
    )

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
def edit_tatuador(tatuador_id):
    tatuador = Tatuador.query.get_or_404(tatuador_id)
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
def add_telefone_tatuador(tatuador_id):
    tatuador = Tatuador.query.get_or_404(tatuador_id)
    data = request.json

    if not data or not data.get("numero"):
        return jsonify({"error": "Número de telefone inválido"}), 400

    telefone = TelefoneTatuador(id_tatuador=tatuador.id_tatuador, numero=data["numero"])
    db.session.add(telefone)
    db.session.commit()

    return jsonify({"message": "Telefone adicionado com sucesso!"}), 201

@tatuador_bp.route("/<int:tatuador_id>/telefone/<string:numero>", methods=["DELETE"])
def delete_telefone_tatuador(tatuador_id, numero):
    telefone = TelefoneTatuador.query.filter_by(id_tatuador=tatuador_id, numero=numero).first_or_404()
    db.session.delete(telefone)
    db.session.commit()

    return jsonify({"message": "Telefone removido com sucesso!"}), 200
