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
        # Create a new instance of GithubOrgClient with the provided org_name
        client = GithubOrgClient(org_name)

        # Call the org method
        client.org()

        # Check that get_json was called once with the expected URL
        expected_url = f"https://api.github.com/orgs/{org_name}"
        mock_get_json.assert_called_once_with(expected_url)

    def test_public_repos_url(self):
        """Test the _public_repos_url property"""
        # Define a known payload for org
        # This payload includes the repos_url
        expected_url = "https://api.github.com/orgs/testorg/repos"
        payload = {"repos_url": expected_url}

        # Create an instance of GithubOrgClient
        org_client = GithubOrgClient("testorg")

        # Use patch to mock the org property
        with patch('client.GithubOrgClient.org',
                   new_callable=PropertyMock) as mock_org:
            # Configure the mock to return our payload
            mock_org.return_value = payload

            # Access the _public_repos_url property
            repos_url = org_client._public_repos_url

            # Assert that it returns the expected URL from our mocked payload
            self.assertEqual(repos_url, expected_url)

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """Test the public_repos method"""
        # Create a test payload with repository data
        test_payload = [
            {"name": "repo1"},
            {"name": "repo2"},
            {"name": "repo3"}
        ]
        mock_get_json.return_value = test_payload

        # Expected list of repository names
        expected_repos = ["repo1", "repo2", "repo3"]

        # Create a client instance
        org_client = GithubOrgClient("testorg")

        # Mock the _public_repos_url property
        with patch('client.GithubOrgClient._public_repos_url',
                   new_callable=PropertyMock) as mock_public_repos_url:
            # Set the mock to return a specific URL
            mock_url = "https://api.github.com/orgs/testorg/repos"
            mock_public_repos_url.return_value = mock_url

            # Call the method under test
            repos = org_client.public_repos()

            # Assert the result is as expected
            self.assertEqual(repos, expected_repos)

            # Verify that the mocked methods were called correctly
            mock_public_repos_url.assert_called_once()
            mock_get_json.assert_called_once_with(mock_url)

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test the has_license static method"""
        # Call the static method with the provided inputs
        result = GithubOrgClient.has_license(repo, license_key)

        # Assert the result is as expected
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
        # Define the side effect function for requests.get.json()
        def get_json_side_effect(url):
            """Side effect function for requests.get"""
            # Mock response object with json method
            mock_response = Mock()

            # GitHub organization URL pattern
            if url.endswith('/google'):
                mock_response.json.return_value = cls.org_payload
            # GitHub repos URL pattern
            elif url.endswith('/google/repos'):
                mock_response.json.return_value = cls.repos_payload
            else:
                mock_response.json.return_value = {}

            return mock_response

        # Create the patcher for requests.get
        cls.get_patcher = patch(
            'utils.requests.get', side_effect=get_json_side_effect
        )

        # Start the patcher
        cls.mock_get = cls.get_patcher.start()

    @classmethod
    def tearDownClass(cls):
        """Tear down for the integration tests"""
        # Stop the patcher
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