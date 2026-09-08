from prometheus_client import Counter, Histogram

HTTP_REQUESTS = Counter(
    "scalepass_http_requests",
    "Total de requisições HTTP processadas pelo ScalePass.",
    labelnames=("method", "route", "status_code"),
)

HTTP_REQUEST_DURATION = Histogram(
    "scalepass_http_request_duration_seconds",
    "Duração das requisições HTTP processadas pelo ScalePass em segundos.",
    labelnames=("method", "route", "status_code"),
)


def observe_http_request(
    method: str,
    route: str,
    status_code: str,
    duration_seconds: float,
) -> None:
    labels = {
        "method": method,
        "route": route,
        "status_code": status_code,
    }

    HTTP_REQUESTS.labels(**labels).inc()
    HTTP_REQUEST_DURATION.labels(**labels).observe(duration_seconds)
