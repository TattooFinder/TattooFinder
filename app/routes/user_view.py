from app.db import execute_query, fetch_one
from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, unset_jwt_cookies, set_access_cookies

user_bp = Blueprint("user", __name__, url_prefix="/api")

@user_bp.route("/logout", methods=["POST"])
def logout():
    """
    Logs a user out by unsetting the JWT cookie.
    """
    response = jsonify({"message": "Logout bem-sucedido!"})
    unset_jwt_cookies(response)
    return response


@user_bp.route("/profile", methods=["GET", "POST"])
@jwt_required()
def profile():
    """
    Gets or updates the profile of the current user.
    """
    current_user_id = get_jwt_identity()
    print(f"--- /api/profile endpoint ---")
    print(f"User ID from JWT: {current_user_id}")
    print(f"Request Method: {request.method}")

    if request.method == "POST":
        data = request.get_json()
        if not data.get("nome") or not data.get("cidade"):
            return jsonify({"error": "Nome e cidade são obrigatórios"}), 400
        print(f"POST data received: {data}")
        
        query_cliente_check = "SELECT id_cliente FROM cliente WHERE id_usuario = %s"
        is_cliente = fetch_one(query_cliente_check, (current_user_id,))
        print(f"Checking for 'cliente': {is_cliente}")
        
        if is_cliente:
            print("User identified as 'cliente'. Preparing to update.")
            query_update = "UPDATE cliente SET nome = %s, cidade = %s WHERE id_usuario = %s"
            params = (data.get("nome"), data.get("cidade"), current_user_id)
            print(f"Executing update for cliente with params: {params}")
            execute_query(query_update, params)
            
            if data.get("email"):
                print("Email found in data. Preparing to update 'usuario' table.")
                query_update_user = "UPDATE usuario SET email = %s WHERE id = %s"
                execute_query(query_update_user, (data.get("email"), current_user_id))
            print("Update for 'cliente' complete.")
        else:
            print("User is not 'cliente'. Checking for 'tatuador'.")
            query_tatuador_check = "SELECT id_tatuador FROM tatuador WHERE id_usuario = %s"
            is_tatuador = fetch_one(query_tatuador_check, (current_user_id,))
            print(f"Checking for 'tatuador': {is_tatuador}")

            if is_tatuador:
                print("User identified as 'tatuador'. Preparing to update.")
                query_update = "UPDATE tatuador SET nome = %s, cidade = %s WHERE id_usuario = %s"
                params = (data.get("nome"), data.get("cidade"), current_user_id)
                print(f"Executing update for tatuador with params: {params}")
                execute_query(query_update, params)
                
                if data.get("email"):
                    print("Email found in data. Preparing to update 'usuario' table.")
                    query_update_user = "UPDATE usuario SET email = %s WHERE id = %s"
                    execute_query(query_update_user, (data.get("email"), current_user_id))
                print("Update for 'tatuador' complete.")
            else:
                print("User not found as 'cliente' or 'tatuador'.")
                return jsonify({"error": "Usuário não encontrado"}), 404

    print("Fetching updated profile data for response.")
    query_cliente = "SELECT 'cliente' as role, c.id_cliente as id, c.nome, c.cidade, u.email FROM cliente c JOIN usuario u ON c.id_usuario = u.id WHERE c.id_usuario = %s"
    user_profile = fetch_one(query_cliente, (current_user_id,))

    if not user_profile:
        query_tatuador = "SELECT 'tatuador' as role, t.id_tatuador as id, t.nome, t.cidade, u.email FROM tatuador t JOIN usuario u ON t.id_usuario = u.id WHERE t.id_usuario = %s"
        user_profile = fetch_one(query_tatuador, (current_user_id,))

    if not user_profile:
        print("Could not fetch profile after operation.")
        return jsonify({"error": "Usuário não encontrado após a operação"}), 404
    
    print(f"Returning profile data: {user_profile}")
    return jsonify(user_profile), 200


@user_bp.route("/login", methods=["POST"])
def login():
    """
    Logs a user in and returns a JWT token as a cookie.
    """
    data = request.json
    if not data or not data.get("email") or not data.get("senha"):
        return jsonify({"error": "Email ou senha inválidos"}), 400

    query_user = "SELECT id, senha FROM usuario WHERE email = %s"
    user = fetch_one(query_user, (data["email"],))

    if not user or not check_password_hash(user['senha'], data["senha"]):
        return jsonify({"error": "Email ou senha inválidos"}), 401

    access_token = create_access_token(identity=str(user['id']))
    response = jsonify(message="Login bem-sucedido!")
    set_access_cookies(response, access_token)
    return response

@user_bp.route("/register", methods=["POST"])
def register():
    """
    Registers a new user as a client or tattoo artist.
    """
    data = request.json

    if not data.get("nome") or not data.get("email") or not data.get("senha") or not data.get("role"):
        return jsonify({"error": "Dados inválidos"}), 400
    
    if data["role"] not in ["cliente", "tatuador"]:
        return jsonify({"error": "Role inválido"}), 400

    query_email = "SELECT id FROM usuario WHERE email = %s"
    if fetch_one(query_email, (data["email"],)):
        return jsonify({"error": "Email já cadastrado"}), 400
    
    hashed_password = generate_password_hash(data["senha"])

    query_insert_user = "INSERT INTO usuario (email, senha) VALUES (%s, %s)"
    execute_query(query_insert_user, (data["email"], hashed_password))
    
    query_user_id = "SELECT id FROM usuario WHERE email = %s"
    user = fetch_one(query_user_id, (data["email"],))
    user_id = user['id']

    if data["role"] == "cliente":
        if not data.get("cidade"):
            return jsonify({"error": "Cidade é obrigatória para clientes"}), 400
        
        query_insert_cliente = "INSERT INTO cliente (nome, cidade, id_usuario) VALUES (%s, %s, %s)"
        execute_query(query_insert_cliente, (data["nome"], data["cidade"], user_id))

    elif data["role"] == "tatuador":
        if not data.get("cidade"):
            return jsonify({"error": "Cidade é obrigatória para tatuadores"}), 400

        query_insert_tatuador = "INSERT INTO tatuador (nome, cidade, id_usuario) VALUES (%s, %s, %s)"
        execute_query(query_insert_tatuador, (data["nome"], data["cidade"], user_id))
    
    # Login automático após o cadastro
    access_token = create_access_token(identity=str(user_id))
    response = jsonify({"message": "Usuário cadastrado com sucesso!"})
    set_access_cookies(response, access_token)
    return response, 201