import textwrap
import os

from unittest import mock, TestCase


from jam import rez_package


class RezPackage(TestCase):
    @mock.patch(
        "builtins.open",
        new_callable=mock.mock_open,
    )
    @mock.patch("jam.rez_package.os.path.exists", return_value=False)
    def test_load_local_package_package_does_not_exist(self, mock_exists, mock_open):

        expected_result = {}

        self.assertEqual(expected_result, rez_package.load_local_package("mock_config"))
        mock_open.assert_not_called()

    @mock.patch("jam.rez_package.os.path.exists", return_value=True)
    def test_load_local_package_success(self, mock_exists):
        file_data = textwrap.dedent(
            """

        name = "mock_package"

        version = "1.0.0"

        authors = ["max-wi"]

        """
        )

        package_path = "/mock/path/package.py"
        expected_result = {
            "mock_package": {"local": True, "path": os.path.dirname(package_path), "version": "1.0.0", "name": "mock_package"}
        }

        with mock.patch("builtins.open", mock.mock_open(read_data=file_data)) as mock_file:
            self.assertEqual(expected_result, rez_package.load_local_package(package_path))
            mock_file.assert_called_once_with(package_path)

    def test_get_package_data_remote_success(self):
        expected_result = {"abc": {"name": "abc", "local": False, "version": "12+<14", "path": ""}}
        self.assertEqual(expected_result, rez_package.get_package_data("abc-12+<14"))

    @mock.patch("jam.rez_package.load_local_package")
    @mock.patch("jam.rez_package.os.path.realpath")
    @mock.patch("jam.rez_package.os.path.exists", return_value=True)
    def test_get_package_data_local_success(self, mock_exist, mock_real_path, load_local_package):
        package_path = "/mock/path/to/package"
        mock_real_path.return_value = package_path
        rez_package.get_package_data(package_path)
        load_local_package.assert_called_once_with(package_path)
