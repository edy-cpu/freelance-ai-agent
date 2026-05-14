from __future__ import annotations

from .draft_generator import generate_draft_reply
from .models import AgentResult
from .parser import parse_order
from .safety_guard import requires_human_review
from .scoring import score_order


def process_order(raw_order: dict) -> AgentResult:
    """Run one raw order through parsing, scoring, draft generation, and safety routing."""
    order = parse_order(raw_order)
    score = score_order(order)
    draft = generate_draft_reply(order, score)

    return AgentResult(
        order_id=order.order_id,
        task_type=score.task_type,
        decision=score.decision,
        score=score.score,
        risk_level=score.risk_level,
        draft_reply=draft,
        reasons=score.reasons,
        requires_human_review=requires_human_review(score),
    )


def process_orders(raw_orders: list[dict]) -> list[AgentResult]:
    """Process multiple orders."""
    return [process_order(raw_order) for raw_order in raw_orders]
