import json
import argparse
import sys

from crypto import (
    calculate_hash,
    sign_hash,
    verify_signature
)

DB_FILE = "integrity_db.json"


def load_db():

    with open(DB_FILE, "r") as f:
        return json.load(f)


def save_db(data):

    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)


def init(path):

    db = load_db()

    file_hash = calculate_hash(path)

    signature = sign_hash(file_hash)

    db[path] = {
        "hash": file_hash,
        "signature": signature
    }

    save_db(db)

    print("Arquivo Registrado")


def check(path):

    db = load_db()

    if path not in db:
        print("Arquivo não monitorado")
        sys.exit(3)

    stored_hash = db[path]["hash"]

    stored_signature = db[path]["signature"]

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

    db = load_db()

    new_hash = calculate_hash(path)

    new_signature = sign_hash(new_hash)

    db[path] = {
        "hash": new_hash,
        "signature": new_signature
    }

    save_db(db)

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