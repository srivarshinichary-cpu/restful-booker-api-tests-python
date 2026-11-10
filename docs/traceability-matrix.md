# Requirement Traceability Matrix

Every requirement maps to at least one test case, and every test case maps back to a requirement.

| Requirement | Description | Test cases | Automated | Manual / Perf | Coverage |
|---|---|---|---|---|---|
| REQ-01 | Authenticate and obtain a token (POST /auth) | TC-001, TC-002, TC-003, TC-004, TC-005 | 5 | 0 | Covered |
| REQ-02 | Create a booking (POST /booking) | TC-006, TC-007, TC-008, TC-009 | 4 | 0 | Covered |
| REQ-03 | Retrieve a booking by id (GET /booking/{id}) | TC-008, TC-016, TC-017 | 3 | 0 | Covered |
| REQ-04 | List and filter bookings (GET /booking) | TC-015, TC-018, TC-021 | 2 | 1 | Covered |
| REQ-05 | Fully update a booking with auth (PUT /booking/{id}) | TC-022, TC-023, TC-024, TC-027 | 3 | 1 | Covered |
| REQ-06 | Partially update a booking with auth (PATCH /booking/{id}) | TC-025, TC-026 | 2 | 0 | Covered |
| REQ-07 | Delete a booking with auth (DELETE /booking/{id}) | TC-028, TC-029, TC-030, TC-031 | 3 | 1 | Covered |
| REQ-08 | Input validation and error handling | TC-010, TC-011, TC-012, TC-013, TC-014 | 2 | 3 | Covered |
| REQ-09 | Performance: response time and behaviour under load | TC-019, TC-032, TC-033 | 1 | 2 | Covered |
| REQ-10 | Response format: JSON content type, headers and schema | TC-007, TC-014, TC-016, TC-020 | 3 | 1 | Covered |

**Totals:** 33 test cases (25 automated in pytest = 28 executed tests including 4 parametrized data sets in TC-009; 8 manual or performance).

Detailed steps and expected results are in `test-cases.csv`.
