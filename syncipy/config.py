import json

from configargparse import ConfigFileParser, ConfigFileParserException
from collections import OrderedDict


class JSONConfigFileParser(ConfigFileParser):
    def get_syntax_description(self):
        msg = ("The config file uses JSON syntax and must represent a JSON "
               "'mapping' (for details, see https://www.json.org/).")
        return msg

    def parse(self, stream):
        """Parses the keys and values from a config file."""

        try:
            parsed_obj = json.load(stream)
        except Exception as e:
            raise ConfigFileParserException("Couldn't parse config file: %s" % e)

        if not isinstance(parsed_obj, dict):
            raise ConfigFileParserException("The config file doesn't appear to "
                                            "contain 'key: value' pairs (aka. a YAML mapping). "
                                            "yaml.load('%s') returned type '%s' instead of 'dict'." % (
                                                getattr(stream, 'name', 'stream'), type(parsed_obj).__name__))

        result = OrderedDict()
        for key, value in parsed_obj.items():
            if isinstance(value, list):
                result[key] = value
            else:
                result[key] = str(value)

        return result

    def serialize(self, items, default_flow_style=False):
        """Does the inverse of config parsing by taking parsed values and
        converting them back to a string representing config file contents.
        Args:
            default_flow_style: defines serialization format (see PyYAML docs)
        """

        # it looks like ordering can't be preserved: http://pyyaml.org/ticket/29
        items = dict(items)
        return json.dumps(items)
