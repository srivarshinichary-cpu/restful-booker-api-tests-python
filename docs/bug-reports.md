# Bug Reports: Restful-Booker API

**Environment for all bugs:** https://restful-booker.herokuapp.com, tested with Postman and pytest, 10-Nov-2026.

**Verification column:** "Confirmed" means an automated test in the pytest suite already asserts the behaviour. "To verify" means reproduce it in Postman and attach a screenshot before submitting the bug.

| ID | Title | Severity | Priority | Verification |
|---|---|---|---|---|
| BUG-001 | Invalid login returns 200 instead of 401 | Medium | High | Confirmed |
| BUG-002 | Successful DELETE returns 201 Created | Low | Low | Confirmed |
| BUG-003 | Missing mandatory fields on create produce a server error instead of 400 | Medium | High | Error status confirmed; exact code to verify |
| BUG-004 | Missing token returns 403 instead of 401 | Low | Low | Confirmed |
| BUG-005 | Deleting a non-existent booking returns 405 instead of 404 | Low | Medium | To verify |
| BUG-006 | PUT without Accept header returns 418 | Low | Low | To verify |
| BUG-007 | Negative price and reversed dates are accepted | Medium | Medium | To verify |
| BUG-008 | Malformed JSON body returns 500 instead of 400 | Medium | Medium | To verify |

---

## BUG-001: Invalid login returns 200 instead of 401
- **Endpoint:** `POST /auth`
- **Steps to reproduce:**
  1. Send `POST /auth` with body `{"username": "admin", "password": "wrong"}`.
- **Expected:** 401 Unauthorized (or 400) with an error message, and no token.
- **Actual:** HTTP 200 with body `{"reason": "Bad credentials"}`.
- **Impact:** Clients that trust the status code treat a failed login as a success.
- **Suggested fix:** Return 401 for failed authentication.
- **Evidence:** pytest `test_invalid_credentials_are_rejected` (4 data sets); attach Postman screenshot.

## BUG-002: Successful DELETE returns 201 Created
- **Endpoint:** `DELETE /booking/{id}`
- **Steps:** Create a booking, then `DELETE /booking/{id}` with a valid token cookie.
- **Expected:** 200 OK or 204 No Content.
- **Actual:** 201 Created, which means a resource was created.
- **Suggested fix:** Return 204 (or 200) on successful delete.
- **Evidence:** pytest `test_delete_removes_booking`.

## BUG-003: Missing mandatory fields on create produce a server error instead of 400
- **Endpoint:** `POST /booking`
- **Steps:** Send `POST /booking` with body `{"firstname": "OnlyFirstName"}`.
- **Expected:** 400 Bad Request listing the missing fields.
- **Actual:** An error status of 400 or above is returned. Record the exact code you see (reported behaviour is 500 Internal Server Error) and attach the response body.
- **Impact:** A 5xx suggests a server fault, not a client mistake, and gives the client no guidance.
- **Suggested fix:** Validate the payload and return 400 with a clear message.
- **Evidence:** pytest `test_create_booking_with_missing_fields_fails`; Postman request "Create booking with missing fields".

## BUG-004: Missing token returns 403 instead of 401
- **Endpoints:** `PUT`, `PATCH`, `DELETE /booking/{id}`
- **Steps:** Call any of these without the `token` cookie.
- **Expected:** 401 Unauthorized, because the caller is not authenticated.
- **Actual:** 403 Forbidden.
- **Suggested fix:** Use 401 for missing credentials and keep 403 for authenticated users without permission.
- **Evidence:** pytest `test_put_without_token_is_forbidden`, `test_patch_without_token_is_forbidden`, `test_delete_without_token_is_forbidden_and_booking_remains`.

## BUG-005: Deleting a non-existent booking returns 405 instead of 404
- **Endpoint:** `DELETE /booking/999999999`
- **Steps:** Send the request with a valid token.
- **Expected:** 404 Not Found.
- **Actual (to verify):** 405 Method Not Allowed. Our automated test accepts 404 or 405, so confirm the exact code in Postman.
- **Suggested fix:** Return 404 when the resource does not exist.

## BUG-006: PUT without Accept header returns 418
- **Endpoint:** `PUT /booking/{id}`
- **Steps:** Send a valid PUT with a token cookie and no `Accept` header.
- **Expected:** The request succeeds, or a clear 4xx such as 406 or 415.
- **Actual (to verify):** 418 I'm a teapot, which has no meaning for this API.
- **Suggested fix:** Default to JSON when no Accept header is sent.
- **Evidence:** Postman request "PUT without Accept header".

## BUG-007: Negative price and reversed dates are accepted
- **Endpoint:** `POST /booking`
- **Steps:**
  1. Send a valid booking with `"totalprice": -100`.
  2. Send a valid booking with `checkout` earlier than `checkin`.
- **Expected:** 400 Bad Request for both, because they break basic business rules.
- **Actual (to verify):** The booking is created (200).
- **Suggested fix:** Add server-side validation for price (>= 0) and date order.
- **Evidence:** Postman requests "Create booking with negative price" and "Create booking with checkout before checkin".

## BUG-008: Malformed JSON body returns 500 instead of 400
- **Endpoint:** `POST /booking`
- **Steps:** Send the raw body `this is not json` with `Content-Type: application/json`.
- **Expected:** 400 Bad Request.
- **Actual (to verify):** An error status is returned (reported behaviour: 500).
- **Evidence:** pytest `test_create_booking_with_non_json_body_fails`; Postman request "Create booking with invalid JSON".
