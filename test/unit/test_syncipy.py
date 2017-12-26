from collections import namedtuple, OrderedDict
from ipaddress import ip_address

import pytest
import requests

from syncipy.syncipy import Syncipy

RequestsMockReponse = namedtuple('RequestResponse', ['text', 'raise_for_status'])


class RequestsMock():
    def __init__(self, responses):
        self.responses = responses

    def raise_for_status_without_exception(self):
        pass

    def raise_for_status_with_exception(self):
        raise requests.ConnectionError

    def get(self, url):
        if url not in self.responses:
            raise Exception('Cannot find {url}'.format(url=url))

        if self.responses[url] is None:
            return RequestsMockReponse(self.responses[url], self.raise_for_status_with_exception)
        else:
            return RequestsMockReponse(self.responses[url], self.raise_for_status_without_exception)


def test_get_current_ip_with_first_hit():
    responses = OrderedDict([
        ('http://testurl1', '92.89.16.23'),
        ('http://testurl2', '92.89.16.24'),
    ])

    current_ip = Syncipy(responses.keys(), requests=RequestsMock(responses=responses)).get_current_ip()

    assert current_ip == ip_address(list(responses.values())[0])


def test_get_current_ip_with_second_hit():
    responses = OrderedDict([
        ('http://testurl1', None),
        ('http://testurl2', '92.89.16.24')
    ])

    current_ip = Syncipy(responses.keys(), requests=RequestsMock(responses=responses)).get_current_ip()

    assert current_ip == ip_address(list(responses.values())[-1])


def test_get_current_ip_no_hit():
    responses = OrderedDict([
        ('http://testurl1', None),
        ('http://testurl2', None)
    ])

    with pytest.raises(Exception):
        Syncipy(responses.keys(), requests=RequestsMock(responses=responses)).get_current_ip()
