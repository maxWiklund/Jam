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

from unittest import mock, TestCase

from jam import common


class TestCommon(TestCase):
    @mock.patch("jam.common.CONFIG_ROOT", "")
    def test_validate_jam_env_no_build_root(self):
        expected_value = False
        self.assertEqual(expected_value, common.validate_jam_env())

    @mock.patch("jam.common.BUILD_ROOT", "/mock/build_path")
    def test_validate_jam_env_no_install_root(self):
        expected_value = False
        self.assertEqual(expected_value, common.validate_jam_env())
