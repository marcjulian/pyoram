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
        with data.open_data_file(utils.KEY_MAP_FILE_NAME, utils.WRITE_MODE) as key_map:
            salt = utils.byte_to_str(self.salt)
            waes_key = utils.byte_to_str(self.waes_key)
            wmac_key = utils.byte_to_str(self.wmac_key)
            json.dump({JSON_SALT: salt, JSON_WAES_KEY: waes_key, JSON_WMAC_KEY: wmac_key}, key_map, indent=2,
                      sort_keys=True)

    @classmethod
    def load_from_file(cls):
        with data.open_data_file(utils.KEY_MAP_FILE_NAME, utils.READ_MODE) as key_map:
            try:
                json_key_map = json.load(key_map)
                salt = utils.str_to_byte(json_key_map[JSON_SALT])
                waes_key = utils.str_to_byte(json_key_map[JSON_WAES_KEY])
                wmac_key = utils.str_to_byte(json_key_map[JSON_WMAC_KEY])
                key_file = KeyFile(salt, waes_key, wmac_key)
                return key_file
            except(ValueError, KeyError):
                raise ErrorInKeyMap('key.map might be empty or the data is not a valid JSON format.')

    @classmethod
    def verify_content(cls):
        try:
            cls.load_from_file()
            return True
        except ErrorInKeyMap:
            return False
