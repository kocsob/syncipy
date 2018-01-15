import io
import pathlib
import sys

import pytest

from syncipy.credential import Base64EncodedCredentialsFileHandler, CredentialHandler


@pytest.mark.usefixtures('fs')
class TestBase64EncodedCredentialsFileHandler:
    TESTPATH = '~/.config/syncipy.cred'
    USERNAME = 'testuser'
    PASSWORD = 'testpass'
    BASE64TEXT = "dGVzdHVzZXI6dGVzdHBhc3M="

    def test_load(self):
        testfile = pathlib.Path(self.TESTPATH)
        testfile.expanduser().parent.mkdir(parents=True)
        testfile.expanduser().write_text(self.BASE64TEXT)

        retval = Base64EncodedCredentialsFileHandler(testfile).load()
        assert retval == self.BASE64TEXT

    def test_store(self):
        testfile = pathlib.Path(self.TESTPATH)
        testfile.expanduser().parent.mkdir(parents=True)

        Base64EncodedCredentialsFileHandler(testfile).store(username=self.USERNAME, password=self.PASSWORD)

        assert testfile.expanduser().is_file()
        assert testfile.expanduser().stat().st_mode & 0o777 == 0o600
        retval = testfile.expanduser().read_text()
        assert retval == self.BASE64TEXT

    def test_store_load(self):
        testfile = pathlib.Path(self.TESTPATH)
        testfile.expanduser().parent.mkdir(parents=True)

        b64ecfh = Base64EncodedCredentialsFileHandler(testfile)
        b64ecfh.store(username=self.USERNAME, password=self.PASSWORD)
        retval = b64ecfh.load()

        assert retval == self.BASE64TEXT


@pytest.mark.usefixtures('fs')
@pytest.mark.filterwarnings('ignore::UserWarning')
class TestCredentialsHandler:
    TESTPATH = '~/.config/syncipy.cred'
    USERNAME = 'testuser'
    PASSWORD = 'testpass'
    BASE64TEXT = "dGVzdHVzZXI6dGVzdHBhc3M="

    def test_store_full_interactive(self):
        sys.stdin = io.StringIO(self.USERNAME + '\n' + self.PASSWORD + '\n' + self.PASSWORD)

        testfile = pathlib.Path(self.TESTPATH)
        testfile.expanduser().parent.mkdir(parents=True)

        CredentialHandler(testfile).store()

        retval = testfile.expanduser().read_text()
        assert retval == self.BASE64TEXT

    def test_store_password_interactive(self):
        sys.stdin = io.StringIO(self.PASSWORD + '\n' + self.PASSWORD)

        testfile = pathlib.Path(self.TESTPATH)
        testfile.expanduser().parent.mkdir(parents=True)

        CredentialHandler(testfile).store(username=self.USERNAME)

        retval = testfile.expanduser().read_text()
        assert retval == self.BASE64TEXT

    def test_store_non_interactive(self):
        testfile = pathlib.Path(self.TESTPATH)
        testfile.expanduser().parent.mkdir(parents=True)

        CredentialHandler(testfile).store(username=self.USERNAME, password=self.PASSWORD)

        retval = testfile.expanduser().read_text()
        assert retval == self.BASE64TEXT
