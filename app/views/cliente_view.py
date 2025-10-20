from app import db
from app.models.cliente_model import Cliente
from app.models.telefone_cliente_model import TelefoneCliente
from flask import Blueprint, request, jsonify

cliente_bp = Blueprint("cliente", __name__, url_prefix="/cliente")

@cliente_bp.route("/<int:cliente_id>/edit", methods=["PUT"])
def edit_cliente(cliente_id):
    cliente = Cliente.query.get_or_404(cliente_id)
    data = request.json

    if not data:
        return jsonify({"error": "Dados inválidos"}), 400

    if "nome" in data:
        cliente.nome = data["nome"]
    
    if "cidade" in data:
        cliente.cidade = data["cidade"]

    db.session.commit()

    return jsonify({"message": "Perfil atualizado com sucesso!"}), 200

@cliente_bp.route("/<int:cliente_id>/telefone", methods=["POST"])
def add_telefone_cliente(cliente_id):
    cliente = Cliente.query.get_or_404(cliente_id)
    data = request.json

    if not data or not data.get("numero"):
        return jsonify({"error": "Número de telefone inválido"}), 400

    telefone = TelefoneCliente(id_cliente=cliente.id_cliente, numero=data["numero"])
    db.session.add(telefone)
    db.session.commit()

    return jsonify({"message": "Telefone adicionado com sucesso!"}), 201

@cliente_bp.route("/<int:cliente_id>/telefone/<string:numero>", methods=["DELETE"])
def delete_telefone_cliente(cliente_id, numero):
    telefone = TelefoneCliente.query.filter_by(id_cliente=cliente_id, numero=numero).first_or_404()
    db.session.delete(telefone)
    db.session.commit()

    return jsonify({"message": "Telefone removido com sucesso!"}), 200
