#!/usr/bin/env python3
"""Test module for client.GithubOrgClient"""
import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Test class for GithubOrgClient"""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch('client.get_json')
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns the correct value"""
        expected_response = {
            "name": org_name,
            "repos_url": f"https://api.github.com/orgs/{org_name}/repos"
        }
        mock_get_json.return_value = expected_response
        
        client = GithubOrgClient(org_name)
        result = client.org
        
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )
        self.assertEqual(result, expected_response)

    def test_public_repos_url(self):
        """Test that _public_repos_url returns correct URL from org payload"""
        test_payload = {
            "repos_url": "https://api.github.com/orgs/test-org/repos",
            "other_data": "ignored"
        }

        client = GithubOrgClient("test-org")

        with patch(
            'client.GithubOrgClient.org',
            new_callable=PropertyMock,
            return_value=test_payload
        ) as mock_org:
            result = client._public_repos_url
            mock_org.assert_called_once()
            self.assertEqual(result, test_payload["repos_url"])

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """Test public_repos returns correct repos and applies license filter"""
        test_repos_payload = [
            {"name": "repo1", "license": {"key": "mit"}},
            {"name": "repo2", "license": {"key": "apache-2.0"}},
            {"name": "repo3", "license": None}
        ]
        
        mock_get_json.return_value = test_repos_payload
        test_url = "https://fake.url/repos"

        client = GithubOrgClient("test-org")

        with patch.object(
            GithubOrgClient,
            '_public_repos_url',
            new_callable=PropertyMock,
            return_value=test_url
        ) as mock_url:
            repos = client.public_repos()
            mock_url.assert_called_once()
            mock_get_json.assert_called_once_with(test_url)
            self.assertEqual(repos, ["repo1", "repo2", "repo3"])

            mock_get_json.reset_mock()
            repos = client.public_repos(license="mit")
            mock_get_json.assert_not_called()
            self.assertEqual(repos, ["repo1"])