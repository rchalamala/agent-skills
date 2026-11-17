---
name: engineering
description: "Use for software engineering work: implementing changes, diagnosing defects, reviewing code, improving performance, or completing a pull request."
---

# Engineering

Own the requested outcome through verification and delivery. Use the harness's
native planning, tools, context management and task tracking. Keep related
reasoning in one loop. Delegate only independent work, a fresh verification
perspective, or work whose context would materially degrade this session.
Give delegates a bounded goal, relevant sources, ownership and acceptance
criteria; inspect their actual work before integrating it. A fresh context is
not evidence of a different model.

## Scope and design

Read the governing project instructions and relevant code before changing it.
Research discoverable facts yourself. Ask only for decisions or inputs that
change the result and cannot be established from available evidence. Continue
independent work while waiting. Existing authorization persists.

For clear bounded work, implement directly. For substantial work, establish the
outcome, constraints and executable acceptance criteria, then maintain one plan
with decisions, progress, commit references and the next action. Reconcile that
record with git and fresh observations when resuming; never redo work solely
because conversation history is missing. Keep durable project facts with the
project; use its established memory policy for personal information.

Use `codebase-design` for consequential interface decisions, `domain-modeling`
when terminology needs resolving, and `prototype` to settle an empirical design
question cheaply. `grill-me`, `grill-with-docs` and
`improve-codebase-architecture` are explicit interview/survey workflows, not
mandatory stages. Their outputs feed the existing plan rather than restarting
requirements discovery. Preserve agreed decisions unless new evidence disproves
them; surface material changes to the requested outcome.

## Implement and diagnose

Prefer deletion, reuse and the smallest coherent change. Test observable
behavior at meaningful interfaces. For behavioral code changes, use
`tdd` where a useful failing test is available. For
configuration, generated artifacts and throwaway experiments, use the relevant
build, evaluator, reproducible probe or runtime observation instead. This
selection is the testing policy for this plugin: do not ask merely to approve
an applicable exception, and do not delete working changes to reenact a test
sequence. Show that verification detects the failure it claims to catch.

Use `systematic-debugging` for non-obvious failures: reproduce, identify the
causal chain, test a specific hypothesis and verify the fix. For performance,
record the workload and baseline, identify the limiter, change one hypothesis
at a time, remeasure under comparable conditions and keep only demonstrated
improvements. Distinguish investigation from a confirmed diagnosis.

## Verify and finish

Use `verification-before-completion` before claiming success. Match each
acceptance criterion to executed evidence. Check the original requested outcome,
not only conformance to the plan: exercise real application flows, realistic
data and affected integration paths where relevant. Tests passing does not
establish that a UI works or an external configuration has been applied.

For substantial or consequential changes, get a fresh review of the integrated
diff against both the original request and project standards. Add specialist
or cross-model review only for an identified risk or unresolved disagreement.
Use `receiving-code-review` to validate feedback before implementing it. New
changes invalidate affected evidence; recheck them. Stop repeated fix loops to
reassess the premise rather than accumulating safeguards.

Carry authorized delivery through PR creation, CI and review-thread resolution.
Follow project merge and deployment boundaries. Resume from the actual PR head,
resolve independent work while other items are blocked, and report remaining
blockers precisely. Distinguish implemented, verified, published, merged and
applied state. Report meaningful changes, evidence and limitations without
claiming an unavailable reviewer, test or deployment ran.
