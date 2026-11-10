"""Thin API client: all HTTP calls live here so tests read as behaviour."""
import requests

import config


class BookingClient:
    def __init__(self, base_url: str = config.BASE_URL, timeout: int = config.TIMEOUT):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update(
            {"Content-Type": "application/json", "Accept": "application/json"}
        )

    def _url(self, path: str) -> str:
        return f"{self.base_url}{path}"

    @staticmethod
    def _auth_cookie(token):
        return {"token": token} if token else None

    # ---- auth ----
    def create_token(self, username: str, password: str) -> requests.Response:
        return self.session.post(
            self._url("/auth"),
            json={"username": username, "password": password},
            timeout=self.timeout,
        )

    # ---- create ----
    def create_booking(self, payload: dict) -> requests.Response:
        return self.session.post(self._url("/booking"), json=payload, timeout=self.timeout)

    def create_booking_raw(self, raw_body: str) -> requests.Response:
        """Send a non-JSON body (for negative tests)."""
        return self.session.post(self._url("/booking"), data=raw_body, timeout=self.timeout)

    # ---- read ----
    def get_booking(self, booking_id: int) -> requests.Response:
        return self.session.get(self._url(f"/booking/{booking_id}"), timeout=self.timeout)

    def get_booking_ids(self, **filters) -> requests.Response:
        return self.session.get(self._url("/booking"), params=filters or None, timeout=self.timeout)

    # ---- update ----
    def update_booking(self, booking_id: int, payload: dict, token=None) -> requests.Response:
        return self.session.put(
            self._url(f"/booking/{booking_id}"),
            json=payload,
            cookies=self._auth_cookie(token),
            timeout=self.timeout,
        )

    def partial_update_booking(self, booking_id: int, payload: dict, token=None) -> requests.Response:
        return self.session.patch(
            self._url(f"/booking/{booking_id}"),
            json=payload,
            cookies=self._auth_cookie(token),
            timeout=self.timeout,
        )

    # ---- delete ----
    def delete_booking(self, booking_id: int, token=None) -> requests.Response:
        return self.session.delete(
            self._url(f"/booking/{booking_id}"),
            cookies=self._auth_cookie(token),
            timeout=self.timeout,
        )
