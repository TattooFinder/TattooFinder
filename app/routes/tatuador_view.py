from app.db import fetch_all, fetch_one, execute_query
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
import os
from werkzeug.utils import secure_filename

tatuador_bp = Blueprint("tatuador", __name__, url_prefix="/tatuador")

ALLOWED_EXTENSIONS = {'png'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@tatuador_bp.route("/<int:tatuador_id>", methods=["GET"])
def get_tatuador(tatuador_id):
    """
    Gets a tattoo artist's public profile.
    """
    query = """
        SELECT 
            t.id_tatuador as id, 
            t.nome, 
            t.cidade, 
            u.email, 
            t.foto_url, 
            t.descricao,
            (SELECT GROUP_CONCAT(e.nome SEPARATOR ', ') FROM estilo e JOIN estilo_tatuador te ON e.id = te.id_estilo WHERE te.id_tatuador = t.id_tatuador) as estilos,
            (SELECT GROUP_CONCAT(tt.numero SEPARATOR ', ') FROM telefone_tatuador tt WHERE tt.id_tatuador = t.id_tatuador) as telefones
        FROM tatuador t 
        JOIN usuario u ON t.id_usuario = u.id
        WHERE t.id_tatuador = %s
        GROUP BY t.id_tatuador, u.id
    """
    tatuador = fetch_one(query, (tatuador_id,))

    if not tatuador:
        return jsonify({"error": "Tatuador não encontrado"}), 404

    return jsonify(tatuador), 200

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

    # The user ID from JWT is a string, so we convert the DB result to string for comparison
    if str(tatuador_auth['id_usuario']) != current_user_id:
        return jsonify({"error": "Não autorizado"}), 403

    data = request.form
    if not data:
        return jsonify({"error": "Dados inválidos"}), 400

    upload_folder = current_app.config['UPLOAD_FOLDER']
    if 'photo' in request.files:
        file = request.files['photo']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            if not os.path.exists(upload_folder):
                os.makedirs(upload_folder)
            file.save(os.path.join(upload_folder, filename))
            
            photo_url = f'{upload_folder}/{filename}'
            query_update_photo = "UPDATE tatuador SET foto_url = %s WHERE id_tatuador = %s"
            execute_query(query_update_photo, (photo_url, tatuador_id))

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

    if update_fields:
        query_update = f"UPDATE tatuador SET {', '.join(update_fields)} WHERE id_tatuador = %s"
        params.append(tatuador_id)
        
        execute_query(query_update, tuple(params))

    return jsonify({"message": "Perfil atualizado com sucesso!"}), 200

