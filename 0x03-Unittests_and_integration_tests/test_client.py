#!/usr/bin/env python3
"""Unit tests for GithubOrgClient.org
"""
import unittest
from unittest.mock import patch
from parameterized import parameterized

from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Tests for the GithubOrgClient class"""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch('client.get_json')
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns the expected result
        and calls get_json once with the correct URL.
        """
        # Arrange
        expected_url = f"https://api.github.com/orgs/{org_name}"
        expected_payload = {"login": org_name, "id": 123}
        mock_get_json.return_value = expected_payload

        # Act
        client = GithubOrgClient(org_name)
        result = client.org()

        # Assert
        self.assertEqual(result, expected_payload)
        mock_get_json.assert_called_once_with(expected_url)


if __name__ == '__main__':
    unittest.main()
