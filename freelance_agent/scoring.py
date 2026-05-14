from __future__ import annotations

from .models import FreelanceOrder, ScoreResult, TaskType

TASK_KEYWORDS: dict[TaskType, set[str]] = {
    "seo_text": {"seo", "сео", "ключ", "ключевые", "оптимизация", "статья"},
    "product_description": {"товар", "карточка", "описание", "маркетплейс", "ozon", "wildberries"},
    "rewrite": {"рерайт", "переписать", "редактировать", "улучшить", "текст"},
    "research": {"исследование", "анализ", "собрать", "найти", "рынок", "конкуренты"},
    "unknown": set(),
}

RISK_KEYWORDS = {
    "срочно",
    "сегодня",
    "бесплатно",
    "тестовое",
    "без оплаты",
    "вне платформы",
    "telegram",
    "whatsapp",
    "перейти",
}


def detect_task_type(order: FreelanceOrder) -> TaskType:
    """Detect likely task type using transparent keyword rules."""
    text = f"{order.title} {order.description}".lower()
    best_type: TaskType = "unknown"
    best_hits = 0

    for task_type, keywords in TASK_KEYWORDS.items():
        hits = sum(1 for keyword in keywords if keyword in text)
        if hits > best_hits:
            best_type = task_type
            best_hits = hits

    return best_type


def score_order(order: FreelanceOrder) -> ScoreResult:
    """Score order relevance and route it to bid, ask, reject, or review."""
    reasons: list[str] = []
    score = 50

    task_type = detect_task_type(order)
    if task_type == "unknown":
        score -= 20
        reasons.append("Task type is unclear")
    else:
        score += 20
        reasons.append(f"Detected task type: {task_type}")

    if len(order.description) >= 120:
        score += 15
        reasons.append("Description has enough detail")
    elif len(order.description) >= 40:
        score += 5
        reasons.append("Description has partial detail")
    else:
        score -= 15
        reasons.append("Description is too short")

    if order.budget is None:
        score -= 10
        reasons.append("Budget is missing")
    elif order.budget >= 3000:
        score += 15
        reasons.append("Budget looks acceptable")
    elif order.budget >= 1000:
        score += 5
        reasons.append("Budget is low but possible")
    else:
        score -= 20
        reasons.append("Budget is too low")

    if order.client_rating is not None:
        if order.client_rating >= 4.5:
            score += 10
            reasons.append("Client rating is strong")
        elif order.client_rating < 3.5:
            score -= 10
            reasons.append("Client rating is weak")

    risk_hits = _risk_hits(order)
    if risk_hits:
        score -= 10 * min(len(risk_hits), 3)
        reasons.append("Risk keywords found: " + ", ".join(risk_hits[:3]))

    score = max(0, min(100, score))
    risk_level = _risk_level(score, risk_hits)
    decision = _decision(score, risk_level, task_type)

    return ScoreResult(
        task_type=task_type,
        score=score,
        risk_level=risk_level,
        decision=decision,
        reasons=reasons,
    )


def _risk_hits(order: FreelanceOrder) -> list[str]:
    text = f"{order.title} {order.description}".lower()
    return sorted(keyword for keyword in RISK_KEYWORDS if keyword in text)


def _risk_level(score: int, risk_hits: list[str]) -> str:
    if len(risk_hits) >= 2 or score < 35:
        return "high"
    if risk_hits or score < 60:
        return "medium"
    return "low"


def _decision(score: int, risk_level: str, task_type: TaskType) -> str:
    if risk_level == "high" or score < 35:
        return "reject"
    if task_type == "unknown" or risk_level == "medium":
        return "review"
    if score < 70:
        return "ask"
    return "bid"
