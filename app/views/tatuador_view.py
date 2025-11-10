from app.db import fetch_all, fetch_one, execute_query
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

tatuador_bp = Blueprint("tatuador", __name__, url_prefix="/tatuador")

@tatuador_bp.route("/<int:tatuador_id>", methods=["GET"])
def get_tatuador(tatuador_id):
    """
    Gets a tattoo artist's profile.
    """
    query_tatuador = "SELECT id_tatuador, nome, cidade, descricao FROM tatuador WHERE id_tatuador = %s"
    tatuador = fetch_one(query_tatuador, (tatuador_id,))

    if not tatuador:
        return jsonify({"error": "Tatuador não encontrado"}), 404

    query_telefones = "SELECT numero FROM telefone_tatuador WHERE id_tatuador = %s"
    telefones = fetch_all(query_telefones, (tatuador_id,))
    tatuador['telefones'] = [tel['numero'] for tel in telefones]

    query_publicacoes = "SELECT id_publicacao, titulo, data_publicacao, descricao FROM publicacao WHERE id_tatuador = %s"
    publicacoes = fetch_all(query_publicacoes, (tatuador_id,))
    tatuador['publicacoes'] = publicacoes

    return jsonify(tatuador), 200

@tatuador_bp.route("/<int:tatuador_id>/feedback", methods=["GET"])
def get_tatuador_feedback(tatuador_id):
    """
    Gets a tattoo artist's feedback.
    """
    query_tatuador = "SELECT id_tatuador FROM tatuador WHERE id_tatuador = %s"
    if not fetch_one(query_tatuador, (tatuador_id,)):
        return jsonify({"error": "Tatuador não encontrado"}), 404

    query = """
        SELECT f.id_feedback, f.titulo, f.data_publicacao, f.descricao, f.nota_avaliativa, c.id_cliente, c.nome AS cliente_nome
        FROM feedback f
        JOIN cliente c ON f.id_cliente = c.id_cliente
        WHERE f.id_tatuador = %s
    """
    feedbacks = fetch_all(query, (tatuador_id,))

    results = [
        {
            "id": feedback['id_feedback'],
            "titulo": feedback['titulo'],
            "data_publicacao": feedback['data_publicacao'].isoformat(),
            "descricao": feedback['descricao'],
            "nota_avaliativa": feedback['nota_avaliativa'],
            "cliente": {
                "id": feedback['id_cliente'],
                "nome": feedback['cliente_nome']
            }
        }
        for feedback in feedbacks
    ]

    return jsonify(results), 200

@tatuador_bp.route("/search", methods=["GET"])
def search_tatuador():
    """
    Searches for tattoo artists.
    """
    nome = request.args.get("nome")
    cidade = request.args.get("cidade")
    descricao = request.args.get("descricao")

    query = "SELECT id_tatuador, nome, cidade, descricao FROM tatuador WHERE 1=1"
    params = []

    if nome:
        query += " AND nome LIKE %s"
        params.append(f"%{nome}%")
    
    if cidade:
        query += " AND cidade LIKE %s"
        params.append(f"%{cidade}%")

    if descricao:
        query += " AND descricao LIKE %s"
        params.append(f"%{descricao}%")

    tatuadores = fetch_all(query, tuple(params))

    return jsonify(tatuadores), 200

@tatuador_bp.route("/<int:tatuador_id>/edit", methods=["PUT"])
@jwt_required()
def edit_tatuador(tatuador_id):
    """
    Edits a tattoo artist's profile.
    """
    current_user_id = get_jwt_identity()
    
    query_auth = "SELECT id_usuario FROM tatuador WHERE id_tatuador = %s"
    tatuador_auth = fetch_one(query_auth, (tatuador_id,))
    
    if not tatuador_auth:
        return jsonify({"error": "Tatuador não encontrado"}), 404

    if tatuador_auth['id_usuario'] != current_user_id:
        return jsonify({"error": "Não autorizado"}), 403

    data = request.json
    if not data:
        return jsonify({"error": "Dados inválidos"}), 400

    update_fields = []
    params = []
    
    if "nome" in data:
        update_fields.append("nome = %s")
        params.append(data["nome"])
    
    if "cidade" in data:
        update_fields.append("cidade = %s")
        params.append(data["cidade"])

    if "descricao" in data:
        update_fields.append("descricao = %s")
        params.append(data["descricao"])

    if not update_fields:
        return jsonify({"error": "Nenhum campo para atualizar"}), 400

    query_update = f"UPDATE tatuador SET {', '.join(update_fields)} WHERE id_tatuador = %s"
    params.append(tatuador_id)
    
    execute_query(query_update, tuple(params))

    return jsonify({"message": "Perfil atualizado com sucesso!"}), 200

@tatuador_bp.route("/<int:tatuador_id>/telefone", methods=["POST"])
@jwt_required()
def add_telefone_tatuador(tatuador_id):
    """
    Adds a phone number to a tattoo artist's profile.
    """
    current_user_id = get_jwt_identity()
    
    query_auth = "SELECT id_usuario FROM tatuador WHERE id_tatuador = %s"
    tatuador_auth = fetch_one(query_auth, (tatuador_id,))

    if not tatuador_auth:
        return jsonify({"error": "Tatuador não encontrado"}), 404

    if tatuador_auth['id_usuario'] != current_user_id:
        return jsonify({"error": "Não autorizado"}), 403

    data = request.json

    if not data or not data.get("numero"):
        return jsonify({"error": "Número de telefone inválido"}), 400

    query_insert = "INSERT INTO telefone_tatuador (id_tatuador, numero) VALUES (%s, %s)"
    execute_query(query_insert, (tatuador_id, data["numero"]))

    return jsonify({"message": "Telefone adicionado com sucesso!"}), 201

@tatuador_bp.route("/<int:tatuador_id>/telefone/<string:numero>", methods=["DELETE"])
@jwt_required()
def delete_telefone_tatuador(tatuador_id, numero):
    """
    Deletes a phone number from a tattoo artist's profile.
    """
    current_user_id = get_jwt_identity()
    
    query_auth = "SELECT id_usuario FROM tatuador WHERE id_tatuador = %s"
    tatuador_auth = fetch_one(query_auth, (tatuador_id,))

    if not tatuador_auth:
        return jsonify({"error": "Tatuador não encontrado"}), 404

    if tatuador_auth['id_usuario'] != current_user_id:
        return jsonify({"error": "Não autorizado"}), 403

    query_delete = "DELETE FROM telefone_tatuador WHERE id_tatuador = %s AND numero = %s"
    execute_query(query_delete, (tatuador_id, numero))

    return jsonify({"message": "Telefone removido com sucesso!"}), 200