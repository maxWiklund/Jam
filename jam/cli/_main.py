# Copyright (C) 2022  Max Wiklund
#
# Licensed under the Apache License, Version 2.0 (the “License”);
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an “AS IS” BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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
