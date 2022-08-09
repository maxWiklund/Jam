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
import re
import os


LOG = logging.getLogger(__name__)
RE_REZ_PACKAGE_NAME_VERSION = re.compile(r"(?P<name>\w+)(?:-(?P<version>.+))?")
RE_NAME = re.compile("(?:name[ =]+['\"](?P<name>\w+)['\"])")
RE_VERSION = re.compile("(?:version[ =]+['\"](?P<version>[\d+\.]+)['\"])")


def load_local_package(package_path: str) -> dict:
    """Parse rez package.py file to extract information from.

    Args:
        package_path: Directory path or file path to package.py file.

    Returns:
        dict: Package info.

    """
    package_path = package_path if package_path.endswith("package.py") else os.path.join(package_path, "package.py")

    if not os.path.exists(package_path):
        LOG.error(f'"{package_path}" does not exists')
        return {}

    with open(package_path) as f:
        package_data = f.read()

    package_name = RE_NAME.search(package_data).group("name")
    package_version = RE_VERSION.search(package_data).group("version")

    return {
        package_name: {
            "local": True,
            "path": os.path.dirname(package_path),
            "version": package_version,
            "name": package_name,
        }
    }


def get_package_data(package: str) -> dict:
    """Get package information from  remote name or local path.

    Args:
        package: Name of remote package or local path to rez package.

    """
    package_path = os.path.realpath(package)
    if os.path.exists(package_path):
        # Local package that needs to be parsed to access information.
        return load_local_package(package_path)
    else:

        # The package name looks something like "python-2.7+<4".
        match = RE_REZ_PACKAGE_NAME_VERSION.match(package)

        package_name = match.group("name")
        package_data = {
            "local": False,
            "version": match.group("version") or "",
            "path": "",
            "name": package_name,
        }
        return {package_name: package_data}
