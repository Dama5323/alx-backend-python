# 🧪 Unittests and Integration Tests

This project demonstrates how to implement **unit tests** and **integration tests** in Python, with a focus on parameterized testing, mocking, patching, and test organization. All code adheres to the **PEP 8** style guide, using **pycodestyle 2.5** for enforcement.

---

## 🚀 Overview

The project includes tests for utility functions and a GitHub client class. These tests demonstrate:

1. **Parameterized Testing** – with the `parameterized` package
2. **Mocking** – isolating tests from external dependencies using `unittest.mock`
3. **Patching** – replacing objects or methods during runtime for controlled testing
4. **Fixtures** – providing consistent test data using local JSON structures
5. **Integration Testing** – testing full workflows with controlled mock responses

---

## 📂 Files Structure

- `utils.py`  
  Utility functions:
  - `access_nested_map`: Traverse nested dictionaries using key paths
  - `get_json`: Fetch and parse JSON from a URL
  - `memoize`: Decorator to cache method results

- `client.py`  
  GitHub API client:
  - `GithubOrgClient`: Fetches data related to GitHub organizations

- `test_utils.py`  
  Unit tests for utilities:
  - `TestAccessNestedMap`
  - `TestGetJson`
  - `TestMemoize`

- `test_client.py`  
  Unit and integration tests for the GitHub client:
  - `TestGithubOrgClient`
  - `TestIntegrationGithubOrgClient`

- `fixtures.py`  
  Contains reusable fixture payloads for testing.

---

## 🧪 Testing Techniques Demonstrated

### ✅ Parameterized Testing

```python
@parameterized.expand([
    ({"a": 1}, ("a",), 1),
    ({"a": {"b": 2}}, ("a",), {"b": 2}),
    ({"a": {"b": 2}}, ("a", "b"), 2),
])
def test_access_nested_map(self, nested_map, path, expected):
    self.assertEqual(access_nested_map(nested_map, path), expected)
```

---

### 🔄 Mocking HTTP Requests

```python
@patch('requests.get')
def test_get_json(self, mock_get):
    mock_response = Mock()
    mock_response.json.return_value = test_payload
    mock_get.return_value = mock_response

    self.assertEqual(get_json(test_url), test_payload)
    mock_get.assert_called_once_with(test_url)
```

---

### 🏷 Testing with PropertyMock

```python
with patch('client.GithubOrgClient.org', new_callable=PropertyMock) as mock_org:
    mock_org.return_value = payload
    self.assertEqual(org_client._public_repos_url, expected_url)
```

---

### 🔗 Integration Testing with Fixtures

```python
@parameterized_class(
    ('org_payload', 'repos_payload', 'expected_repos', 'apache2_repos'),
    TEST_PAYLOAD
)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.get_patcher = patch('requests.get')
        cls.mock_get = cls.get_patcher.start()

    @classmethod
    def tearDownClass(cls):
        cls.get_patcher.stop()
```

---

## 🧪 Running Tests

Run individual test files:

```bash
python3 -m unittest test_utils.py
python3 -m unittest test_client.py
```

Run all tests recursively:

```bash
python3 -m unittest discover
```

---

## ✅ Style Guide Compliance

All code is checked using `pycodestyle`:

```bash
pycodestyle utils.py test_utils.py client.py test_client.py
```

---

## 👤 Author

Part of the **ALX Software Engineering Program** – Back-End Python Curriculum.
