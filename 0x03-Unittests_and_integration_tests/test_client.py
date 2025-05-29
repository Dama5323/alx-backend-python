#!/usr/bin/env python3
"""Unit tests for client module"""
import unittest
import requests
from parameterized import parameterized, parameterized_class
from unittest.mock import patch, PropertyMock, Mock
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD


class TestGithubOrgClient(unittest.TestCase):
    """Test case for GithubOrgClient class"""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch('client.get_json')
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns the correct value"""
        client = GithubOrgClient(org_name)
        expected_response = {
            "name": org_name,
            "repos_url": f"https://api.github.com/orgs/{org_name}/repos"
        }
        mock_get_json.return_value = expected_response

        result = client.org
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )
        self.assertEqual(result, expected_response)

    def test_public_repos_url(self):
        """Test the _public_repos_url property"""
        expected_url = "https://api.github.com/orgs/testorg/repos"
        payload = {"repos_url": expected_url}

        org_client = GithubOrgClient("testorg")

        with patch('client.GithubOrgClient.org',
                   new_callable=PropertyMock) as mock_org:
            mock_org.return_value = payload
            repos_url = org_client._public_repos_url
            self.assertEqual(repos_url, expected_url)

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """Test the public_repos method"""
        test_payload = [
            {"name": "repo1"},
            {"name": "repo2"},
            {"name": "repo3"}
        ]
        mock_get_json.return_value = test_payload
        expected_repos = ["repo1", "repo2", "repo3"]

        org_client = GithubOrgClient("testorg")

        with patch('client.GithubOrgClient._public_repos_url',
                   new_callable=PropertyMock) as mock_public_repos_url:
            mock_url = "https://api.github.com/orgs/testorg/repos"
            mock_public_repos_url.return_value = mock_url

            repos = org_client.public_repos()
            self.assertEqual(repos, expected_repos)
            mock_public_repos_url.assert_called_once()
            mock_get_json.assert_called_once_with(mock_url)

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test the has_license static method"""
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected)


@parameterized_class(
    ('org_payload', 'repos_payload', 'expected_repos', 'apache2_repos'),
    TEST_PAYLOAD
)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient class"""

    @classmethod
    def setUpClass(cls):
        """Set up for the integration tests"""
        def get_json_side_effect(url):
            mock_response = Mock()
            if url == "https://api.github.com/orgs/google":
                mock_response.json.return_value = cls.org_payload
            elif url == "https://api.github.com/orgs/google/repos":
                mock_response.json.return_value = cls.repos_payload
            return mock_response

        cls.get_patcher = patch(
            'requests.get',
            side_effect=get_json_side_effect
        )
        cls.get_patcher.start()

    @classmethod
    def tearDownClass(cls):
        """Tear down for the integration tests"""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test the public_repos method returns the expected repos"""
        client = GithubOrgClient("google")
        repos = client.public_repos()
        self.assertEqual(repos, self.expected_repos)

    def test_public_repos_with_license(self):
        """Test the public_repos method with license filter"""
        client = GithubOrgClient("google")
        repos = client.public_repos(license="apache-2.0")
        self.assertEqual(repos, self.apache2_repos)


if __name__ == "__main__":
    unittest.main()
