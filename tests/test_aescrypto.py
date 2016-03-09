from unittest import TestCase

from pyoram.crypto.aes_crypto import AESCrypto, InvalidToken, InvalidDataId
from pyoram.exceptions import WrongPassword


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
        dummy_data = b'V9OGOoo7kU8OtYh-N_ea5lQffScS8-sSMaSEITUVv82PAq6O8INU0cznZm9Y8G2i1vpnGknMlYbvOR6tXrgRAA6HsD39XonT9j6mRJdnpdkb-_EYiqdXFEAFyxZkpJjMwIZhXX-Exmp079hxg8H9NbDw5x0HyQgdrsK7XtFlPV9gCEwpgPLZyOyIqGqOWICXqJQ7kRo6ZD22sQ-VjmYq02B_vkCVmAm72Fi-eXXHIi2PKOewUZf5y_LUljhAK8RJdSDLIXs3IkYd5asZTh8noFxIwKlpHoF1-F07d3_Blmuyu8lHARaFkRs94oiQ6GioMtSkA83G8NFey7YlMBVIOX5a7QD0ddA2cCkPUMLLE3NPwfbiRnlysz7i3ZuU0EBGH_Ii_2_8HXQWPNHNJ9KMC6YYtMOf2Ch7E9mZ5m8y_YZ6bkjczkx5sLRZ3MWioR3177_eh1kbBHquAHeP6nKjBRq_hzawnU3zsi9TegC4L_nw8LVyekJDOf_6R0OSXuLklKINfO1TmLtCYXJq1nfPfozVL9fcQdQNbx9FzzE1WMU4W5ZTC6ZA7o3nfNzz0TJlVlQASzq8tfY8b78Cz4V3aCAA0CrJs_JbIRTjbYxcOu5UJW9dSSyZMMxbNojyz46fA8jG1VlVn2lbHsYVumB9L6kuDzjn4kzRitJsM5m9DuvVMUM8NVaScpPnCKcb-dWxRFXkX8SijKpSg4hVfNxY_46IhZoZP6dYROiZ5uIsmNSL5Q_s8AC5j8GoHbDbwQATVqxx_nOVjkrXKF1iXmBJ0OPA3cWrQkkfoTk19JtpmAQZXbXRHKjDu0bu5LW_EZ417vgSvSahcULFVyS8VTlhwnKIsxKH0zcjfP_Enudb3EmmNMSl8Bs7wZljf8bzwtcxhAFabbO1dKtl96JyYwgT5G6Up8NxQiv5V3KljnOWoaK7SYvhbvi40Xgwe9ALSAm82lDSPRdP0wGNZk80z_bUHGt8Hh0AAF_M81m7wA=='
        password = 'BestPasswordEver'

        key_file = AESCrypto.create_keys(password)
        aes_crypto = AESCrypto(key_file, password)

        try:
            aes_crypto.retrieve_data_id(dummy_data)
            assert False
        except InvalidDataId:
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
