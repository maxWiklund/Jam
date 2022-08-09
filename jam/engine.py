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

from typing import List
import hashlib
import os
import re
import subprocess

from jam import common


_EXCLUDE_DIRS = (r"__pycache__", r"build", r".*\.egg-info")
_RE_EXCLUDE_PATTERN = re.compile("|".join(map(lambda a: f"({a})", _EXCLUDE_DIRS)))


def hash_directory(path: str) -> str:
    """Generate hash for directory and all content.

    Args:
        path: Directory to hash.

    Returns:
        str: Unique for directory content.

    """
    hash_func = hashlib.sha1
    filenames = []
    for root, dirs, files in os.walk(path):
        [dirs.remove(d) for d in list(dirs) if _RE_EXCLUDE_PATTERN.match(d)]
        for fn in files:
            filenames.append(os.path.join(root, fn))

    filenames.sort()
    index = "\n".join(
        "{}={}".format(os.path.relpath(fn, path), hash_func(open(fn, "rb").read()).hexdigest()) for fn in filenames
    )
    return hash_func(index.encode("utf-8")).hexdigest()


def build_package(install_dir: str, package: dict):
    """Build package with rez.

    Args:
        install_dir: Unique install directory.
        package: Package dictionary.

    """
    if not os.path.exists(install_dir):
        os.makedirs(install_dir)

    print("Building package: ", package.get("name"))
    cmd = ["cd {}".format(package.get("path", ""))]
    cmd.append(f"rez build -ci --prefix {install_dir}")
    subprocess.run(" ; ".join(cmd), shell=True)


class ConfigEngine(object):
    """Class to generate packages and build paths."""

    def __init__(self, config: dict):
        """Initialize class and do nothing.

        Args:
            config: Jam config to run.

        """
        super(ConfigEngine, self).__init__()
        self._config = config

    def get_install_paths(self) -> List[str]:
        """Get install paths from local packages."""
        hashed_package_paths = []
        for package in self._config.values():
            if not package.get("local"):
                continue

            pk_hash = hash_directory(package.get("path"))
            package_hash_path = os.path.join(common.BUILD_ROOT, pk_hash)

            if not os.path.exists(package_hash_path):
                # The package is new or a change has been made to the source code. We need to rebuild it.
                build_package(package_hash_path, package)

            hashed_package_paths.append(package_hash_path)

        return hashed_package_paths

    def get_packages(self) -> List[str]:
        """Get rez packages to rezolve.

        Returns:
            list[str]: List of rez packages.

        """
        packages = []
        for package in self._config.values():
            version = "-" + package["version"] if package["version"] else ""
            packages.append(package.get("name") + version)

        return packages
