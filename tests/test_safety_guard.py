from freelance_agent.models import ScoreResult
from freelance_agent.safety_guard import can_auto_send, requires_human_review


def test_auto_send_disabled_by_default():
    score = ScoreResult(
        task_type="seo_text",
        score=95,
        risk_level="low",
        decision="bid",
        reasons=[],
    )

    assert can_auto_send(score) is False
    assert requires_human_review(score) is True


def test_low_quality_case_requires_review():
    score = ScoreResult(
        task_type="unknown",
        score=55,
        risk_level="medium",
        decision="review",
        reasons=[],
    )

    assert requires_human_review(score) is True
