from flask import Blueprint, request, jsonify
from app.db import fetch_all

search_bp = Blueprint("search", __name__, url_prefix="/api/search")

@search_bp.route("/", methods=["GET"])
def search_artists():
    """
    Searches for tattoo artists by name, style, or city with prioritization.
    Priority: Name > Style > City
    """
    query_string = request.args.get('q', '').strip()

    if not query_string:
        return jsonify([])

    # The search term will be used in multiple LIKE clauses
    search_term = f"%{query_string}%"
    
    # The query uses a CASE statement in ORDER BY to prioritize results.
    # 1 = Name match, 2 = Style match, 3 = City match
    query = """
        SELECT
            t.id_tatuador,
            t.nome,
            t.cidade,
            t.foto_url,
            GROUP_CONCAT(DISTINCT e.nome SEPARATOR ', ') as estilos
        FROM tatuador t
        LEFT JOIN estilo_tatuador et ON t.id_tatuador = et.id_tatuador
        LEFT JOIN estilo e ON et.id_estilo = e.id
        WHERE
            t.nome LIKE %s OR
            t.cidade LIKE %s OR
            e.nome LIKE %s
        GROUP BY t.id_tatuador, t.nome, t.cidade, t.foto_url
        ORDER BY
            MIN(CASE
                WHEN t.nome LIKE %s THEN 1
                WHEN e.nome LIKE %s THEN 2
                WHEN t.cidade LIKE %s THEN 3
                ELSE 4
            END),
            t.nome;
    """
    
    # We need to pass the search term for each placeholder in the query
    params = (search_term, search_term, search_term, search_term, search_term, search_term)
    
    try:
        results = fetch_all(query, params)
        return jsonify(results)
    except Exception as e:
        print(f"Error during search: {e}")
        return jsonify({"error": "An error occurred during the search."}), 500
