import os
import base64

from unittest import TestCase

from pyoram.exceptions import WrongPassword
from pyoram.crypto.aes_crypto import AESCrypto, InvalidToken


class TestAESCrypto(TestCase):
    def test_encrypt_decrypt(self):
        text = b"A very very secret message."
        password = 'Blubb1234'

        key_file = AESCrypto.create_keys(password)

        aes_crypto = AESCrypto(key_file, password)
        ciphertext, iv, hmac = aes_crypto.encrypt(text, 1)
        assert text != ciphertext

        plaintext = aes_crypto.decrypt(ciphertext, iv, hmac)
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

        ciphertext, iv, hmac = aes_crypto.encrypt(text, 5)
        try:
            aes_crypto.decrypt(ciphertext[10:50], iv, hmac)
            assert False
        except InvalidToken:
            assert True

    def test_retrieve_data_id(self):
        text = b'5 days weekend would be awesome!'
        password = 'supersecure'
        dataIDs = [1, 10, 759, 4578, 92134, 257192, 8194235, 53827461]

        key_file = AESCrypto.create_keys(password)
        aes_crypto = AESCrypto(key_file, password)
        for dataID in dataIDs:
            ciphertext, iv, hmac = aes_crypto.encrypt(text, dataID)
            actual_data_id = aes_crypto.retrieve_data_id(ciphertext)
            assert dataID == actual_data_id

    def test_retrieve_data_id_from_dummy_data(self):
        dummy_data = b'Nm1tQ1NsYVVpRXJlS2h5c253cW1zT2d5c20yVG9rMEl4dTNiaGo5SXBnbWx3MER5UkVOTHY5SnpHRDFBNU42SlpzTGJJSGQ3SUZLdnM0dTB2M0pnbWt0NTlRTmRDdjl2V3Znd0NYNHpwN1NqendMdzhaV1l6M3JkNXdFNWRnSEZicFFhSnRZakp3ZWl2Qk9lcmtFRUZibmwwU1VSNDE1cnVXSDR4T3RLUVFWTGMySUg0UjRYbUw5UlZDQVJHVk9PcVpkbHZMYk5MOW1XMkhUbk5Sc3h4eTBVUEg4dmYzMk1DUHM4cWJkVlNsRUZOREpScFh3SmxPMllFWVV2ZERRb1ZKa3BjOElzSVo2MlVWaGtkY3NLSkNOc1RoMTJWSTlKSGJSa1FUNnR0ZnM5R3JDcmFBZlo0ZDM4a09GUmJHNXh5VVlJNWJnODMwSmIyUHI4MnZjMmx5RlVLd1VvM1BrbFhNMTRiZXJOb3lYbXE0QjRMWGg1ZjdESVJXeE1nUlUwNVN2M3Y4cHRRb1gyd2xPU1FEWVJuUVZpZzdMNkNDMVdZVFd6T21xUm5SYmxRVTdzS3VqV0tQUFFNajlESjlJV0oxNVo4d0txMExmU2llejU4Z0xteUI5cVZHc2ZPbmdyd21iVHgxUXFsQjhiTGEzV25rSnNSYkxZTWY5eWl1V1Z6emprNkx2ZVdLWUoxOEdDVFVGYkJwc2plUUF4WFdpcld4ZkJNVmlrYXUwSVZmUVN4TEU5azJyd2xUNzRiWmx3UVFOQkU2eGR4THZ3UXJNTEI4TEVPYURaSjFMV29LZTNHSmdqR29FcG15ZXlITWJWczRoTEM2Z1M1TEt1ZnVKaGVvV1pHeFhoZTNCV1hTNDk5Y05KaDlJSkRPcndxVHh0NFlwU3JzNDNMTXU4V0JlNmtpN2pRY3laZGFqMWs4UzI1a1JzZUl4YVh5cXhmWlgyVlA3cEJlaXB4STEyZERHVzd2N2NiWElEWWFQNTdR'
        password = 'BestPasswordEver'

        key_file = AESCrypto.create_keys(password)
        aes_crypto = AESCrypto(key_file, password)

        # TODO: expect to fail, maybe dummy_data needs to be string or dataid added to identify dummy data
        data_id = aes_crypto.retrieve_data_id(dummy_data)

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
