# coding: utf-8

"""
Law command line interface entry point.
"""


import sys
from importlib import import_module
from argparse import ArgumentParser

import law


progs = ["run", "index", "config", "software", "completion", "location"]
forward_progs = ["run"]

# temporary command to show renaming note
progs.append("db")


def run():
    """
    Entry point to the law cli. Sets up all parsers, parses all arguments, and executes the
    requested subprogram.
    """
    # setup the main parser and sub parsers
    parser = ArgumentParser(prog="law", description="The law command line tool.")
    sub_parsers = parser.add_subparsers(help="subcommands", dest="command")

    # add main arguments
    parser.add_argument("--version", "-V", action="version", version=law.__version__)

    # setup all progs
    mods = {}
    for prog in progs:
        mods[prog] = import_module("law.cli." + prog)
        mods[prog].setup_parser(sub_parsers)

    # parse args and dispatch execution
    prog = sys.argv[1] if len(sys.argv) >= 2 else None
    if prog and prog in forward_progs:
        # add the prog to the executable in argv so it will be included
        # in help and error messages of the forwarded parser
        sys.argv[0] += " " + prog
        args = parser.parse_args(sys.argv[1:3])
    else:
        args = parser.parse_args()

    # the parser determines the prog, so overwrite it
    prog = args.command
    if prog:
        mods[prog].execute(args)
    else:
        parser.print_help()
