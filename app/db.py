import pymysql
from pymysql.cursors import DictCursor

def get_db_connection():
    """Cria e retorna uma nova conexão com o banco de dados."""
    return pymysql.connect(
        host="127.0.0.1",
        user="root",
        password="",
        database="tf_db",
        cursorclass=DictCursor
    )

def execute_query(query, params=None):
    """
    Executa uma query que não retorna resultados (INSERT, UPDATE, DELETE).
    """
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(query, params)
        conn.commit()
    finally:
        conn.close()

def fetch_all(query, params=None):
    """
    Executa uma query e retorna todos os resultados.
    """
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(query, params)
            return cursor.fetchall()
    finally:
        conn.close()

def fetch_one(query, params=None):
    """
    Executa uma query e retorna o primeiro resultado.
    """
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(query, params)
            return cursor.fetchone()
    finally:
        conn.close()
