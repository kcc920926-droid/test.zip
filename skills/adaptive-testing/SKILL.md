---
name: adaptive-testing
description: "Choose and run proportionate validation for code changes, or optimize a slow test workflow. Keep small suites simple; introduce affected tests only when measured savings justify selection costs. Use when deciding which tests to run during implementation, before commit, or in CI."
---

# Adaptive Testing

Minimize time to trustworthy feedback, including agent decision time, startup, retries, and maintenance. Preserve required checks and coverage. Do not introduce a testing framework, modify hooks/CI, or weaken merge gates just to perform an ordinary code change.

These instructions are host-independent. Use the current agent's available file, shell, and test tools; no Codex-specific API or invocation syntax is required. Resolve supporting references relative to this skill directory. `agents/openai.yaml` is optional Codex UI metadata, not an execution dependency. Follow applicable host and project instructions, including the relevant `AGENTS.md`, `CLAUDE.md`, or `GEMINI.md`; this skill does not grant additional tool permissions.

## Cheap default

Read applicable project instructions and the existing test commands once. Check what commands actually execute: a command named `test` may include full E2E. Use existing duration records if available; otherwise observe the next necessary run. Do not run benchmarks merely to choose a policy.

Choose a mode once per work item. Test count is not a decision criterion. These are adjustable starting heuristics, not industry standards or deadlines:

| Comparable full fast-check duration | Default behavior |
| --- | --- |
| Unknown or at most 30 seconds | **Simple:** run the complete existing fast checks after a coherent behavior change. Do not build an impact map or scoring system. |
| Over 30 through 90 seconds | **Light:** keep simple execution unless an existing package/path filter clearly saves time. Do not introduce dependency-graph tooling. |
| Over 90 seconds repeatedly | **Selective candidate:** evaluate savings before adopting affected selection; being slow alone is insufficient. |

“Fast checks” means the project's routine lint/typecheck/unit checks, including cheap deterministic contract tests when already grouped there. It does not mean full E2E or the browser matrix. Pure documentation/non-runtime edits need only applicable checks. For bug diagnosis, run the reproducing test first in any mode.

Use the median of about five comparable ordinary runs when available, distinguishing cold and warm starts. With insufficient evidence, retain the simpler mode; do not collect extra runs solely for calibration. Keep the mode stable across individual edits. In the middle band, preserve an established effective mode rather than repeatedly switching.

Read [references/selective-validation.md](references/selective-validation.md) only when evaluating selective execution, implementing workflow changes, or resolving selection/cache uncertainty. If selection consumes the time it would save, use the broader existing command.

## Required scope, independent of mode

- Internal logic: unit checks and typecheck at the affected project/package scope, including consumers when needed.
- UI interaction: component tests; add relevant E2E when routing, browser behavior, or cross-layer integration needs verification. A text/style-only change does not automatically require E2E.
- API/service boundaries: contract/integration checks and affected user journeys as needed. Mock-only agreement is not provider compatibility evidence.
- Authentication, authorization, payments, migrations, or shared infrastructure: include domain-specific checks before merge even in a small project. A short suite is not evidence of low risk.
- Full E2E/regression: CI by default, or an explicit user request or applicable mandatory project requirement. Do not run it after every edit. Do not move necessary pre-merge coverage to nightly just to meet a time target.

## Execute without repetition

Work in coherent change batches, not per edited file. Diagnose a failure with its smallest reproducer. After fixing it, verify the reproducer and reconsider the scope affected by the fix; rerunning only previous failures is not completion evidence for everything else.

Reuse an existing trustworthy success only when all relevant inputs still match. Prefer the project's task cache. Do not invent a new cache for a small task. Check source/dependency inputs, tests, configuration, dependency versions, relevant environment, and tested snapshot; a commit SHA alone is insufficient. Do not cache shared-server/external-state E2E results by default. A working-tree pass does not automatically validate a partial staged commit.

Do not rerun an unchanged successful check just because the workflow reaches commit or push. Honor mandatory hooks and required CI checks; local success does not replace required CI evidence. Stop extending validation when applicable checks pass unless another change, failure, or unresolved concern warrants it.

Time targets never authorize dropping tests or reporting a timeout as success. A retry pass does not justify automatically editing product code, weakening assertions, or quarantining a test. Diagnose intermittent failures; any quarantine needs a documented reason, owner, expiry, and adequate critical-flow coverage.

Report briefly: chosen mode if useful, checks actually run and results, verified cache reuse, and any required validation still outstanding. Never report planned CI runs as completed. Avoid a lengthy test-selection analysis for a small change.
