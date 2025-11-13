import pymysql
from pymysql.cursors import DictCursor
import os

def get_db_connection():
    """Cria e retorna uma nova conexão com o banco de dados, usando variáveis de ambiente."""
    return pymysql.connect(
        host=os.getenv("DB_HOST", "127.0.0.1"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        database=os.getenv("DB_NAME", "tf_db"),
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
    except pymysql.MySQLError as e:

        conn.rollback()
        print(f"Erro ao executar query de modificação: {e}")
        raise
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
    except pymysql.MySQLError as e:
        print(f"Erro ao buscar todos os resultados: {e}")
        raise
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
    except pymysql.MySQLError as e:
        print(f"Erro ao buscar um resultado: {e}")
        raise
    finally:
        conn.close()


if __name__ == '__main__':
    try:

        execute_query("INSERT INTO sua_tabela (coluna1, coluna2) VALUES (%s, %s)", ('valor_a', 123))
        print("Dados inseridos com sucesso.")


        usuarios = fetch_all("SELECT * FROM sua_tabela WHERE coluna1 = %s", ('valor_a',))
        print("Resultados da busca:", usuarios)

    except ConnectionError as ce:
        print(f"Não foi possível continuar devido ao erro de conexão: {ce}")
    except Exception as e:
        print(f"Ocorreu um erro geral: {e}")