import base64
import os

from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


def _derive_key(password: str) -> bytes:
    salt = bytes(os.uname())
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    return base64.urlsafe_b64encode(kdf.derive(password))


class SymmetricKey:

    def __init__(self, password):
        self.crypto = Fernet(_derive_key(password))

    def encrypt(self, data: bytes) -> bytes:
        return self.crypto.encrypt(data)

    def decrypt(self, data: bytes) -> bytes:
        return self.crypto.decrypt(data)
