import os
import threading

from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from kivy.uix.treeview import TreeViewLabel, TreeView

from pyoram import utils, controller
from pyoram.exceptions import WrongPassword, NoSelectedNode, DownloadFileError, FileSizeError, CloudTokenError

AES_CRYPTO = None


def open_popup_error(title, err):
    open_popup(title, err.__str__())


def open_popup(title, status):
    popup = Popup(title=title, content=Label(text=status),
                  size_hint=(None, None), size=(300, 200))
    popup.open()


class SignupScreen(Screen):
    Builder.load_file('gui/signupscreen.kv')

    def signup(self, pw, repw):
        if pw == repw and (pw and repw):
            controller.create_keys(pw)
            self.manager.current = 'login'
        elif not pw and not repw:
            open_popup('Empty password', 'Password cannot be empty')
        else:
            open_popup('Re-enter passwords', 'Passwords do not match')


class LoginScreen(Screen):
    Builder.load_file('gui/loginscreen.kv')

    def verify(self, pw):
        try:
            global AES_CRYPTO
            AES_CRYPTO = controller.verify_pw(pw)
            self.manager.current = 'main'
        except WrongPassword as err:
            open_popup_error('Wrong password', err)


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

    def setup_cloud_task(self):
        try:
            controller.setup_cloud(AES_CRYPTO)
        except CloudTokenError as err:
            open_popup_error('Cloud Token', err)
        self.stop.set()

    def on_pre_enter(self, *args):
        controller.setup_stash()
        # use thread for background task, use clock in a background task to access the ui
        threading.Thread(target=self.setup_cloud_task).start()
        file_names = controller.get_uploaded_file_names()
        self.file_view = TreeView(hide_root=True, indent_level=4)
        self.file_view.size_hint = 1, None
        self.file_view.bind(minimum_height=self.file_view.setter('height'))
        self.scroll_view.add_widget(self.file_view)
        for file_name in file_names:
            self.file_view.add_node(TreeViewLabel(text=file_name))

        self.max_storage_size = controller.get_max_storage_size()
        self.usage_bar.max = self.max_storage_size
        self.update_storage_view()

    def dismiss_popup(self):
        self._popup.dismiss()

    def select_file(self):
        content = LoadDialog(load=self.upload_file, cancel=self.dismiss_popup)
        self._popup = Popup(title="Upload file", content=content, size_hint=(0.9, 0.9))
        self._popup.open()

    def update_storage_view(self):
        self.used_storage_size = controller.get_used_storage_size()
        self.usage_label.text = controller.get_data_type_format(self.used_storage_size, self.max_storage_size)
        self.usage_bar.value = self.used_storage_size

    def get_free_storage_size(self):
        return self.max_storage_size - self.used_storage_size

    def split_input_file_task(self):
        controller.save_file_input(self.filename, self.file_input, AES_CRYPTO)
        self.file_view.add_node(TreeViewLabel(text=self.filename))
        self.update_storage_view()
        try:
            controller.update_data(self.filename, AES_CRYPTO)
        except CloudTokenError as err:
            open_popup_error('Cloud Token', err)
        self.stop.set()

    def upload_file_task(self):
        with open(os.path.join(self.path, self.filename[0]), utils.READ_BINARY_MODE) as file:
            self.file_input = file.read()

        if controller.is_storage_available(len(self.file_input), self.get_free_storage_size()):
            self.filename = os.path.basename(self.filename[0])
            self.split_input_file_task()
        else:
            open_popup('Upload Error', 'Not enough storage available.')

        self.stop.set()

    def upload_file(self, path, filename):
        self.path = path
        self.filename = filename
        threading.Thread(target=self.upload_file_task).start()
        self.dismiss_popup()

    def get_selected_node(self):
        selected_node = self.file_view.selected_node
        if selected_node is None:
            raise NoSelectedNode('No file has been selected.')
        return selected_node

    def select_location(self):
        try:
            self.selected_node_text = self.get_selected_node().text
        except NoSelectedNode as err:
            open_popup_error('Download error', err)
            return
        content = SaveDialog(save=self.save, cancel=self.dismiss_popup)
        content.file_name_label.text = self.selected_node_text
        self._popup = Popup(title="Download file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def download_file_task(self):
        try:
            controller.download_selected_file(self.selected_node_text, self.path, self.filename, AES_CRYPTO)
            open_popup('Download file', 'Download was successful')
        except (DownloadFileError, FileSizeError, CloudTokenError) as err:
            open_popup_error('Download error', err)
            return
        self.stop.set()

    def save(self, path, filename):
        self.path = path
        self.filename = filename
        threading.Thread(target=self.download_file_task).start()
        self.dismiss_popup()

    def delete_file_task(self):
        controller.delete_selected_node(self.selected_node_text)
        self.update_storage_view()
        self.stop.set()

    def delete_selected_file(self):
        try:
            self.selected_node = self.get_selected_node()
            self.selected_node_text = self.selected_node.text
        except NoSelectedNode as err:
            open_popup_error('Delete error', err)
            return
        self.file_view.remove_node(self.selected_node)
        threading.Thread(target=self.delete_file_task).start()
