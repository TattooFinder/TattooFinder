
# Exemplo de Refatoração: SQLAlchemy para SQL Puro

# --- ANTES (usando SQLAlchemy) ---

# from app import db
# from app.models.cliente_model import Cliente
# from flask import Blueprint, request, jsonify
# from flask_jwt_extended import jwt_required, get_jwt_identity

# cliente_bp = Blueprint("cliente", __name__, url_prefix="/cliente")

# @cliente_bp.route("/<int:cliente_id>/edit", methods=["PUT"])
# @jwt_required()
# def edit_cliente_sqlalchemy(cliente_id):
#     """
#     Edita o perfil de um cliente.
#     """
#     current_user_id = get_jwt_identity()
#     cliente = Cliente.query.get_or_404(cliente_id)

#     if cliente.id_usuario != current_user_id:
#         return jsonify({"error": "Não autorizado"}), 403

#     data = request.json

#     if not data:
#         return jsonify({"error": "Dados inválidos"}), 400

#     if "nome" in data:
#         cliente.nome = data["nome"]
    
#     if "cidade" in data:
#         cliente.cidade = data["cidade"]

#     db.session.commit()

#     return jsonify({"message": "Perfil atualizado com sucesso!"}), 200

# --- DEPOIS (usando SQL Puro) ---

# from app.database import execute_query, fetch_one # Funções hipotéticas do novo módulo
# from flask import Blueprint, request, jsonify
# from flask_jwt_extended import jwt_required, get_jwt_identity

# cliente_bp_sql = Blueprint("cliente_sql", __name__, url_prefix="/cliente")

# @cliente_bp_sql.route("/<int:cliente_id>/edit", methods=["PUT"])
# @jwt_required()
# def edit_cliente_sql_puro(cliente_id):
#     """
#     Edita o perfil de um cliente usando SQL puro.
#     """
#     current_user_id = get_jwt_identity()
    
#     # 1. Verificar autorização
#     query_auth = "SELECT id_usuario FROM cliente WHERE id_cliente = %s"
#     cliente_auth = fetch_one(query_auth, (cliente_id,))
    
#     if not cliente_auth:
#         return jsonify({"error": "Cliente não encontrado"}), 404

#     if cliente_auth['id_usuario'] != current_user_id:
#         return jsonify({"error": "Não autorizado"}), 403

#     data = request.json
#     if not data:
#         return jsonify({"error": "Dados inválidos"}), 400

#     # 2. Construir e executar a query de atualização
#     update_fields = []
#     params = []
    
#     if "nome" in data:
#         update_fields.append("nome = %s")
#         params.append(data["nome"])
    
#     if "cidade" in data:
#         update_fields.append("cidade = %s")
#         params.append(data["cidade"])

#     if not update_fields:
#         return jsonify({"error": "Nenhum campo para atualizar"}), 400

#     query_update = f"UPDATE cliente SET {', '.join(update_fields)} WHERE id_cliente = %s"
#     params.append(cliente_id)
    
#     execute_query(query_update, tuple(params))

#     return jsonify({"message": "Perfil atualizado com sucesso!"}), 200
