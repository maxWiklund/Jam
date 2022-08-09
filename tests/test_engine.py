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

from jam import engine


class TestConfigEngine(TestCase):
    @mock.patch("jam.engine.os.path.exists", return_value=True)
    @mock.patch("jam.engine.subprocess.run")
    def test_build_package_command(self, mock_run, mock_exists):
        install_dir = "/mock/build/path"
        source_dir = "/mock/local/path"
        cmd = ["cd", source_dir, ";"]
        cmd.extend(["rez", "build", "-ci", "--prefix", install_dir])
        package = {"local": True, "path": source_dir, "version": "2.7.4", "name": "python"}

        engine.build_package(install_dir, package)
        mock_run.assert_called_once_with(" ".join(cmd), shell=True)

    @mock.patch("jam.engine.build_package")
    @mock.patch("jam.engine.os.path.exists", return_value=False)
    @mock.patch("jam.engine.hash_directory")
    def test_get_install_paths_package_does_not_exist(self, mock_hash, mock_exists, mock_build):
        hash_dir = "/mock/hash/directory"
        mock_hash.return_value = hash_dir

        package = {
            "local": True,
            "path": "/mock/package/path",
            "version": "2.7.4",
            "name": "python",
        }
        config = {"python": package}

        _engine = engine.ConfigEngine(config)

        self.assertEqual([hash_dir], _engine.get_install_paths())
        mock_exists.assert_called_once_with(hash_dir)
        mock_build.assert_called_once_with(hash_dir, package)

    @mock.patch("jam.engine.build_package")
    @mock.patch("jam.engine.os.path.exists", return_value=True)
    @mock.patch("jam.engine.hash_directory")
    def test_get_install_paths_package_does_exist(self, mock_hash, mock_exists, mock_build):
        hash_dir = "/mock/hash/directory"
        mock_hash.return_value = hash_dir

        package = {
            "local": True,
            "path": "/mock/package/path",
            "version": "2.7.4",
            "name": "python",
        }
        config = {"python": package}

        _engine = engine.ConfigEngine(config)

        self.assertEqual([hash_dir], _engine.get_install_paths())
        mock_exists.assert_called_once_with(hash_dir)
        mock_build.assert_not_called()

    @mock.patch("jam.engine.hash_directory")
    def test_get_install_paths_package_not_local(self, mock_hash):
        package = {
            "local": False,
            "path": "",
            "version": "2.7.4",
            "name": "python",
        }
        config = {"python": package}
        _engine = engine.ConfigEngine(config)
        self.assertEqual([], _engine.get_install_paths())
        mock_hash.assert_not_called()

    def test_get_packages(self):
        expected_value = ["python-2.7.4"]

        package = {
            "local": False,
            "path": "",
            "version": "2.7.4",
            "name": "python",
        }
        config = {"python": package}
        _engine = engine.ConfigEngine(config)

        self.assertEqual(expected_value, _engine.get_packages())
