# Safety Model

The project is designed around safe automation.

The agent can analyze, score, and prepare draft replies, but it should not silently act on behalf of the user.

## Principles

1. Human review is the default.
2. Drafts are preparation, not execution.
3. Risky cases are blocked or routed to review.
4. Missing information should trigger clarification, not blind execution.
5. External marketplace automation must be explicit, limited, and auditable.

## Blocked by default

- Automatic message sending
- Automatic proposal submission
- Off-platform communication suggestions
- High-risk or unclear orders
- Low-budget tasks with suspicious wording

## Review triggers

An order requires review when:

- risk level is medium or high;
- task type is unknown;
- description is too short;
- budget is missing or too low;
- risky keywords are detected;
- the generated draft needs user approval.

## Future safety improvements

- Add audit logs for every decision
- Add approval queue with explicit user confirmation
- Add policy checks before any external write-action
- Add per-platform compliance rules
- Add test cases for adversarial order descriptions