# Test Plan: Restful-Booker API

| | |
|---|---|
| **Document version** | 1.0 |
| **Author** | Sri Varshini Chary |
| **Date** | 10-Nov-2026 |
| **Application under test** | Restful-Booker public demo API (https://restful-booker.herokuapp.com) |
| **API documentation** | https://restful-booker.herokuapp.com/apidoc/index.html |

## 1. Introduction
This plan describes how the Restful-Booker booking API is tested: what is covered, how, with which tools, and when testing is considered complete.

## 2. Objectives
- Verify that each endpoint behaves as documented (functional correctness).
- Verify authentication and authorisation rules on protected endpoints.
- Verify input validation and error handling.
- Verify that response times and error rates stay acceptable under moderate load.
- Report defects clearly, with steps to reproduce, so they can be fixed and retested.

## 3. Scope
**In scope**
- Endpoints: `POST /auth`, `POST /booking`, `GET /booking`, `GET /booking/{id}`, `PUT /booking/{id}`, `PATCH /booking/{id}`, `DELETE /booking/{id}`, `GET /ping`
- Functional, negative, regression, JSON schema and header checks
- Light load testing (up to 100 virtual users)

**Out of scope**
- Security penetration testing and stress or soak testing (the target is a shared public demo service)
- UI testing (covered by the separate SauceDemo UI project)
- Data privacy and compliance testing

## 4. Requirements under test
See `traceability-matrix.md` for the full mapping (REQ-01 to REQ-10) to test cases.

## 5. Test approach
| Type | Approach | Tool |
|---|---|---|
| Functional | Each endpoint tested with valid input and checked for status, body, headers | pytest + requests, Postman |
| Negative | Missing or invalid token, missing fields, malformed body, non-existent ids | pytest, Postman |
| Schema | Response bodies validated against JSON schemas | jsonschema |
| Data-driven | Parametrized data sets including boundary values and special characters | pytest parametrize |
| Regression | Full automated suite re-run on every push and weekly | GitHub Actions |
| Exploratory / manual | Business-rule checks such as negative prices and reversed dates | Postman |
| Performance | Load test of list, create and get flows | JMeter |

## 6. Test environment
- Public shared instance of Restful-Booker; data may be changed by other users, so every test creates and cleans up its own data.
- Python 3.x, pytest, requests, Postman and Newman, Apache JMeter 5.6+.
- Credentials: public demo account (admin / password123).

## 7. Entry criteria
- API reachable (`GET /ping` returns a response).
- Test data builders and framework set up; Postman environment imported.

## 8. Exit criteria
- 100% of High-priority test cases executed.
- No open Critical or High severity defects, or each has an agreed workaround.
- Automated regression suite passes, apart from documented known defects.
- Load test: error rate below 1% and 90th percentile response time within target (TC-032, TC-033).

## 9. Severity and priority
| Severity | Meaning |
|---|---|
| Critical | Core function unusable, data loss or security hole |
| High | Major function wrong, no workaround |
| Medium | Function wrong, workaround exists |
| Low | Cosmetic or convention issue (for example a non-standard status code) |

Priority (High / Medium / Low) is the order in which the defect should be fixed, set with the product owner.

## 10. Risks and mitigation
| Risk | Impact | Mitigation |
|---|---|---|
| Shared public API may be slow, down or reset | Flaky results | Re-run, record timestamps, keep response-time thresholds generous |
| Other users change shared data | False failures | Each test creates its own uniquely named data |
| Load testing a public service | Could disrupt other users | Keep load small (max 100 users, short duration) |
| Known API quirks differ from REST conventions | Tests could hide defects | Tests assert the actual behaviour and each deviation is logged as a bug |

## 11. Schedule (two one-week sprints)
| Sprint | Work |
|---|---|
| Sprint 1 | Requirements analysis, test cases, automated functional and negative suite, CI pipeline |
| Sprint 2 | Postman collection, manual business-rule checks, load tests, defect reporting, final report |

## 12. Deliverables
Test plan, test cases and traceability matrix, automated test suite, Postman collection, JMeter plan, bug reports, regression checklist, performance summary.

## 13. Defect lifecycle
New → Open → Fixed → Retested → Closed (or Reopened if the retest fails). Each defect carries severity, priority, environment, steps to reproduce, expected and actual results, and evidence.
