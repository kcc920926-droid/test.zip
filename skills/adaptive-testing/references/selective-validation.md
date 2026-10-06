# Selective validation and workflow optimization

Read this only for selective mode, a requested workflow optimization, or a concrete selection/cache issue. Do not make these steps a prerequisite for simple mode.

## Decide whether selection pays

Compare total feedback time, not test-body time or test count:

```text
Per-run saving = F - A - D
Net saving over a chosen period = N * (F - A - D) - I - M
```

- F: comparable complete fast-check wall time, including startup and retries.
- A: selected-check wall time, including the same categories of overhead.
- D: additional selection time, including agent reasoning and tool calls.
- N: expected normal runs during the chosen period.
- I: one-time setup effort, in comparable time units.
- M: expected maintenance effort during that period.

Separate measured values from estimates; do not invent timing or frequency. Use a practical horizon such as one or two working weeks if the project has no preference. Adopt selection when net savings are clearly positive, not a marginal estimate, and coverage can be maintained. No frequency threshold or timing threshold by itself authorizes new tooling.

Examples are illustrative, not measurements of the user's project:

| Situation | Decision |
| --- | --- |
| Full 18 s; selected 7 s; selection 12 s | Keep simple: selection makes the loop slower. |
| Full 60 s; existing package filter 18 s; selection 2 s | Use the existing filter; no new framework is needed. |
| Full 180 s; selected 30 s; selection 5 s; 10 runs/day | Candidate saves about 24 min/day before setup and maintenance costs. |
| Full 120 s; startup dominates; selected 110 s | Address startup/reuse first; selection has little room to help. |
| Thousands of tests finish in 20 s | Keep simple despite the test count. |
| A few external-state E2E tests take minutes | Improve fixtures/isolation/setup; do not assume a graph solves the delay. |

Inspect existing logs to separate startup/build/DB initialization, execution, and retries. Prefer existing runner filters, incremental builds, and valid task caching before introducing new infrastructure. Compare p50/p95 feedback time and retry rate when enough natural observations exist. Avoid claiming a meaningful p95 from five runs.

Revisit the mode after material suite/runtime changes, not each edit. If selective execution becomes slower than the broader command, fall back. If ordinary full fast checks remain below 30 seconds across several comparable runs, prefer simple mode again; keep useful existing cache/tooling rather than deleting it solely to change modes.

## Select conservatively

Use the union of:

1. Directly modified tests and tests for the bug or behavior being changed.
2. Tests of changed modules and reverse dependents.
3. Explicit mappings for HTTP, database, queue, runtime loading, and other boundaries the import graph cannot see.
4. Domain-specific mandatory checks for the change's risk.

Choose a diff appropriate to the task: working-tree changes include tracked and relevant untracked files; commit checks target the actual index; PR checks compare the intended base and head. Use the project's established integration baseline when one exists. Do not assume `HEAD~1` represents a multi-commit PR. Handle deletions and renames, including old owners where needed.

For executable changes with zero selected tests, unmapped files, uncertain dependencies, or changes to common fixtures/configuration/lockfiles, broaden to the affected package/domain. Expand further when the scope remains unclear. Documentation-only changes need not trigger a zero-selection fallback. Broader unit/integration checks and required CI regression remain available without defaulting every local ambiguity to full E2E.

During rollout, retain broad required CI checks on the same relevant code snapshot and compare failures against the selector's choices. Investigate failures outside the selected set and repair mappings. An affected-selector pass alone does not establish that full CI coverage can be removed. Add broad periodic regression according to the project's existing policy.

## Change workflow only within the request

When authorized to optimize hooks or CI, start with existing commands:

| Stage | Suggested responsibility |
| --- | --- |
| Implementation | Simple/light/selected fast checks after coherent changes; add risk-driven checks. |
| Commit | Staged lint and valid fast-check evidence for the staged content. |
| Push | Conditional integration/smoke when useful; avoid duplicating required CI mechanically. |
| PR / merge | Required validation on the appropriate snapshot; preserve broad coverage while proving selection. |
| Nightly | Wider regression/browser matrix and detection of selection misses; never a substitute for required pre-merge checks. |

Before reusing success, validate the complete task input closure and the environment assumptions. Missing cache keys or unknown external state mean run the check. Failed, interrupted, or partial runs are not successful cache entries.

For E2E, reuse authentication only outside tests of authentication itself. Isolate mutable accounts/data per worker or test. Reuse local servers only when their code/configuration is current and test state can be reset. Tune concurrency against actual CPU/DB capacity and observed failures. Use measured timeout distributions with headroom rather than cutting all timeouts arbitrarily.

Full E2E stays in CI unless explicitly requested or mandated by applicable project instructions. Explain any unresolved required check rather than silently bypassing it.
