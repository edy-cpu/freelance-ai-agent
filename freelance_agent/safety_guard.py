from __future__ import annotations

from .models import ScoreResult


def can_auto_send(score: ScoreResult, *, enable_write_actions: bool = False) -> bool:
    """Return whether the agent is allowed to send anything automatically.

    By default this is always false. The public project keeps the agent in
    human-reviewed mode to avoid unsafe marketplace automation.
    """
    if not enable_write_actions:
        return False
    return score.decision == "bid" and score.risk_level == "low" and score.score >= 85


def requires_human_review(score: ScoreResult) -> bool:
    """All non-trivial decisions are routed to human review."""
    if score.decision in {"ask", "review", "reject"}:
        return True
    return not can_auto_send(score)
