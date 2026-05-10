import hashlib
import psycopg2
import os
from datetime import datetime
from dotenv import load_dotenv


load_dotenv()


def conectar_banco():
    conexao = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        database=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD")
    )

    return conexao


def gerar_hash_arquivo(caminho_arquivo):
    sha256 = hashlib.sha256()

    with open(caminho_arquivo, "rb") as arquivo:
        for byte in iter(lambda: arquivo.read(4096), b""):
            sha256.update(byte)

    return sha256.hexdigest()


def salvar_hash_no_banco(caminho_arquivo, hash_gerado):
    conexao = conectar_banco()
    cursor = conexao.cursor()

    comando_sql = """
        INSERT INTO hashes (path, hash, data_criacao)
        VALUES (%s, %s, %s);
    """

    cursor.execute(
        comando_sql,
        (
            caminho_arquivo,
            hash_gerado,
            datetime.now()
        )
    )

    conexao.commit()

    cursor.close()
    conexao.close()


arquivo = "teste.txt"

hash_gerado = gerar_hash_arquivo(arquivo)

print("Hash gerado:")
print(hash_gerado)

salvar_hash_no_banco(arquivo, hash_gerado)

print("Hash salvo no banco com sucesso!")