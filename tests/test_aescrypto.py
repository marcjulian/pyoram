from unittest import TestCase

from pyoram.exceptions import WrongPassword
from pyoram.crypto.aes_crypto import AESCrypto, InvalidToken


class TestAESCrypto(TestCase):
    def test_encrypt_decrypt(self):
        text = b"A very very secret message."
        password = 'Blubb1234'

        key_file = AESCrypto.create_keys(password)

        aes_crypto = AESCrypto(key_file, password)
        ciphertext = aes_crypto.encrypt(text)
        assert text != ciphertext

        plaintext = aes_crypto.decrypt(ciphertext)
        assert text == plaintext

    def test_encryption_input_error(self):
        text = "Spr scrt mssg, dnt tll nyn."
        password = '1234Secure'

        key_file = AESCrypto.create_keys(password)
        aes_crypto = AESCrypto(key_file, password)

        try:
            aes_crypto.encrypt(text)
            assert False
        except TypeError:
            assert True

    def test_decryption_error(self):
        text = b"Spr scrt mssg, dnt tll nyn."
        password = '1234Secure'

        key_file = AESCrypto.create_keys(password)
        aes_crypto = AESCrypto(key_file, password)

        ciphertext = aes_crypto.encrypt(text)
        try:
            aes_crypto.decrypt(ciphertext[10:50])
            assert False
        except InvalidToken:
            assert True

    def test_password(self):
        password = 'SIIT2016'

        key_file = AESCrypto.create_keys(password)
        try:
            AESCrypto(key_file, password)
            assert True
        except WrongPassword:
            assert False

    def test_wrong_password(self):
        password = 'SecretPassword'

        key_file = AESCrypto.create_keys(password)
        wrong_password = "Forgot the password"
        try:
            AESCrypto(key_file, wrong_password)
            assert False
        except WrongPassword:
            assert True
