import os
import threading

from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.treeview import TreeViewLabel
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty

from pyoram.crypto.aes_crypto import AESCrypto
from pyoram.crypto.keyfile import KeyFile
from pyoram.exceptions import WrongPassword
from pyoram.core.stash import Stash
from pyoram.core.oram import PathORAM
from pyoram.core.chunk_file import ChunkFile
from pyoram import utils

AES_CRYPTO = None


class SignupScreen(Screen):
    Builder.load_file('gui/signupscreen.kv')

    def signup(self, pw, repw):
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
            global AES_CRYPTO
            AES_CRYPTO = AESCrypto(key_file, pw)
            self.manager.current = 'main'
        except WrongPassword as err:
            popup = Popup(title='Wrong password', content=Label(text=err.__str__()),
                          size_hint=(None, None), size=(200, 200))
            popup.open()


class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)


class MainScreen(Screen):
    file_view = ObjectProperty(None)
    Builder.load_file('gui/mainscreen.kv')
    stop = threading.Event()
    """ TODO: file chooser button and show data tree, create stash,
     oram function, splitting file, encrypting and decrypting file"""

    def background_task(self):
        self.oram = PathORAM()
        self.oram.setup_cloud()
        self.stop.set()

    def on_pre_enter(self, *args):
        self.stash = Stash()
        # use thread for background task, use clock in a background task to access the ui
        threading.Thread(target=self.background_task).start()
        # TODO: create file and position map
        # TODO: read file map and display uploaded files in the listview
        file_label = self.file_view.add_node(TreeViewLabel(text='Files', is_open=True))
        # TODO: remove this node, add the real files from the filemap
        #self.file_view.add_node(TreeViewLabel(text='Test.txt'), file_label)

    def dismiss_popup(self):
        self._popup.dismiss()

    def select_file(self):
        content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
        self._popup = Popup(title="Load file", content=content, size_hint=(0.9, 0.9))
        self._popup.open()

    def load(self, path, filename):
        # TODO: save filename in the file.map
        # TODO: create chunks of the file and encrypt it, store it in the stash
        # TODO: save file size (maybe add padding)

        with open(os.path.join(path, filename[0]), utils.READ_BINARY_MODE) as file:
            self.file_input = file.read()

        # TODO: move it to a background thread
        chunkfile = ChunkFile(self.file_input, AES_CRYPTO)
        chunkfile.split()
        self.dismiss_popup()

    def select_location(self):
        print(2)

    def delete_selected_file(self):
        print(3)
