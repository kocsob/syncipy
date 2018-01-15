import io
from io import StringIO
from pathlib import Path

import pytest

from syncipy.credential import Base64EncodedCredentialsFileHandler, CredentialHandler, CredentialsHandlerError, AbstractCredentialsFileHandler


class TestBase64EncodedCredentialsFileHandler:
    USERNAME = 'testuser'
    PASSWORD = 'testpass'
    BASE64TEXT = "dGVzdHVzZXI6dGVzdHBhc3M="

    def test_parse(self):
        file_object = io.StringIO(self.BASE64TEXT)
        retval = Base64EncodedCredentialsFileHandler.parse(file_object=file_object)
        assert retval == self.BASE64TEXT

    def test_serialize(self):
        file_object = io.StringIO()
        Base64EncodedCredentialsFileHandler.serialize(username=self.USERNAME, password=self.PASSWORD, file_object=file_object)
        assert file_object.getvalue() == self.BASE64TEXT


class TestCredentialsHandler:
    USERNAME = 'testuser'
    PASSWORD = 'testpass'

    def test_password_interactive_match(self):
        called = 0

        def input(message):
            nonlocal called
            called += 1
            if called == 1:
                return self.PASSWORD
            elif called == 2:
                return self.PASSWORD
            else:
                raise Exception("Too much input call")

        retval = CredentialHandler._get_password_interactive(input=input)
        assert retval == self.PASSWORD
        assert called == 2

    def test_password_interactive_not_match(self):
        called = 0

        def input(message):
            nonlocal called
            called += 1
            if called == 1:
                return self.PASSWORD
            elif called == 2:
                return self.PASSWORD + 'a'
            else:
                raise Exception("Too much input call")

        with pytest.raises(CredentialsHandlerError):
            CredentialHandler._get_password_interactive(input=input)
        assert called == 2

    def test_store_wit_given_user_and_password(self):
        credential_file_path, stored_username, stored_password = None, None, None

        class DummyCredentialsFileHandler(AbstractCredentialsFileHandler):
            def store(self, username: str, password: str):
                nonlocal credential_file_path, stored_username, stored_password
                stored_username = username
                stored_password = password
                credential_file_path = self.credential_file_path

            @staticmethod
            def parse(file_object: StringIO):
                pass

            @staticmethod
            def serialize(username: str, password: str, file_object: StringIO):
                pass

        CredentialHandler(Path('/credential/file/path'), DummyCredentialsFileHandler).store(username=self.USERNAME, password=self.PASSWORD)
        assert stored_username == self.USERNAME
        assert stored_password == self.PASSWORD
        assert credential_file_path == Path('/credential/file/path')

    def test_load(self):
        credential = "dummy_credential"

        class DummyCredentialsFileHandler(AbstractCredentialsFileHandler):
            def load(self):
                return credential

            @staticmethod
            def parse(file_object: StringIO):
                pass

            @staticmethod
            def serialize(username: str, password: str, file_object: StringIO):
                pass

        retval = CredentialHandler(Path('/credential/file/path'), DummyCredentialsFileHandler).load()
        assert retval == credential
