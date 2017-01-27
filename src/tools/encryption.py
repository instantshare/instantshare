import base64
import os

from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


class CryptoError(Exception):
    pass


def _derive_key(password: str) -> bytes:
    from tools.persistence import KVStore
    kvstore = KVStore(".encryption")
    if "salt" not in kvstore.keys():
        kvstore["salt"] = os.urandom(16)
        kvstore.sync()

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=kvstore["salt"],
        iterations=100000,
        backend=default_backend()
    )
    return base64.urlsafe_b64encode(kdf.derive(bytes(password, encoding="ascii")))


class SymmetricKey:

    def __init__(self, password):
        self.crypto = Fernet(_derive_key(password))

    def encrypt(self, data: bytes) -> bytes:
        return self.crypto.encrypt(data)

    def decrypt(self, data: bytes) -> bytes:
        try:
            return self.crypto.decrypt(data)
        except InvalidToken:
            raise CryptoError
