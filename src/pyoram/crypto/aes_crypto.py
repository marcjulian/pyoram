"""
Cipher: AES with CBC mode
HMAC SHA-512
"""
import base64
import os

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.keywrap import aes_key_wrap, aes_key_unwrap, InvalidUnwrap
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from pyoram.crypto.keyfile import KeyFile
from pyoram.exceptions import WrongPassword


class AESCrypto(object):

    def __init__(self, key_file, pw, backend=None):
        if backend is None:
            backend = default_backend()

        salt = self.from_base64(key_file.salt)
        waes_key = self.from_base64(key_file.waes_key)
        wmac_key = self.from_base64(key_file.wmac_key)
        if len(salt) != 16:
            raise ValueError(
                "Master key salt must be 16 url-safe base64-encoded bytes."
            )

        master_key = self.generate_key(pw, salt)
        self.aes_key = self.unwrap_key(master_key, waes_key)
        self.mac_key = self.unwrap_key(master_key, wmac_key)
        self.backend = backend
        if len(self.aes_key) != 32:
            raise ValueError(
                "AES key must be 32 url-safe base64-encoded bytes."
            )

        if len(self.mac_key) != 32:
            raise ValueError(
                "Mac key must be 32 url-safe base64-encoded bytes."
            )

    @classmethod
    def to_base64(cls, att):
        return base64.urlsafe_b64encode(att)

    @classmethod
    def from_base64(cls, att):
        return base64.urlsafe_b64decode(att)

    @classmethod
    def generate_key(cls, password, salt):
        kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=100000, backend=default_backend())
        return kdf.derive(password.encode())

    @classmethod
    def generate_random_key(cls):
        return os.urandom(32)

    @classmethod
    def wrap_key(cls, wrapping_key, key_to_wrap):
        return aes_key_wrap(wrapping_key, key_to_wrap, default_backend())

    @classmethod
    def create_keys(cls, pw):
        salt = os.urandom(16)
        master_key = cls.generate_key(pw, salt)

        aes_key = cls.generate_random_key()
        mac_key = cls.generate_random_key()

        wrapped_aes_key = cls.wrap_key(master_key, aes_key)
        wrapped_mac_key = cls.wrap_key(master_key, mac_key)

        return KeyFile(cls.to_base64(salt), cls.to_base64(wrapped_aes_key), cls.to_base64(wrapped_mac_key))

    def unwrap_key(self, wrapping_key, key_to_unwrap):
        try:
            return aes_key_unwrap(wrapping_key, key_to_unwrap, default_backend())
        except InvalidUnwrap:
            raise WrongPassword("Password is incorrect.")


    def encrypt(self, data):
        iv = os.urandom(16)
        # TODO: save IV in the position map
        return 0

    def decrypt(self, data):
        return 0
