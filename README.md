# Restful-Booker API Test Automation (Python)

API test automation framework for the public [Restful-Booker](https://restful-booker.herokuapp.com/apidoc/index.html) service, built with **Python, pytest, requests, jsonschema and GitHub Actions**.

## What it covers
| Area | Details |
|------|---------|
| CRUD | POST, GET, PUT, PATCH, DELETE on `/booking` |
| Authentication | Token from `/auth`, cookie-based auth, missing and invalid token cases |
| Validation | Status codes, headers, response body, response time, JSON schema |
| Data-driven | `pytest.mark.parametrize` for valid bookings and invalid credentials |
| Negative testing | Missing fields, malformed body, no/invalid token, non-existent ids |
| Reporting | Self-contained HTML report (pytest-html) |
| CI | GitHub Actions runs smoke then full regression on every push, PR and weekly |

## Design
- **Client layer** (`clients/booking_client.py`): one `requests.Session` with default headers; all endpoints wrapped as methods.
- **Fixtures** (`tests/conftest.py`): session-scoped `client` and `token`; a `new_booking` fixture that creates test data and cleans it up afterwards.
- **Data builder** (`utils/data_builder.py`): unique data per test, so tests are independent and can run in any order.
- **Schema validation** (`utils/schema.py` + `schemas/`): JSON schemas checked with `jsonschema`.
- **Markers**: `smoke`, `regression`, `negative`.
- **Config** (`config.py`): override with environment variables such as `BASE_URL`.

## Project structure
```
clients/booking_client.py
utils/data_builder.py, schema.py
schemas/booking.json, create_booking.json
tests/conftest.py, test_auth.py, test_create_booking.py,
      test_get_booking.py, test_update_booking.py, test_delete_booking.py
.github/workflows/api-tests.yml
pytest.ini, requirements.txt, config.py
```

## Run locally
Prerequisite: Python 3.9+.
```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt

pytest                             # everything
pytest -m smoke                    # smoke only
pytest -m negative                 # negative tests only
pytest -k "booking and not delete" # filter by name
```
The HTML report is written to `reports/report.html`.

## Known API behaviours (documented, not hidden)
- Bad credentials on `/auth` return HTTP 200 with `{"reason": "Bad credentials"}` instead of 401.
- A successful `DELETE` returns 201 instead of 200/204.
- Malformed `POST /booking` bodies return 500 instead of 400.

The tests assert the current behaviour and note where it deviates from REST conventions.

## Sample resume bullet
> Built a pytest and requests API automation framework with 30+ tests covering CRUD, authentication, JSON schema validation and negative cases, with HTML reporting and a GitHub Actions CI pipeline.
## 📊 Test Execution Report

The API automation test suite was executed successfully using Pytest and the pytest-html reporting plugin.

### Test Summary

| Metric | Result |
|---|---:|
| Total Test Cases | 28 |
| Passed | 28 |
| Failed | 0 |
| Skipped | 0 |
| Execution Time | 20 seconds |

### Test Report Summary

![Test Report Summary](screenshots/test-report-summary.png)

### Detailed Test Results

![Detailed Test Results](screenshots/test-report-details.png)

**Final Result:** 100% test execution success with all 28 test cases passed.