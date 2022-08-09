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

from setuptools import setup
import jam


setup(
    name="jam",
    version=jam.__version__,
    packages=["jam", "jam.cli"],
    url="",
    license="Apache License 2.0",
    author="max-wi",
    author_email="",
    scripts=["bin/jam"],
    description="Tool to ease development with rez.",
    python_requires=">=3.6.2",
)
