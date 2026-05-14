from __future__ import annotations

from .models import FreelanceOrder


def parse_order(raw: dict) -> FreelanceOrder:
    """Convert raw JSON-like input into a normalized order object."""
    return FreelanceOrder(
        order_id=str(raw.get("order_id") or raw.get("id") or "unknown"),
        title=str(raw.get("title") or "").strip(),
        description=str(raw.get("description") or "").strip(),
        budget=_parse_budget(raw.get("budget")),
        client_rating=_parse_rating(raw.get("client_rating")),
        platform=str(raw.get("platform") or "generic"),
    )


def _parse_budget(value: object) -> int | None:
    if value is None or value == "":
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _parse_rating(value: object) -> float | None:
    if value is None or value == "":
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None
