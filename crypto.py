import base64
import hashlib
from pathlib import Path

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.exceptions import InvalidSignature
from cryptography.fernet import Fernet


def ensure_keys():

    private_key_path = Path("private.pem")
    public_key_path = Path("public.pem")

    if private_key_path.exists() and public_key_path.exists():
        return

    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )

    public_key = private_key.public_key()

    private_key_path.write_bytes(private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    ))

    public_key_path.write_bytes(public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    ))


def ensure_storage_key():

    key_path = Path("storage.key")

    if key_path.exists():
        return

    key_path.write_bytes(Fernet.generate_key())


def load_storage_cipher():

    ensure_storage_key()

    key_path = Path("storage.key")

    return Fernet(key_path.read_bytes())


def calculate_hash(path):

    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def sign_hash(hash_str):

    ensure_keys()

    with open("private.pem", "rb") as f:

        private_key = serialization.load_pem_private_key(
            f.read(),
            password=None
        )

    signature = private_key.sign(
        hash_str.encode(),

        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),

        hashes.SHA256()
    )

    return base64.b64encode(signature).decode()


def verify_signature(hash_str, signature_b64):

    ensure_keys()

    with open("public.pem", "rb") as f:

        public_key = serialization.load_pem_public_key(
            f.read()
        )

    signature = base64.b64decode(signature_b64)

    try:

        public_key.verify(
            signature,
            hash_str.encode(),

            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),

            hashes.SHA256()
        )

        return True

    except InvalidSignature:

        return False


def encrypt_signature(signature_b64):

    cipher = load_storage_cipher()

    return cipher.encrypt(signature_b64.encode()).decode()


def decrypt_signature(encrypted_signature):

    cipher = load_storage_cipher()

    return cipher.decrypt(encrypted_signature.encode()).decode()