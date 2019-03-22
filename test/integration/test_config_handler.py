import json
import pathlib

import pytest

from syncipy.config_handler import JsonConfigFileHandler


@pytest.mark.usefixtures('fs')
class TestBase64EncodedCredentialsFileHandler:
    CONFIG_FILE_PATH = '~/.config/syncipy'
    HOSTANME = 'hostname'
    USERNAME = 'testuser'
    PASSWORD = 'testpass'
    CONFIG_DATA = dict(
        hostname=HOSTANME,
        username=USERNAME,
        password=PASSWORD,
    )
    CONFIG_FILE_CONTENT = json.dumps(CONFIG_DATA, indent=4)

    def test_load(self):
        config_file = pathlib.Path(self.CONFIG_FILE_PATH).expanduser()
        config_file.parent.mkdir(parents=True)
        config_file.write_text(self.CONFIG_FILE_CONTENT)

        retval = JsonConfigFileHandler(config_file).load()
        assert retval == self.CONFIG_DATA

    def test_store(self):
        config_file = pathlib.Path(self.CONFIG_FILE_PATH).expanduser()
        config_file.parent.mkdir(parents=True)

        JsonConfigFileHandler(config_file).store(hostname=self.HOSTANME, username=self.USERNAME, password=self.PASSWORD)

        assert config_file.is_file()
        assert config_file.stat().st_mode & 0o777 == 0o600
        assert config_file.read_text() == self.CONFIG_FILE_CONTENT

    def test_store_load(self):
        config_file = pathlib.Path(self.CONFIG_FILE_PATH).expanduser()
        config_file.parent.mkdir(parents=True)

        jch = JsonConfigFileHandler(config_file)
        jch.store(hostname=self.HOSTANME, username=self.USERNAME, password=self.PASSWORD)
        retval = jch.load()

        assert retval == self.CONFIG_DATA