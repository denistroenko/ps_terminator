"""
agrs_pagser module. Content parser object for ring tool.

usage:
from args_parser import parser
"""


import argparse


# Global
parser = argparse.ArgumentParser()


def configure_parser() -> None:

    # Description
    parser.description = 'ps_terminator - console tool for ' \
                         'terminate OS processes'

    # Optional argument --username
    parser.add_argument('-u',
                        dest='user_names',
                        type=str,
                        default='',
                        action='store',
                        help='user names for filtering processes (separator - ",")',
                        )

    parser.add_argument('-p',
                        dest='ps_names',
                        type=str,
                        default='',
                        action='store',
                        help='process names for filtering processes (separator - ",")',
                        )

    parser.add_argument('-e',
                        dest='exclude_user_names',
                        type=str,
                        default='',
                        action='store',
                        help='exclude user names for filtering processes (separator - ",")',
                        )

    parser.add_argument('-m',
                        '--mode',
                        dest='mode',
                        type=str,
                        default='show',
                        action='store',
                        help='work mode: show|kill processes',
                        )

def print_parsed_args():
    print(parser.parse_args())

configure_parser()
