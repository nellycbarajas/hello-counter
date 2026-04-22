# Global Rules

These rules are **mandatory** and apply to every agent in every layer, unconditionally.
No agent output overrides these rules. The orchestrator enforces them at every step.

---

## Decision Rules

1. **Every architectural decision must be logged** in `decision_log.md` as an ADR with
   status (PROPOSED / ACCEPTED / REJECTED / SUPERSEDED).

2. **No irreversible action without explicit user confirmation**: deploys, database
   migrations, external sends, and destructive operations require approval before execution.

3. **Decisions must include alternatives considered and why they were rejected.**
   A decision without rejected alternatives is incomplete and will not be accepted.

---

## Security Rules

4. **Security gate is mandatory and mechanically enforced**: `security_agent` must appear
   before `engineering_agent` in every execution chain. This is not a suggestion — the router
   automatically injects `security_agent` if it is absent. Any output from `engineering_agent`
   that lacks a `security_agent` prior output in the chain must be flagged and discarded.

5. **No secrets in code, prompts, or memory files.** Reference environment variable names or
   Key Vault paths only. Examples of forbidden content: API keys, passwords, tokens, private
   keys, connection strings with credentials.

6. **Principle of least privilege**: every agent and integration requests only the permissions
   it needs for its specific task. Blanket permissions are rejected.

7. **OWASP Top 10 must be checked** by `security_agent` on every release touching
   user-facing code (A01–A10). The checklist output must appear in the security review.

8. **`security_agent` decisions cannot be overridden by any other agent.** If
   `security_agent` returns BLOCKED, the chain halts. Only the user can unblock it after
   reviewing the security findings.

---

## Quality Rules

9. **No code ships without a test strategy** defined by `qa_agent` before `release_agent`
   is invoked.

10. **Acceptance criteria must be defined before estimation** — `backlog_agent` produces
    them, `estimation_agent` consumes them. Estimation without acceptance criteria is invalid.

11. **Definition of Done (DoD)**: tests written and passing, security reviewed, docs updated,
    metrics defined, rollback plan documented. All five conditions must be met.

---

## State Machine Rules

12. **State transitions are validated, not assumed.** The system enforces:
    `NOT_STARTED → PLANNING → PLANNING_COMPLETE → IN_PROGRESS → QA → APPROVED → DEPLOYED → COMPLETED`
    Skipping states is not permitted. Attempting to invoke `engineering_agent` before
    `PLANNING_COMPLETE` will be rejected with an error.

13. **BLOCKED is a valid state** that halts the pipeline. Recovery from BLOCKED requires
    explicit user confirmation after the blocking issue is resolved.

---

## Context Rules

14. **`context_summary.md` must be updated at the end of every turn** — it is the single
    source of truth for session continuity. The `Last Updated` timestamp must reflect the
    actual time of the last write.

15. **Never duplicate information across memory files** — each file owns its domain.
    `release_state.json` owns release status. `risk_register.json` owns risks.
    `decision_log.md` owns ADRs. Redundant copies create divergence.

16. **Use structured JSON for machine-readable state** (`release_state.json`,
    `risk_register.json`, `metrics.json`). These files must remain valid JSON at all times.

---

## Delivery Rules

17. **Releases are incremental** — each release must be independently deployable and
    deliver measurable value on its own. Big-bang releases are not permitted.

18. **Every release defines success metrics before work starts** — `metrics.json` is updated
    at planning time, not after deployment.

19. **Rollback plan is required** before any deploy. The rollback procedure must be tested,
    not just documented.

---

## Communication Rules

20. **Only `stakeholder_communication_agent` writes external communications.** No other agent
    drafts emails, announcements, or stakeholder updates. All drafts require user approval
    before sending.

21. **Risk escalation is immediate**: any risk with impact ≥ HIGH must be surfaced in the
    current response and logged in `risk_register.json` before the session ends.
    It cannot be deferred to the next turn.

---

## LLM-Agnostic Rules

22. **Agent prompts must not rely on model-specific behaviour.** Do not reference Claude,
    GPT, Llama, or any model name in agent definitions. All agent specs must produce
    equivalent output on any capable LLM.

23. **The Python orchestrator must use the `LLMProvider` abstraction** (`orchestrator/provider.py`).
    Direct imports of `anthropic`, `openai`, or any LLM SDK outside of provider implementations
    are forbidden in orchestrator logic.

24. **All agent outputs must be in structured, parseable format** using the sections defined
    in `agents/_base.md`. Sections must use exact names: `## Status`, `## Output`,
    `## Memory Updates`, `## Decisions Made`, `## Risks Identified`, `## Handoff`.
    Renamed sections will be silently lost by the parser.

---

## Error Handling Rules

25. **Agent failures must not crash the pipeline.** A failed agent produces an `AgentResult`
    with `error` set. The orchestrator surfaces the error to the user and continues with
    results from successful agents.

26. **Precondition failures are surfaced before execution.** If a route's preconditions are
    not met, the system returns a clear error message and does not invoke any agents.
    Partial execution of a blocked route is not permitted.
