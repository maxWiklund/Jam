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
