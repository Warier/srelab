from fastapi.testclient import TestClient
from prometheus_client import CONTENT_TYPE_LATEST


def metric_value(
    metrics: str,
    metric_name: str,
    method: str,
    route: str,
    status_code: str,
) -> float:
    expected_labels = (
        f'method="{method}"',
        f'route="{route}"',
        f'status_code="{status_code}"',
    )

    for line in metrics.splitlines():
        if not line.startswith(f"{metric_name}{{"):
            continue

        if all(label in line for label in expected_labels):
            return float(line.rsplit(" ", maxsplit=1)[1])

    return 0.0


def test_catalog_request_generates_counter_and_histogram_count(
    client: TestClient,
) -> None:
    labels = {
        "method": "GET",
        "route": "/api/events",
        "status_code": "200",
    }

    metrics_before = client.get("/metrics").text
    counter_before = metric_value(
        metrics_before,
        "scalepass_http_requests_total",
        **labels,
    )
    histogram_count_before = metric_value(
        metrics_before,
        "scalepass_http_request_duration_seconds_count",
        **labels,
    )

    response = client.get("/api/events")

    assert response.status_code == 200

    metrics_after = client.get("/metrics").text
    counter_after = metric_value(
        metrics_after,
        "scalepass_http_requests_total",
        **labels,
    )
    histogram_count_after = metric_value(
        metrics_after,
        "scalepass_http_request_duration_seconds_count",
        **labels,
    )

    assert counter_after >= counter_before + 1
    assert histogram_count_after >= histogram_count_before + 1


def test_unmatched_route_uses_fixed_404_label(client: TestClient) -> None:
    labels = {
        "method": "GET",
        "route": "unmatched",
        "status_code": "404",
    }

    metrics_before = client.get("/metrics").text
    counter_before = metric_value(
        metrics_before,
        "scalepass_http_requests_total",
        **labels,
    )

    response = client.get("/nao-existe")

    assert response.status_code == 404

    metrics_after = client.get("/metrics").text
    counter_after = metric_value(
        metrics_after,
        "scalepass_http_requests_total",
        **labels,
    )

    assert counter_after >= counter_before + 1


def test_metrics_endpoint_uses_prometheus_content_type_and_is_not_measured(
    client: TestClient,
) -> None:
    response = client.get("/metrics")

    assert response.status_code == 200
    assert response.headers["content-type"] == CONTENT_TYPE_LATEST
    assert 'route="/metrics"' not in response.text
