from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

TaskType = Literal["seo_text", "product_description", "rewrite", "research", "unknown"]
Decision = Literal["bid", "ask", "reject", "review"]
RiskLevel = Literal["low", "medium", "high"]


@dataclass(frozen=True)
class FreelanceOrder:
    """Normalized freelance order input."""

    order_id: str
    title: str
    description: str
    budget: int | None = None
    client_rating: float | None = None
    platform: str = "generic"


@dataclass(frozen=True)
class ScoreResult:
    """Scoring result used for routing and review."""

    task_type: TaskType
    score: int
    risk_level: RiskLevel
    decision: Decision
    reasons: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class AgentResult:
    """Final agent output for human review."""

    order_id: str
    task_type: TaskType
    decision: Decision
    score: int
    risk_level: RiskLevel
    draft_reply: str
    reasons: list[str]
    requires_human_review: bool
