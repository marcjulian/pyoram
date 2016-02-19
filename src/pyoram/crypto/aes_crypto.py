import base64
import binascii
import os
import six

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.keywrap import aes_key_wrap, aes_key_unwrap, InvalidUnwrap
from cryptography.hazmat.primitives.hmac import HMAC

from pyoram.crypto.keyfile import KeyFile
from pyoram.exceptions import WrongPassword


class InvalidToken(Exception):
    # TODO: catch InvalidToken for the user to inform about the error, maybe add a text for the different invalidtokens
    pass


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
        return self.encrypt_with_hmac(data, iv)

    def encrypt_with_hmac(self, data, iv):
        if not isinstance(data, bytes):
            raise TypeError("data must be bytes.")

        # PKCS7 padding
        padder = padding.PKCS7(algorithms.AES.block_size).padder()
        padded_data = padder.update(data) + padder.finalize()
        # AES with CBC mode
        encryptor = Cipher(algorithms.AES(self.aes_key), modes.CBC(iv), backend=self.backend).encryptor()
        ciphertext = encryptor.update(padded_data) + encryptor.finalize()

        # TODO: Store iv locally, not on the server (position.map)
        # TODO: store dataID with the ciphertext (important for downloading to determine if its the actual data)
        main_parts = (
            b"\x80" + ciphertext
        )

        h = HMAC(self.mac_key, hashes.SHA256(), backend=self.backend)
        h.update(main_parts)
        hmac = h.finalize()
        # TODO: Store hmac locally, not on the server (in the position.map) to optimize the speed of the
        # transfer to the cloud
        return self.to_base64(main_parts), self.to_base64(iv), self.to_base64(hmac)

    def decrypt(self, token, iv, hmac):
        if not isinstance(token, bytes):
            raise TypeError("token must be bytes")

        try:
            data = self.from_base64(token)
            iv = self.from_base64(iv)
            hmac = self.from_base64(hmac)
        except (TypeError, binascii.Error):
            raise InvalidToken

        if not data or six.indexbytes(data, 0) != 0x80:
            raise InvalidToken

        h = HMAC(self.mac_key, hashes.SHA256(), backend=self.backend)
        h.update(data)
        try:
            h.verify(hmac)
        except InvalidSignature:
            raise InvalidToken

        ciphertext = data[1:]
        decryptor = Cipher(algorithms.AES(self.aes_key), modes.CBC(iv), self.backend).decryptor()
        plaintext_padded = decryptor.update(ciphertext)
        try:
            plaintext_padded += decryptor.finalize()
        except ValueError:
            raise InvalidToken

        unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
        plaintext = unpadder.update(plaintext_padded)
        try:
            plaintext += unpadder.finalize()
        except ValueError:
            raise InvalidToken
        return plaintext
