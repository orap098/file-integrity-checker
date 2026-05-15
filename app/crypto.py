import hashlib
import base64

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.exceptions import InvalidSignature


def calculate_hash(path):

    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def sign_hash(hash_str):

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