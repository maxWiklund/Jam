import os

from jam import common, config


class RmArgs:
    """Class to handle `rm` flag."""

    name = "rm"

    @staticmethod
    def build_args(sub_parser) -> None:
        """Setup arg parser for `rm` flag.

        Args:
            sub_parser (argparse._SubParsersAction): Parser to add arguments to.

        """
        parser = sub_parser.add_parser("rm", help="Remove dependency")
        parser.add_argument("package", help="Package name to remove as dependency")
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

        config_data = config.get_jam_config(args.config)
        if config_data.get(args.package):
            del config_data[args.package]

        config.write_config(args.config, config_data)
