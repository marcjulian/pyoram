from unittest import TestCase
from pyoram.crypto.aes_crypto import AESCrypto


class TestAESCrypto(TestCase):

    def test_verify_pw(self):
        pw = 'Blubb1234'
        hashed_pw = AESCrypto.hash_pw(pw)
        print(hashed_pw)
        assert AESCrypto.verify_pw(pw, hashed_pw)

    def test_false_verify_pw(self):
        pw = 'Blubb1234'
        hashed_pw = AESCrypto.hash_pw(pw)
        pw2 = '1234Blubb'
        assert not AESCrypto.verify_pw(pw2, hashed_pw)
