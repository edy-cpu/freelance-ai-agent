from freelance_agent.pipeline import process_order, process_orders


def test_process_order_returns_human_review_output():
    result = process_order(
        {
            "order_id": "ord_test",
            "title": "SEO текст для сайта",
            "description": "Нужна SEO статья с ключевыми запросами, структурой и понятным результатом.",
            "budget": 4000,
            "client_rating": 4.7,
        }
    )

    assert result.order_id == "ord_test"
    assert result.task_type == "seo_text"
    assert result.draft_reply
    assert result.requires_human_review is True


def test_process_orders_handles_multiple_items():
    results = process_orders(
        [
            {
                "order_id": "1",
                "title": "Описание товара",
                "description": "Нужно описание карточки товара для маркетплейса с преимуществами.",
                "budget": 2500,
            },
            {
                "order_id": "2",
                "title": "Срочно бесплатно",
                "description": "Сначала тестовое без оплаты, потом обсудим.",
                "budget": 300,
            },
        ]
    )

    assert len(results) == 2
    assert results[0].order_id == "1"
    assert results[1].decision == "reject"
