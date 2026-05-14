# Architecture

Freelance AI Agent is organized as a small deterministic pipeline. The goal is to keep the product logic transparent and easy to test before adding external integrations or LLM calls.

## Pipeline

```text
Raw order JSON
  -> parser
  -> scoring engine
  -> decision router
  -> draft generator
  -> safety guard
  -> human review output
```

## Modules

### parser.py

Normalizes raw JSON into a `FreelanceOrder` object. It keeps input handling isolated from the scoring and routing logic.

### scoring.py

Detects task type, calculates a relevance score, assigns risk level, and returns the final decision:

- `bid` — good candidate;
- `ask` — candidate needs clarification;
- `review` — unclear or medium-risk case;
- `reject` — weak or risky order.

### draft_generator.py

Creates first-response drafts based on the decision and task type. Drafts are not sent automatically.

### safety_guard.py

Blocks write-actions by default. The current public version routes all meaningful actions to human review.

### pipeline.py

Combines all modules into one flow and returns an `AgentResult` object.

## Why deterministic first

The first version uses clear rule-based logic. This makes the agent easier to test, explain, debug, and improve. LLM-based generation can be added later behind the same safety layer.