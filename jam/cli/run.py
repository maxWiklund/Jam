import logging
import os
import subprocess

from jam import common, config, engine

LOG = logging.getLogger(__name__)


class RunArgs:
    name = "run"

    @staticmethod
    def build_args(sub_parser) -> None:
        """Setup arg parser for `run` flag.

        Args:
            sub_parser (argparse._SubParsersAction): Parser to add arguments to.

        """
        parser = sub_parser.add_parser("run", help="Build and run Jam config.")
        parser.add_argument("--command", "-c", help="Command to run after building and loading config.")
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
        _engine = engine.ConfigEngine(config_data)

        rez_command = ["rez", "env"]
        rez_command.extend([f'"{p}"' for p in _engine.get_packages()])
        rez_command.extend(["--paths", ":".join(_engine.get_install_paths())])

        if args.command:
            rez_command.extend(["-c", args.command])

        print("Running rez env on configured packages.")
        LOG.debug(" ".join(rez_command))
        subprocess.run(" ".join(rez_command), shell=True)
