from unittest import TestCase

from pyoram.crypto.aes_crypto import AESCrypto, InvalidToken
from pyoram.exceptions import WrongPassword


class TestAESCrypto(TestCase):
    # TODO: add test for dummy data
    def test_encrypt_decrypt(self):
        text = b"A very very secret message."
        password = 'Blubb1234'
        id = 1

        key_file = AESCrypto.create_keys(password)

        aes_crypto = AESCrypto(key_file, password)
        token = aes_crypto.encrypt(text, id)
        assert text != token

        data_id, data = aes_crypto.decrypt(token)
        assert id == data_id
        assert text == data

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

        ciphertext = aes_crypto.encrypt(text, 5)
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
