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

import logging
import os

from jam import common, config

LOG = logging.getLogger(__name__)


class ListArgs:
    """Class to handle `list` flag."""

    name = "list"

    @staticmethod
    def build_args(sub_parser) -> None:
        """Setup arg parser for `list` flag.

        Args:
            sub_parser (argparse._SubParsersAction): Parser to add arguments to.

        """
        parser = sub_parser.add_parser("list", help="List information from Jam config.")
        parser.add_argument("--all", action="store_true", help="List all packages in config.")
        parser.add_argument("--config", default=os.getenv("JAM_ENV"), help="Jam config name.")
        parser.add_argument("--configs", action="store_true", help="List existing Jam configs.")
        parser.add_argument("--package", help="Package name to query information from.")

    @staticmethod
    def execute(args) -> None:
        """Execute command option.

        Args:
            args (argparse.Namespace): Parsed argument flags.

        """
        if args.configs:
            _print_configs()
            return

        if not args.config:
            common.no_config()
            return

        config_data = config.get_jam_config(args.config)
        if args.all:
            _print_table_of_content(config_data)
        elif args.package:
            _print_table_of_content({args.package: config_data.get(args.package, {})})


def _print_configs() -> None:
    """Print Existing jam config names."""
    for _conf in os.listdir(common.CONFIG_ROOT):
        if _conf.endswith(".jam"):
            print(_conf.replace(".jam", ""))


def _print_table_of_content(_config: dict) -> None:
    """Print data as table.

    Args:
        _config (dict): Jam package or config dict to print as table.

    """
    columns = []
    length = len(_config) + 1  # Add extra space for header.

    for column_key in ("name", "version", "path"):
        columns.append([column_key.capitalize()] + [v.get(column_key, "") for v in _config.values()])

    splitter = ""
    for row in range(length):
        row_text = "|"
        splitter = "+"
        for column in columns:
            text_length = len(max(column, key=len))
            text = column[row]
            row_text += f" {text}" + " " * (text_length - len(text)) + " |"
            splitter += "-" * (text_length + 1) + "-+"

        print(splitter)
        print(row_text)
    print(splitter)
