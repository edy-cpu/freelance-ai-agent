from __future__ import annotations

from .models import FreelanceOrder, ScoreResult


def generate_draft_reply(order: FreelanceOrder, score: ScoreResult) -> str:
    """Generate a concise first-response draft for human review."""
    if score.decision == "reject":
        return ""

    if score.decision == "review":
        return (
            "Здравствуйте! Перед тем как предложить точные сроки и стоимость, "
            "хочу уточнить несколько деталей по задаче. Можете, пожалуйста, подробнее описать результат, "
            "который хотите получить, и формат сдачи работы?"
        )

    if score.decision == "ask":
        return _clarification_reply(score)

    return _bid_reply(order, score)


def _bid_reply(order: FreelanceOrder, score: ScoreResult) -> str:
    task_hint = {
        "seo_text": "SEO-текст с учетом структуры, ключевых запросов и читаемости",
        "product_description": "описание товара с акцентом на преимущества и понятную структуру",
        "rewrite": "аккуратную переработку текста с сохранением смысла",
        "research": "краткий структурированный анализ с выводами",
        "unknown": "задачу после уточнения деталей",
    }[score.task_type]

    return (
        f"Здравствуйте! Могу выполнить: {task_hint}. "
        "Перед началом быстро уточню требования, затем подготовлю результат в понятном формате. "
        "Если нужно, могу предложить структуру и согласовать её перед выполнением."
    )


def _clarification_reply(score: ScoreResult) -> str:
    questions = {
        "seo_text": "Какие ключевые запросы, объем и целевая страница?",
        "product_description": "Для какой площадки описание и какие характеристики товара важны?",
        "rewrite": "Нужно сохранить исходный стиль или сделать текст более продающим/простым?",
        "research": "Какие источники можно использовать и какой формат результата нужен?",
        "unknown": "Какой итоговый результат нужен и в каком формате его нужно сдать?",
    }
    return "Здравствуйте! Готов посмотреть задачу. " + questions[score.task_type]
