# Backend Tests

This directory contains comprehensive backend tests for the FastAPI activity management system.

## Test Organization

Tests are organized by endpoint for easy navigation and maintenance:

- **test_get_activities.py** — Tests for the GET `/activities` endpoint
  - Retrieval of all activities
  - Response structure validation
  - Participant data verification

- **test_signup_for_activity.py** — Tests for the POST `/activities/{activity_name}/signup` endpoint
  - Successful signup scenarios
  - Duplicate signup prevention
  - Non-existent activity handling
  - Participant counter validation

- **test_remove_participant.py** — Tests for the DELETE `/activities/{activity_name}/participants/{email}` endpoint
  - Successful participant removal
  - Non-existent participant handling
  - Non-existent activity handling
  - Participant counter validation
  - Re-signup after removal

## Running Tests

### Run all tests
```bash
pytest tests/
```

### Run tests with verbose output
```bash
pytest tests/ -v
```

### Run a specific test file
```bash
pytest tests/test_get_activities.py
```

### Run a specific test function
```bash
pytest tests/test_signup_for_activity.py::test_signup_success
```

### Run tests and show coverage (requires pytest-cov)
```bash
pytest tests/ --cov=src.app
```

## Test Fixtures

Tests use the following shared fixtures defined in `conftest.py`:

- **client** — FastAPI TestClient for making requests to the application
- **reset_activities** — Fixture that resets the in-memory activities database to a clean state before and after each test, preventing state pollution

## Test Coverage

Current test coverage includes:

### GET /activities
- ✅ Successful retrieval of all activities
- ✅ Response structure validation
- ✅ Participant data verification
- ✅ Activity detail verification

### POST /activities/{activity_name}/signup
- ✅ Successful signup
- ✅ Duplicate email prevention
- ✅ Non-existent activity error handling
- ✅ Multiple different students signup
- ✅ Participant count increase verification

### DELETE /activities/{activity_name}/participants/{email}
- ✅ Successful participant removal
- ✅ Non-existent participant error handling
- ✅ Non-existent activity error handling
- ✅ Participant count decrease verification
- ✅ Remove all participants from an activity
- ✅ Re-signup after removal

## Setup

Make sure to install dependencies:
```bash
pip install -r requirements.txt
```

This will install pytest and all other required packages.

## Notes

- Tests use an in-memory database that is reset between each test via the `reset_activities` fixture
- All tests are integration tests that test endpoints via the FastAPI TestClient
- Tests follow a clear naming convention: `test_<scenario>` for easy identification of what is being tested
- Error cases (HTTP 400, 404) are tested alongside happy paths
