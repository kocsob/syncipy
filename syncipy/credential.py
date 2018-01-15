import abc
import base64
import getpass
from io import StringIO
from pathlib import Path
from typing import Type


class AbstractCredentialsFileHandler(abc.ABC):
    def __init__(self, credential_file_path: Path) -> None:
        self._credential_file_path = credential_file_path.expanduser()

    @property
    def credential_file_path(self):
        return self._credential_file_path

    def load(self) -> str:
        with self.credential_file_path.open('r') as fp:
            return self.parse(fp)

    def store(self, username: str, password: str):
        temp_file = self.credential_file_path.with_suffix('.tmp')
        with temp_file.open('w') as fp:
            self.serialize(username, password, fp)
        temp_file.rename(self.credential_file_path)
        self.credential_file_path.chmod(0o600)

    @staticmethod
    @abc.abstractmethod
    def parse(file_object: StringIO) -> str:
        pass

    @staticmethod
    @abc.abstractmethod
    def serialize(username: str, password: str, file_object: StringIO) -> None:
        pass


class Base64EncodedCredentialsFileHandler(AbstractCredentialsFileHandler):
    @staticmethod
    def parse(file_object: StringIO) -> str:
        return file_object.read()

    @staticmethod
    def serialize(username: str, password: str, file_object: StringIO) -> None:
        content = username + ':' + password
        encoded_content = base64.b64encode(content.encode('utf-8'))
        file_object.write(encoded_content.decode('utf-8'))


class CredentialsHandlerError(Exception):
    pass


class CredentialHandler:
    def __init__(self, credential_file_path: Path, credential_file_handler: Type[AbstractCredentialsFileHandler]=Base64EncodedCredentialsFileHandler):
        self._credential_file_handler = credential_file_handler(credential_file_path)

    def load(self):
        return self._credential_file_handler.load()

    def store(self, username: str=None, password: str=None):
        if username is None:
            username = self._get_username_interactive()

        if password is None:
            password = self._get_password_interactive()

        self._credential_file_handler.store(username, password)

    @staticmethod
    def _get_username_interactive(input: input=input):
        username = input("username: ")
        return username

    @staticmethod
    def _get_password_interactive(input: input=getpass.getpass):
        password = input("password: ")
        retype_password = input("retype password: ")

        if (password != retype_password):
            raise CredentialsHandlerError("Passwords do not match")

        return password
