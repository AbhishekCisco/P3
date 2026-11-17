import pytest

from priority_score import calculate_priority_score


@pytest.mark.parametrize(
    ("severity", "expected_score"),
    [
        ("critical", 68),
        ("warning", 38),
        ("info", 18),
    ],
)
def test_calculate_priority_score_above_threshold(
    severity: str,
    expected_score: int,
) -> None:
    score = calculate_priority_score(severity, metric_value=120.0, threshold=100.0)

    assert score == expected_score
    assert isinstance(score, int)
