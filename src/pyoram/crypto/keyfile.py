import json
import data

from pyoram import utils
from pyoram.exceptions import ErrorInKeyMap

JSON_SALT = 'salt'
JSON_WAES_KEY = 'waes_key'
JSON_WMAC_KEY = 'wmac_key'


class KeyFile(object):

    def __init__(self, salt, waes_key, wmac_key):
        self.salt = salt
        self.waes_key = waes_key
        self.wmac_key = wmac_key

    def save_to_file(self):
        key_map = data.open_data_file(utils.KEY_MAP_FILE_NAME, utils.WRITE_MODE)
        salt = self.byte_to_str(self.salt)
        waes_key = self.byte_to_str(self.waes_key)
        wmac_key = self.byte_to_str(self.wmac_key)
        key_map.write(json.dumps({JSON_SALT:  salt, JSON_WAES_KEY: waes_key, JSON_WMAC_KEY: wmac_key}, sort_keys=True))
        key_map.close()

    @classmethod
    def load_from_file(cls):
        key_map = data.open_data_file(utils.KEY_MAP_FILE_NAME, utils.READ_MODE)
        try:
            json_key_map = json.load(key_map)
            salt = cls.str_to_byte(json_key_map[JSON_SALT])
            waes_key = cls.str_to_byte(json_key_map[JSON_WAES_KEY])
            wmac_key = cls.str_to_byte(json_key_map[JSON_WMAC_KEY])
            key_file = KeyFile(salt, waes_key, wmac_key)
            return key_file
        except(ValueError, KeyError):
            raise ErrorInKeyMap('key.map might be empty or the data is not a valid JSON format.')
        finally:
            key_map.close()

    @classmethod
    def verify_content(cls):
        try:
            cls.load_from_file()
            return True
        except ErrorInKeyMap:
            return False

    @classmethod
    def byte_to_str(cls, att):
        return att.decode()

    @classmethod
    def str_to_byte(cls, att):
        return att.encode()
