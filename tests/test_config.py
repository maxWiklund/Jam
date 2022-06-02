from unittest import mock, TestCase

from jam import config


@mock.patch("jam.config.os.path.join", lambda *args: "/".join(args))
@mock.patch("jam.config.common.CONFIG_ROOT", "/mock/config_install")
class TestConfig(TestCase):
    @mock.patch("jam.config.os.path.exists", return_value=True)
    def test_config_exists_success(self, mock_exists):
        expected_value = True

        self.assertEqual(expected_value, config.config_exists("dev"))

    @mock.patch("jam.config.os.path.exists", return_value=False)
    def test_config_exists_failed(self, mock_exists):
        expected_value = False
        self.assertEqual(expected_value, config.config_exists("dev"))

    @mock.patch("builtins.open", new_callable=mock.mock_open)
    @mock.patch("jam.config.json.load")
    @mock.patch("jam.config.config_exists", return_value=True)
    def test_get_jam_config_success(self, mock_exists, json_mock, mock_open_file):
        config.get_jam_config("dev")
        mock_open_file.assert_called_once_with("/mock/config_install/dev.jam")

    @mock.patch("builtins.open", new_callable=mock.mock_open)
    @mock.patch("jam.config.config_exists", return_value=False)
    def test_get_jam_config_config_does_not_exist(self, mock_exists, mock_open_file):
        expected_value = {}
        self.assertEqual(expected_value, config.get_jam_config("dev"))
        mock_open_file.assert_not_called()

    @mock.patch("jam.config.json.dump")
    @mock.patch("builtins.open", new_callable=mock.mock_open)
    def test_write_config_success(self, mock_open_file, json_mock):
        expected_file_path = "/mock/config_install/test.jam"
        data = {"maya": {"name": "maya", "version": "1.0.0"}}

        # with mock.
        config.write_config("test", data)

        mock_open_file.assert_called_once_with(expected_file_path, "w")
