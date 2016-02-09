from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
from kivy.uix.label import Label

from pyoram.crypto.aes_crypto import AESCrypto
from pyoram.crypto.keyfile import KeyFile
from pyoram.exceptions import WrongPassword


class SignupScreen(Screen):
    Builder.load_file('gui/signupscreen.kv')

    def text(self, pw, repw):
        if pw == repw and (pw and repw):
            key_file = AESCrypto.create_keys(pw)
            key_file.save_to_file()
            self.manager.current = 'login'
        elif not pw and not repw:
            popup = Popup(title='Empty password', content=Label(text='Password cannot be empty'),
                          size_hint=(None, None), size=(200, 200))
            popup.open()
        else:
            popup = Popup(title='Re-enter passwords', content=Label(text='Passwords do not match'),
                          size_hint=(None, None), size=(200, 200))
            popup.open()


class LoginScreen(Screen):
    Builder.load_file('gui/loginscreen.kv')

    def verify(self, pw):
        key_file = KeyFile.load_from_file()
        try:
            aes_crypto = AESCrypto(key_file, pw)
            # TODO: save aes_crypto as global variable, so it can be used in the main screen
            self.manager.current = 'main'
        except WrongPassword as err:
            popup = Popup(title='Wrong password', content=Label(text=err.__str__()),
                          size_hint=(None, None), size=(200, 200))
            popup.open()


class MainScreen(Screen):
    Builder.load_file('gui/mainscreen.kv')
    """ TODO: file chooser button and show data tree, create stash,
     oram function, splitting file, encrypting and decrypting file"""
