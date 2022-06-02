"""Setup command line args."""
import argparse
import sys

from jam import cli
from jam import common


def enough_args():
    """bool: Validate number of arguments."""
    return len(sys.argv) > 1


def run() -> None:
    """Run application."""
    parser = argparse.ArgumentParser(description="Develop tool for rez.")
    sub_parser = parser.add_subparsers(dest="cmd", metavar="COMMAND")

    # Setup command line options.
    for arg_module in cli.CLI_ARG_OPTIONS:
        arg_module.build_args(sub_parser)

    args = parser.parse_args()
    if not enough_args():
        parser.error("To few arguments provided.")
        return

    if not common.validate_jam_env():
        return

    for arg_module in cli.CLI_ARG_OPTIONS:
        if sys.argv[1] == arg_module.name:
            arg_module.execute(args)
            return
