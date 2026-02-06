import pytest


def test_trend_schema_contract():
    """Ensure the trend fetcher returns a list of trend objects matching the API contract described
    in `specs/technical.md`.

    Expected contract (each trend should include at minimum):
      - trend_id: str
      - title: str
      - score: float
      - source: str
      - timestamp: str (ISO-8601)
      - tags: list[str]
      - metrics: dict with keys 'mentions' (int) and 'engagement' (float)
    """

    try:
        # Implementation placeholder - repo is expected to provide this
        from planner.trend_fetcher import fetch_trends
    except Exception as e:  # ImportError or ModuleNotFoundError
        pytest.fail("Missing implementation: planner.trend_fetcher.fetch_trends() - implement trend fetcher")

    trends = fetch_trends()
    assert isinstance(trends, list), "fetch_trends() must return a list"
    assert len(trends) > 0, "fetch_trends() must return at least one trend for contract tests"

    trend = trends[0]
    assert isinstance(trend, dict), "Each trend item must be a dict/object"

    required_keys = {
        "trend_id": str,
        "title": str,
        "score": (int, float),
        "source": str,
        "timestamp": str,
        "tags": list,
        "metrics": dict,
    }

    for key, expected_type in required_keys.items():
        assert key in trend, f"Missing required key '{key}' in trend"
        assert isinstance(trend[key], expected_type), f"'{key}' has wrong type"

    # metrics detail
    metrics = trend["metrics"]
    assert "mentions" in metrics and isinstance(metrics["mentions"], int)
    assert "engagement" in metrics and isinstance(metrics["engagement"], (int, float))
