import os

from locust import HttpUser, between, task
from locust.exception import StopUser


def required_environment_variable(name: str) -> str:
    value = os.getenv(name)

    if not value:
        raise RuntimeError(
            f"Missing required environment variable: {name}. "
            f"Set {name} before running Locust."
        )

    return value


LOAD_EMAIL = required_environment_variable("SCALEPASS_LOAD_EMAIL")
LOAD_PASSWORD = required_environment_variable("SCALEPASS_LOAD_PASSWORD")
LOAD_EVENT_ID = required_environment_variable("SCALEPASS_LOAD_EVENT_ID")


class ScalePassUser(HttpUser):
    wait_time = between(0.5, 1.5)

    def on_start(self) -> None:
        with self.client.post(
            "/login",
            data={
                "email": LOAD_EMAIL,
                "password": LOAD_PASSWORD,
            },
            name="POST /login",
            allow_redirects=False,
            catch_response=True,
        ) as response:
            if response.status_code != 303:
                response.failure(
                    f"Expected 303 after login, received {response.status_code}"
                )
                raise StopUser()

    @task(6)
    def list_events(self) -> None:
        with self.client.get(
            "/api/events",
            name="GET /api/events",
            catch_response=True,
        ) as response:
            if response.status_code != 200:
                response.failure(
                    f"Expected 200 for event list, received {response.status_code}"
                )

    @task(3)
    def view_event(self) -> None:
        with self.client.get(
            f"/events/{LOAD_EVENT_ID}",
            name="GET /events/[event_id]",
            catch_response=True,
        ) as response:
            if response.status_code != 200:
                response.failure(
                    f"Expected 200 for event detail, received {response.status_code}"
                )

    @task(1)
    def buy_ticket(self) -> None:
        with self.client.post(
            f"/events/{LOAD_EVENT_ID}/buy",
            data={"quantity": "1"},
            name="POST /events/[event_id]/buy",
            allow_redirects=False,
            catch_response=True,
        ) as response:
            if response.status_code != 303:
                response.failure(
                    f"Expected 303 after purchase, received {response.status_code}"
                )