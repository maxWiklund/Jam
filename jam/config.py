import json
import logging
import os

from jam import common

LOG = logging.getLogger(__name__)


def config_exists(config_name: str):
    """Check if jam config exists

    Args:
        config_name: Jam config name.

    Returns:
        bool: True if config exists else False.

    """
    config_path = os.path.join(common.CONFIG_ROOT, f"{config_name}.jam")
    return os.path.exists(config_path)


def get_jam_config(config_name: str) -> dict:
    """Load jam config from name.

    Args:
        config_name: Name of jam config file to load (without extension).

    Returns:
        dict: Config data from jam config.

    """
    config_path = os.path.join(common.CONFIG_ROOT, f"{config_name}.jam")
    if not config_exists(config_name):
        LOG.error(f'"{config_name}" does not exist in "{common.CONFIG_ROOT}"')
        return {}

    with open(config_path) as f:
        try:
            package_data = json.load(f)
            return package_data
        except json.decoder.JSONDecodeError:
            LOG.exception(f'Failed to parse "{config_path}"')
            return {}


def create_new_config(config_name: str) -> None:
    """Create new jam config.

    Args:
        config_name: New config name (without extension).

    """
    write_config(config_name, {})


def write_config(config_name: str, data: dict) -> None:
    """Write jam config data to disk.

    Args:
        config_name: Name of jam config file to write.
        data: Data to write as json.

    """
    config_path = os.path.join(common.CONFIG_ROOT, f"{config_name}.jam")
    with open(config_path, "w") as f:
        json.dump(data, f, indent=2)
