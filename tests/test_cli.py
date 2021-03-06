import os
import unittest
import click
from click.testing import CliRunner
import nordicsemi
from nordicsemi import __main__
from nordicsemi import dfu


class TestManifest(unittest.TestCase):
    runner = CliRunner()
    cli = __main__.cli

    def setUp(self):
        script_abspath = os.path.abspath(__file__)
        script_dirname = os.path.dirname(script_abspath)
        os.chdir(script_dirname)

    def test_pkg_gen(self):
        result = self.runner.invoke(self.cli,
                                    ['pkg', 'generate',
                                     '--application', 'resources/dfu_test_app_hrm_s130.hex',
                                     '--hw-version', '52', '--sd-req', '0', '--application-version',
                                     '0', '--sd-id', '0x008C', 'test.zip'])
        self.assertIsNone(result.exception)

    def test_dfu_ble_address(self):
        argumentList = ['dfu', 'ble', '-ic', 'NRF52', '-p', 'port', '-pkg',
                        'resources/test_package.zip', '--address']

        address = 'AABBCC112233'
        result = self.runner.invoke(self.cli, argumentList + [address])
        self.assertTrue('Invalid address' not in result.output)
        self.assertTrue('Failed to open' in str(result.exception))

        address = 'AA:BB:CC:11:22:33'
        result = self.runner.invoke(self.cli, argumentList + [address])
        self.assertTrue('Invalid address' not in result.output)
        self.assertTrue('Failed to open' in str(result.exception))

        address = 'AABBCC11223'
        result = self.runner.invoke(self.cli, argumentList + [address])
        self.assertTrue('Invalid address' in result.output)
        self.assertIsNone(result.exception)

        address = 'AABBCC1122334'
        result = self.runner.invoke(self.cli, argumentList + [address])
        self.assertIsNone(result.exception)


if __name__ == '__main__':
    unittest.main()
