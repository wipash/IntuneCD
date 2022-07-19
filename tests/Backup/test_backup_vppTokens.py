#!/usr/bin/env python3

"""This module tests backing up VPP Tokens."""

import json
import yaml
import unittest

from pathlib import Path
from unittest.mock import patch
from testfixtures import TempDirectory
from src.IntuneCD.backup_vppTokens import savebackup

VPP_TOKEN = {
    "value": [{
        "id": "0",
        "tokenName": "test",
        "displayName": "test"
    }]}


@patch("src.IntuneCD.backup_vppTokens.savebackup")
@patch("src.IntuneCD.backup_vppTokens.makeapirequest",
       return_value=VPP_TOKEN)
class TestBackupVPPTokens(unittest.TestCase):
    """Test class for backup_vppTokens."""

    def setUp(self):
        self.directory = TempDirectory()
        self.directory.create()
        self.token = 'token'
        self.saved_path = f"{self.directory.path}/Apple VPP Tokens/test."
        self.expected_data = {"tokenName": "test", "displayName": "test"}

    def tearDown(self):
        self.directory.cleanup()

    def test_backup_yml(self, mock_data, mock_makeapirequest):
        """The folder should be created, the file should have the expected contents, and the count should be 1."""

        self.count = savebackup(self.directory.path, 'yaml', self.token)

        with open(self.saved_path + 'yaml', 'r') as f:
            data = json.dumps(yaml.safe_load(f))
            self.saved_data = json.loads(data)

        self.assertTrue(
            Path(f'{self.directory.path}/Apple VPP Tokens').exists())
        self.assertEqual(self.expected_data, self.saved_data)
        self.assertEqual(1, self.count)

    def test_backup_json(self, mock_data, mock_makeapirequest):
        """The folder should be created, the file should have the expected contents, and the count should be 1."""

        self.count = savebackup(self.directory.path, 'json', self.token)

        with open(self.saved_path + 'json', 'r') as f:
            self.saved_data = json.load(f)

        self.assertTrue(
            Path(f'{self.directory.path}/Apple VPP Tokens').exists())
        self.assertEqual(self.expected_data, self.saved_data)
        self.assertEqual(1, self.count)

    def test_backup_with_no_return_data(self, mock_data, mock_makeapirequest):
        """The count should be 0 if no data is returned."""

        mock_data.return_value = {"value": []}
        self.count = savebackup(self.directory.path, 'json', self.token)
        self.assertEqual(0, self.count)


if __name__ == '__main__':
    unittest.main()
