#!/usr/bin/env python3
"""Test module for client.GithubOrgClient
"""
import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized
from client import GithubOrgClient
from unittest.mock import PropertyMock



class TestGithubOrgClient(unittest.TestCase):
    """Test class for GithubOrgClient
    """
    
    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch('client.get_json')
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns the correct value
        """
        # Set up the mock return value
        expected_response = {"name": org_name, "repos_url": f"https://api.github.com/orgs/{org_name}/repos"}
        mock_get_json.return_value = expected_response
        
        # Create the client instance
        client = GithubOrgClient(org_name)
        
        # Call the org property
        result = client.org
        
        # Assert that get_json was called once with the correct URL
        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")
        
        # Assert that the result is correct
        self.assertEqual(result, expected_response)

        self.assertEqual(result, expected_response)

    def test_public_repos_url(self):
        """Test that _public_repos_url returns the correct URL from the org payload"""
        # Test payload with known repos_url
        test_payload = {
            "repos_url": "https://api.github.com/orgs/test-org/repos",
            "other_data": "ignored"
        }

        # Create client instance
        client = GithubOrgClient("test-org")

        # Patch the org property to return our test payload
        with patch(
            'client.GithubOrgClient.org',
            new_callable=PropertyMock,
            return_value=test_payload
        ) as mock_org:
            # Call the _public_repos_url property
            result = client._public_repos_url

            # Verify the org property was accessed
            mock_org.assert_called_once()

            # Verify we got the expected URL
            self.assertEqual(result, test_payload["repos_url"])

      
    