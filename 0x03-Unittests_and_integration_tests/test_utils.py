#!/usr/bin/env python3
"""Unit tests for utils.access_nested_map"""
import unittest
from parameterized import parameterized
from utils import access_nested_map
from unittest.mock import patch, Mock
from typing import Dict
from utils import get_json
from utils import memoize



class TestAccessNestedMap(unittest.TestCase):
    """Tests for access_nested_map function"""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """Test that access_nested_map returns the expected result"""
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",), "a"),
        ({"a": 1}, ("a", "b"), "b"),
    ])
    def test_access_nested_map_exception(self, nested_map, path, expected_key):
        """Test access_nested_map raises KeyError for invalid paths."""
        with self.assertRaises(KeyError) as context:
            access_nested_map(nested_map, path)
        self.assertEqual(str(context.exception), f"'{expected_key}'")

class TestGetJson(unittest.TestCase):
    """Test class for get_json function."""

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    def test_get_json(self, test_url: str, test_payload: Dict) -> None:
        """Test get_json returns expected result without making HTTP calls.
        
        Args:
            test_url: URL to mock
            test_payload: Expected JSON response
        """
        # Create a mock response with json() method
        mock_response = Mock()
        mock_response.json.return_value = test_payload

        # Patch requests.get to return our mock
        with patch('requests.get', return_value=mock_response) as mock_get:
            # Call the function
            result = get_json(test_url)

            # Assert the mock was called correctly
            mock_get.assert_called_once_with(test_url)

            # Assert we got the expected payload
            self.assertEqual(result, test_payload)


class TestMemoize(unittest.TestCase):
    """Test class for memoize decorator."""

    def test_memoize(self):
        """Test that memoize caches the result properly."""
        # Define the test class inside the test method
        class TestClass:
            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        # Create instance and mock a_method
        test_instance = TestClass()
        
        with patch.object(test_instance, 'a_method') as mock_method:
            mock_method.return_value = 42  # Set return value

            # First call - should call a_method
            result1 = test_instance.a_property
            self.assertEqual(result1, 42)

            # Second call - should use cached value
            result2 = test_instance.a_property
            self.assertEqual(result2, 42)            
        




if __name__ == '__main__':
    unittest.main()