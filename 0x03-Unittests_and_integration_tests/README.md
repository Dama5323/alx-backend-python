# Unittests and Integration Tests

This project demonstrates how to implement unit tests and integration tests in Python, focusing on parameterized tests, mock objects, fixtures, and proper test organization. The tests follow the PEP 8 style guide (enforced by pycodestyle 2.5).

## Overview

The project contains tests for utility functions and a GitHub client implementation, showcasing various testing techniques:

1. **Parameterized testing**: Using the `parameterized` package to run the same test with different inputs

2. **Integration tests**: Testing components working together while mocking external systems

## Files Structure

- `utils.py`: Utility functions to be tested
  - `access_nested_map`: Navigates nested dictionaries using a sequence of keys
  
- `client.py`: GitHub organization client implementation
  - `GithubOrgClient`: Client for accessing GitHub organization data

- `test_utils.py`: Unit tests for utility functions
  - `TestAccessNestedMap`: Tests for the access_nested_map function
    
- `test_client.py`: Unit and integration tests for the GitHub client
  - `TestGithubOrgClient`: Unit tests for GithubOrgClient class
  - `TestIntegrationGithubOrgClient`: Integration tests using parameterized fixtures

- `fixtures.py`: Test fixtures for the integration tests

## Testing Techniques Demonstrated

### Parameterized Testing
```python
@parameterized.expand([
    ({"a": 1}, ("a",), 1),
    ({"a": {"b": 2}}, ("a",), {"b": 2}),
    ({"a": {"b": 2}}, ("a", "b"), 2),
])
def test_access_nested_map(self, nested_map, path, expected):
    """Test that access_nested_map returns the expected result"""
    self.assertEqual(access_nested_map(nested_map, path), expected)
```


## Running the Tests

To run the tests, use the unittest framework:

```bash
python -m unittest test_utils.py
python -m unittest test_client.py
```

Or run all tests:

```bash
python -m unittest discover
```

## Style Compliance

All code and tests comply with PEP 8 style guide, as enforced by pycodestyle 2.5:

```bash
pycodestyle test_utils.py
pycodestyle test_client.py
```

## Author

ALX SE Program - Back-End Python Curriculum
