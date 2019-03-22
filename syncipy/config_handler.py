import json
import abc
from pathlib import Path
from typing import Dict, TextIO


class AbstractConfigFileHandler(abc.ABC):
    def __init__(self, config_file_path: Path) -> None:
        self._config_file_path = config_file_path

    @property
    def config_file_path(self):
        return self._config_file_path

    def load(self) -> Dict:
        with self.config_file_path.open('r') as fp:
            return self.parse(fp)

    def store(self, *args, **kwargs):
        temp_file = self.config_file_path.with_suffix('.tmp')
        with temp_file.open('w') as fp:
            self.serialize(fp, *args, **kwargs)
        temp_file.rename(self.config_file_path)
        self.config_file_path.chmod(0o600)

    @staticmethod
    @abc.abstractmethod
    def parse(file_object: TextIO) -> Dict:
        pass

    @staticmethod
    @abc.abstractmethod
    def serialize(file_object: TextIO, hostname: str, username: str, password: str) -> None:
        pass


class JsonConfigFileHandler(AbstractConfigFileHandler):
    @staticmethod
    def parse(file_object: TextIO) -> Dict:
        return json.load(file_object)

    @staticmethod
    def serialize(file_object: TextIO, hostname: str, username: str, password: str) -> None:
        fields = dict(
            hostname=hostname,
            username=username,
            password=password,
        )
        json.dump(fields, file_object, indent=4)
