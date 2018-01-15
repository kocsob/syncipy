#!/usr/bin/env python3

import os
import sys
from pathlib import Path

import configargparse

import credential
import syncipy
from config import JSONConfigFileParser


def _add_sync_ip_parser_arguments(sync_ip_parser):
    sync_ip_parser.add_argument('--bar', action='store_true', help='bar help')


def create_argument_parser():
    parser = configargparse.ArgumentParser(prog='Syncipy', default_config_files=[])
    parser.add_argument('--debug', action='store_true', help='debug log')
    subparsers = parser.add_subparsers(title='subcommands', description='valid subcommands', help='additional help')
    subparsers.required = True

    # create the parser for run sync ip
    sync_ip_parser = subparsers.add_parser('sync-ip', help='sync ip help', config_file_parser_class=JSONConfigFileParser, default_config_files=['~/.config/syncipy.conf'])
    _add_sync_ip_parser_arguments(sync_ip_parser)
    sync_ip_parser.set_defaults(func=lambda args: syncipy.Syncipy(syncipy.IP_IDENTIFIER_URLS).get_current_ip(args.bar))

    # create the parser for storing configuration
    store_conf_parser = subparsers.add_parser('store-conf', help='b help', config_file_parser_class=JSONConfigFileParser)
    _add_sync_ip_parser_arguments(store_conf_parser)
    store_conf_parser.add_argument('--path', help='baz help', default=os.path.expanduser('~/.config/syncipy.conf'), is_write_out_config_file_arg=True)

    # create the parser for storing credential
    store_cred_parser = subparsers.add_parser('store-cred', help='store syncipy credential')
    store_cred_parser.add_argument('--username', help='username')
    store_cred_parser.add_argument('--password', help='password')
    store_cred_parser.add_argument('--path', help='credentials file path', default='~/.config/syncipy.cred', type=Path)
    store_cred_parser.set_defaults(func=lambda args: credential.CredentialsHandler(args.path).store(args.username, args.password))

    return parser


def main(argv=sys.argv):
    parser = create_argument_parser()
    args = parser.parse_args(argv[1:])

    print(args.debug)
    args.func(args)


if __name__ == '__main__':
    main(sys.argv)
