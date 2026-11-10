# Regression Checklist

Run after every API change or deployment. Automated items run in CI on every push.

## Smoke (run first, about 1 minute)
- [ ] `GET /ping` responds
- [ ] `POST /auth` with valid credentials returns a token
- [ ] `POST /booking` creates a booking and returns an id
- [ ] `GET /booking/{id}` returns the created booking
- [ ] `PUT /booking/{id}` with a token updates the booking
- [ ] `DELETE /booking/{id}` with a token removes it (GET then returns 404)

Command: `pytest -m smoke`

## Full regression
- [ ] Authentication: valid and invalid credentials (TC-001 to TC-005)
- [ ] Create: valid, boundary and special-character data; missing fields; non-JSON body (TC-006 to TC-011)
- [ ] Read: list, get by id, 404, filters, headers, schema (TC-015 to TC-020)
- [ ] Update: PUT and PATCH with and without token (TC-022 to TC-026)
- [ ] Delete: with and without token, non-existent id (TC-028 to TC-030)

Command: `pytest -m regression`

## Manual checks (Postman or Newman)
- [ ] Run the whole collection: `newman run postman/restful-booker.postman_collection.json -e postman/restful-booker.postman_environment.json`
- [ ] Business rules: negative price, reversed dates, missing Accept header (TC-012 to TC-014)
- [ ] Filter by dates, PUT and DELETE on missing ids (TC-021, TC-027, TC-031)

## After a bug fix
- [ ] Re-run the exact steps from the bug report
- [ ] Re-run the related automated tests
- [ ] Re-run smoke, then full regression
- [ ] Update the bug status (Fixed → Retested → Closed)

## Performance (before release or when performance-related code changes)
- [ ] JMeter run with 50 users; compare with the previous results (TC-032)
