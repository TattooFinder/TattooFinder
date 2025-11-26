import pymysql
from pymysql.cursors import DictCursor
import os
from dotenv import load_dotenv


load_dotenv()


def get_db_connection():
    try:
        return pymysql.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
            cursorclass=DictCursor
        )
    except pymysql.MySQLError as e:

        print(f"Erro ao conectar ao MySQL: {e}")

        raise ConnectionError("Não foi possível estabelecer a conexão com o banco de dados.") from e


def execute_query(query, params=None):

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