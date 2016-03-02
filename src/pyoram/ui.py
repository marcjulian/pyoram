import os
import threading

from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.uix.treeview import TreeViewLabel
from kivy.uix.popup import Popup

from pyoram import utils, controller
from pyoram.exceptions import WrongPassword, NoSelectedNode

AES_CRYPTO = None


def open_popup(title, err):
    popup = Popup(title=title, content=Label(text=err.__str__()),
                  size_hint=(None, None), size=(200, 200))
    popup.open()


class SignupScreen(Screen):
    Builder.load_file('gui/signupscreen.kv')

    def signup(self, pw, repw):
        if pw == repw and (pw and repw):
            controller.create_keys(pw)
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
        try:
            global AES_CRYPTO
            AES_CRYPTO = controller.verify_pw(pw)
            self.manager.current = 'main'
        except WrongPassword as err:
            open_popup('Wrong password', err)


class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)


class SaveDialog(FloatLayout):
    save = ObjectProperty(None)
    cancel = ObjectProperty(None)


class MainScreen(Screen):
    file_view = ObjectProperty(None)
    Builder.load_file('gui/mainscreen.kv')
    stop = threading.Event()
    """ TODO: file chooser button and show data tree, create stash,
     oram function, splitting file, encrypting and decrypting file"""

    def background_task(self):
        controller.setup_cloud()
        self.stop.set()

    def on_pre_enter(self, *args):
        controller.setup_stash()
        # use thread for background task, use clock in a background task to access the ui
        threading.Thread(target=self.background_task).start()
        file_names = controller.get_uploaded_file_names()
        for file_name in file_names:
            self.file_view.add_node(TreeViewLabel(text=file_name))

    def dismiss_popup(self):
        self._popup.dismiss()

    def select_file(self):
        content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
        self._popup = Popup(title="Load file", content=content, size_hint=(0.9, 0.9))
        self._popup.open()

    def load(self, path, filename):
        with open(os.path.join(path, filename[0]), utils.READ_BINARY_MODE) as file:
            self.file_input = file.read()

        # TODO: move it to a background thread, if necessary
        filename = os.path.basename(filename[0])
        controller.split_file_input(filename, self.file_input, AES_CRYPTO)
        self.file_view.add_node(TreeViewLabel(text=filename))
        self.dismiss_popup()

    def get_selected_node(self):
        selected_node = self.file_view.selected_node
        if selected_node is None:
            print('No selected Node')
            raise NoSelectedNode('No file has been selected.')
        return selected_node.text

    def select_location(self):
        try:
            self.selected_node_text = self.get_selected_node()
        except NoSelectedNode as err:
            open_popup('Download error', err)
            return
        print(self.selected_node_text)
        # content = SaveDialog(save=self.save, cancel=self.dismiss_popup)
        # self._popup = Popup(title="Save file", content=content,
        #                   size_hint=(0.9, 0.9))
        # self._popup.open()

    def save(self, path, filename):
        # TODO: retrieve filename from keyfile to identify dataIDs
        # TODO: check if data items are stored in the stash otherwise download them from the cloud
        self.dismiss_popup()

    def delete_selected_file(self):
        try:
            self.selected_node_text = self.get_selected_node()
        except NoSelectedNode as err:
            open_popup('Delete error', err)
            return
        print(self.selected_node_text)
        # TODO: delete selected file from file.map, position map and maybe stash
