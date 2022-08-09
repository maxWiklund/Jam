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

from jam import config, shell

LOG = logging.getLogger(__name__)


class NewArgs:
    """Class to handle `new` flag."""

    name = "new"

    @staticmethod
    def build_args(sub_parser) -> None:
        """Setup arg parser for `new` flag.

        Args:
            sub_parser (argparse._SubParsersAction): Parser to add arguments to.

        """
        parser = sub_parser.add_parser("new", help="New package name.")
        parser.add_argument("config", help="New Jam config name to create.")

    @staticmethod
    def execute(args) -> None:
        """Execute command option.

        Args:
            args (argparse.Namespace): Parsed argument flags.

        """
        if config.config_exists(args.config):
            LOG.error(f'Config "{args.config}" already exists.')
            return

        config.create_new_config(args.config)
        shell.create_and_run_shell(args.config)
