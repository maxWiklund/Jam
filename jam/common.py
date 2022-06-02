import logging
import os

LOG = logging.getLogger(__name__)
CONFIG_ROOT = os.getenv("JAM_CONFIG_PATH", "")
BUILD_ROOT = os.getenv("JAM_BUILD_PATH", "")


def validate_jam_env() -> bool:
    """bool: Check if jam is configured correctly."""
    if not os.path.exists(BUILD_ROOT):
        LOG.error("Environment variable JAM_BUILD_PATH is not set.")
        return False
    if not os.path.exists(CONFIG_ROOT):
        LOG.error("Environment variable JAM_CONFIG_PATH is not set.")
        return False

    return True


def no_config() -> None:
    """Print no config message."""
    LOG.error("No Jam config provided. Either run `jam edit <config_name>` or proved the `--config` flag.")
