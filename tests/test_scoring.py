from freelance_agent.models import FreelanceOrder
from freelance_agent.scoring import detect_task_type, score_order


def test_detects_seo_text_task_type():
    order = FreelanceOrder(
        order_id="1",
        title="SEO текст для сайта",
        description="Нужна статья с ключевыми запросами и оптимизацией.",
        budget=4000,
    )

    assert detect_task_type(order) == "seo_text"


def test_good_order_gets_bid_decision():
    order = FreelanceOrder(
        order_id="1",
        title="SEO текст для сайта",
        description="Нужно подготовить SEO статью для страницы услуги. Есть ключевые запросы, структура и требования по объему.",
        budget=4500,
        client_rating=4.8,
    )

    result = score_order(order)

    assert result.decision == "bid"
    assert result.risk_level == "low"
    assert result.score >= 70


def test_risky_order_gets_rejected():
    order = FreelanceOrder(
        order_id="2",
        title="Срочно сегодня бесплатно тестовое",
        description="Оплата потом, сначала тестовое, лучше перейти в telegram.",
        budget=500,
        client_rating=3.0,
    )

    result = score_order(order)

    assert result.decision == "reject"
    assert result.risk_level == "high"
