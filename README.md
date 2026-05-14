# Freelance AI Agent

AI-powered assistant for freelance order analysis, relevance scoring, draft reply generation, and safe human-reviewed workflow.

The agent helps freelancers and small service teams reduce routine work: reading incoming orders, filtering weak or risky requests, preparing first-response drafts, and keeping risky actions blocked by default.

## Core Idea

Freelance marketplaces generate many low-quality or unclear requests. A freelancer still needs to make the final decision, but an agent can speed up the first layer of work:

1. parse the order text;
2. extract the likely task type and requirements;
3. score relevance, clarity, budget, and risk;
4. generate a draft reply or clarification questions;
5. route uncertain cases to manual review.

This project is built around **safe automation**: the agent can prepare decisions and drafts, but it does not auto-send anything.

## Features

- Order parsing from structured JSON fixtures
- Task type detection: SEO text, product description, rewrite, research, unknown
- Relevance and risk scoring
- Decision routing: `bid`, `ask`, `reject`, `review`
- Draft reply generation
- Safety guard for write-actions
- CLI pipeline for local runs
- Unit tests for scoring, safety, and pipeline behavior

## Architecture

```text
Input orders
   ↓
Parser
   ↓
Scoring Engine
   ↓
Decision Router
   ↓
Draft Generator
   ↓
Safety Guard
   ↓
Human Review Output
```

## Quick Start

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e .[dev]
python -m freelance_agent.cli --input fixtures/orders.json
pytest
```

## Example Output

```json
{
  "order_id": "ord_1001",
  "task_type": "seo_text",
  "decision": "bid",
  "score": 82,
  "risk_level": "low",
  "draft_reply": "Здравствуйте! Могу подготовить SEO-текст...",
  "requires_human_review": true
}
```

## Safety Model

The project intentionally separates preparation from execution.

- Draft generation is allowed.
- Scoring and routing are allowed.
- Automatic sending is blocked by default.
- High-risk or unclear cases go to manual review.
- Synthetic sample data is used in this public repository.

## Repository Structure

```text
freelance-ai-agent/
  freelance_agent/
    cli.py
    models.py
    parser.py
    scoring.py
    draft_generator.py
    safety_guard.py
    pipeline.py
  fixtures/
    orders.json
  tests/
    test_scoring.py
    test_safety_guard.py
    test_pipeline.py
  docs/
    architecture.md
    safety.md
  pyproject.toml
  README.md
```

## Product Direction

Possible next steps:

- Add a small operator dashboard
- Add persistent review queue storage
- Add LLM-based draft generation behind strict safety rules
- Add analytics: accepted/rejected/reviewed orders
- Add A/B testing for reply variants
- Add marketplace-specific adapters

## Status

Working MVP foundation with deterministic logic and synthetic data. The current focus is product logic, scoring, routing, and safety-first workflow rather than marketplace automation.