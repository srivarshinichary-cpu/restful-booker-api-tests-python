"""Test data builders: every test creates its own unique data."""
import uuid


def unique_suffix() -> str:
    return uuid.uuid4().hex[:8]


def build_booking(
    firstname=None,
    lastname=None,
    totalprice=250,
    depositpaid=True,
    additionalneeds="Breakfast",
    checkin="2026-12-01",
    checkout="2026-12-05",
) -> dict:
    return {
        "firstname": firstname or f"First{unique_suffix()}",
        "lastname": lastname or f"Last{unique_suffix()}",
        "totalprice": totalprice,
        "depositpaid": depositpaid,
        "bookingdates": {"checkin": checkin, "checkout": checkout},
        "additionalneeds": additionalneeds,
    }
