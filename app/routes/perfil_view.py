import os
from werkzeug.utils import secure_filename
from app.db import execute_query, fetch_one
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

perfil_bp = Blueprint("perfil", __name__, url_prefix="/api/perfil")

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@perfil_bp.route("/", methods=["GET", "POST"])
@jwt_required()
def profile():
    """
    Gets or updates the profile of the current user, including styles and phones for tattoo artists.
    """
    current_user_id = get_jwt_identity()
    claims = get_jwt()
    role = claims.get('role')

    if request.method == "POST":
        # --- Update Logic ---
        data = request.form
        
        # Handle photo upload
        if 'photo' in request.files:
            file = request.files['photo']
            if file and allowed_file(file.filename):
                upload_folder = current_app.config['UPLOAD_FOLDER']
                filename = secure_filename(file.filename)
                if not os.path.exists(upload_folder):
                    os.makedirs(upload_folder)
                file.save(os.path.join(upload_folder, filename))
                
                photo_url = f'{upload_folder}/{filename}'.replace("\\", "/")
                
                table = 'cliente' if role == 'cliente' else 'tatuador'
                query_update_photo = f"UPDATE {table} SET foto_url = %s WHERE id_usuario = %s"
                execute_query(query_update_photo, (photo_url, current_user_id))

        # Handle text fields update
        update_fields = []
        params = []

        if "nome" in data:
            update_fields.append("nome = %s")
            params.append(data.get("nome"))
        if "cidade" in data:
            update_fields.append("cidade = %s")
            params.append(data.get("cidade"))
        if role == 'tatuador' and "descricao" in data:
            update_fields.append("descricao = %s")
            params.append(data.get("descricao"))

        if update_fields:
            params.append(current_user_id)
            table = 'cliente' if role == 'cliente' else 'tatuador'
            query_update = f"UPDATE {table} SET {', '.join(update_fields)} WHERE id_usuario = %s"
            execute_query(query_update, tuple(params))
        
        # Handle email update
        if data.get("email"):
            query_update_user = "UPDATE usuario SET email = %s WHERE id = %s"
            execute_query(query_update_user, (data.get("email"), current_user_id))

        # Handle styles and phones for tattoo artists
        if role == 'tatuador':
            tatuador_info = fetch_one("SELECT id_tatuador FROM tatuador WHERE id_usuario = %s", (current_user_id,))
            if tatuador_info:
                id_tatuador = tatuador_info['id_tatuador']
                
                # Update styles
                if 'estilos' in data:
                    execute_query("DELETE FROM estilo_tatuador WHERE id_tatuador = %s", (id_tatuador,))
                    style_names = [s.strip() for s in data.get('estilos', '').split(',') if s.strip()]
                    if style_names:
                        style_ids = []
                        for name in style_names:
                            execute_query("INSERT IGNORE INTO estilo (nome) VALUES (%s)", (name,))
                            style_info = fetch_one("SELECT id FROM estilo WHERE nome = %s", (name,))
                            if style_info: style_ids.append(style_info['id'])
                        
                        if style_ids:
                            style_values = [(id_tatuador, sid) for sid in style_ids]
                            for val_pair in style_values:
                                execute_query("INSERT INTO estilo_tatuador (id_tatuador, id_estilo) VALUES (%s, %s)", val_pair)

                # Update phones
                if 'telefones' in data:
                    execute_query("DELETE FROM telefone_tatuador WHERE id_tatuador = %s", (id_tatuador,))
                    phone_numbers = [p.strip() for p in data.get('telefones', '').split(',') if p.strip()]
                    if phone_numbers:
                        phone_values = [(id_tatuador, num) for num in phone_numbers]
                        for val_pair in phone_values:
                            execute_query("INSERT INTO telefone_tatuador (id_tatuador, numero) VALUES (%s, %s)", val_pair)


    # --- Fetch Logic (for both GET and after POST) ---
    if role == 'cliente':
        query = "SELECT 'cliente' as role, c.id_cliente as id, c.nome, c.cidade, u.email, c.foto_url FROM cliente c JOIN usuario u ON c.id_usuario = u.id WHERE c.id_usuario = %s"
        user_profile = fetch_one(query, (current_user_id,))
    else: # tatuador
        query = """
            SELECT 
                'tatuador' as role, 
                t.id_tatuador as id, 
                t.nome, 
                t.cidade, 
                u.email, 
                t.foto_url, 
                t.descricao,
                GROUP_CONCAT(DISTINCT e.nome SEPARATOR ', ') as estilos,
                GROUP_CONCAT(DISTINCT tt.numero SEPARATOR ', ') as telefones
            FROM tatuador t
            JOIN usuario u ON t.id_usuario = u.id
            LEFT JOIN estilo_tatuador te ON t.id_tatuador = te.id_tatuador
            LEFT JOIN estilo e ON te.id_estilo = e.id
            LEFT JOIN telefone_tatuador tt ON t.id_tatuador = tt.id_tatuador
            WHERE t.id_usuario = %s
            GROUP BY t.id_tatuador, u.id, u.email, t.nome, t.cidade, t.foto_url, t.descricao
        """
        user_profile = fetch_one(query, (current_user_id,))

    if not user_profile:
        return jsonify({"error": "Usuário não encontrado"}), 404
    
    return jsonify(user_profile), 200
