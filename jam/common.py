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
