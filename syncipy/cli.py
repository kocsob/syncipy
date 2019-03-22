import pathlib

import click

from syncipy.config_handler import JsonConfigFileHandler
from syncipy.syncipy import Syncipy, IP_IDENTIFIER_URLS

APP_NAME = 'syncipy'


@click.group()
def cli():
    """Sync public IP to different DNS provider."""


@cli.command()
@click.option('--hostname', prompt=True, help='Hostname')
@click.option('--username', prompt=True, help='Username for the DNS provider')
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True, help='Password for the DNS provider')
@click.option('--path', type=pathlib.Path, default=click.get_app_dir(APP_NAME), help='config file path', show_default=True)
def config(path, hostname, username, password):
    """Store configuration for syncing IP to the DNS provider"""
    config_file_handler = JsonConfigFileHandler(config_file_path=path)
    config_file_handler.store(hostname, username, password)


def load_config_from_file(ctx, param, config_file_path):
    config_file_handler = JsonConfigFileHandler(config_file_path)
    ctx.default_map = config_file_handler.load()


@cli.command()
@click.option('--hostname', required=True, help='Hostname')
@click.option('--username', required=True, help='Username for the DNS provider')
@click.option('--password', required=True, help='Password for the DNS provider')
@click.option('--config-file', type=pathlib.Path, default=click.get_app_dir(APP_NAME), help='config file path', show_default=True, is_eager=True, callback=load_config_from_file)
def sync(hostname, username, password, config_file):
    """Sync IP to the DNS provider"""
    print(hostname, username, password)
    print(Syncipy(ip_identifier_urls=IP_IDENTIFIER_URLS).get_current_ip())


if __name__ == '__main__':
    cli()
