import argparse
import os
from pathlib import Path
import sys

import psycopg2

from crypto import (
    calculate_hash,
    sign_hash,
    verify_signature
)

DB_CONFIG = {
    "host": os.getenv("POSTGRES_HOST"),
    "port": os.getenv("POSTGRES_PORT"),
    "dbname": os.getenv("POSTGRES_DB"),
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD"),
}

PGCRYPTO_PASSPHRASE = os.getenv("PGCRYPTO_PASSPHRASE", "integrity-key")


def get_connection():

    return psycopg2.connect(**DB_CONFIG)


def ensure_table(connection):

    with connection.cursor() as cursor:
        cursor.execute(
            """
            CREATE EXTENSION IF NOT EXISTS pgcrypto;

            CREATE TABLE IF NOT EXISTS hashes (
                id SERIAL PRIMARY KEY,
                path VARCHAR(255) UNIQUE NOT NULL,
                hash TEXT NOT NULL,
                signature BYTEA NOT NULL,
                data_criacao TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
    connection.commit()


def get_record(path):

    with get_connection() as connection:
        ensure_table(connection)

        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT hash, pgp_sym_decrypt(signature, %s) FROM hashes WHERE path = %s",
                (PGCRYPTO_PASSPHRASE, path)
            )
            return cursor.fetchone()


def save_record(path, file_hash, signature):

    with get_connection() as connection:
        ensure_table(connection)

        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO hashes (path, hash, signature, data_criacao)
                VALUES (%s, %s, pgp_sym_encrypt(%s, %s), CURRENT_TIMESTAMP)
                ON CONFLICT (path)
                DO UPDATE SET
                    hash = EXCLUDED.hash,
                    signature = EXCLUDED.signature,
                    data_criacao = CURRENT_TIMESTAMP
                """,
                (path, file_hash, signature, PGCRYPTO_PASSPHRASE)
            )

        connection.commit()


def init(path):

    file_hash = calculate_hash(path)

    signature = sign_hash(file_hash)

    save_record(path, file_hash, signature)

    print("Arquivo Registrado")


def check(path):

    record = get_record(path)

    if record is None:
        print("Arquivo não monitorado")
        sys.exit(3)

    stored_hash, stored_signature = record

    current_hash = calculate_hash(path)

    if current_hash == stored_hash:

        print(" Arquivo íntegro")
        sys.exit(0)

    valid_signature = verify_signature(
        stored_hash,
        stored_signature
    )

    if valid_signature:

        print("Arquivo alterado")
        sys.exit(2)

    else:

        print("Assinatura inválida")
        sys.exit(3)


def update(path):

    if Path(path).suffix.lower() == ".log":
        print("Update bloqueado para arquivos .log")
        print("Use apenas check para detectar adulteracao em logs")
        sys.exit(4)

    new_hash = calculate_hash(path)

    new_signature = sign_hash(new_hash)

    save_record(path, new_hash, new_signature)

    print("Hash atualizado")


parser = argparse.ArgumentParser()

parser.add_argument("command")
parser.add_argument("path")

args = parser.parse_args()

if args.command == "init":
    init(args.path)

elif args.command == "check":
    check(args.path)

elif args.command == "update":
    update(args.path)

else:
    print("Comando inválido")