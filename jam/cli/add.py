import logging
import os

from jam import common, config, rez_package

LOG = logging.getLogger(__name__)


class AddArgs:
    """Class to handle `add` flag."""

    name = "add"

    @staticmethod
    def build_args(sub_parser) -> None:
        """Setup arg parser for `add` flag.

        Args:
            sub_parser (argparse._SubParsersAction): Parser to add arguments to.

        """
        parser = sub_parser.add_parser("add", help="Add local or remote package as build dependency")
        parser.add_argument("package", help="Package name (optional version) or local directory")
        parser.add_argument("--config", default=os.getenv("JAM_ENV"), help="Jam config name.")

    @staticmethod
    def execute(args) -> None:
        """Execute command option.

        Args:
            args (argparse.Namespace): Parsed argument flags.

        """
        if not args.config:
            common.no_config()
            return

        package = rez_package.get_package_data(args.package)
        if not package:
            return

        config_data = config.get_jam_config(args.config)
        config_data.update(package)

        config.write_config(args.config, config_data)
