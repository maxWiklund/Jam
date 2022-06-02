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
