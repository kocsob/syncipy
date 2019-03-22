import logging
from ipaddress import ip_address, IPv4Address, IPv6Address, AddressValueError
from typing import List, Union

import requests


IP_IDENTIFIER_URLS = [
    "http://ipv4.icanhazip.com/",
    "http://v4.ident.me/",
    "https://api.ipify.org/",
    "http://ifconfig.me/ip"
]


class Syncipy:

    def __init__(self, ip_identifier_urls: List[str], requests: requests=requests, logger=None):
        self.ip_identifier_urls = ip_identifier_urls
        self.requests = requests
        self.logger = logger
        if self.logger is None:
            self.logger = logging.getLogger(__name__)

    def get_current_ip(self) -> Union[IPv4Address, IPv6Address]:
        current_ip = None
        for ip_identifier_url in self.ip_identifier_urls:
            current_ip = self._get_ip_from_identifier(ip_identifier_url)
            print(current_ip)
            if current_ip:
                break

        if current_ip is None:
            raise Exception('Cannot get current ip')

        return current_ip

    def _get_ip_from_identifier(self, ip_identifier_url: str) -> Union[IPv4Address, IPv6Address, None]:
        try:
            response = self.requests.get(ip_identifier_url)
            response.raise_for_status()
            current_ip = ip_address(response.text.strip())
            self.logger.debug('Current IP is {current_ip}'.format(current_ip=current_ip))
            return current_ip
        except (requests.ConnectionError, AddressValueError):
            pass

        return None


