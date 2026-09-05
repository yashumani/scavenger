# Development status

Cycle: 0.2.0-rc.1 public-release preparation, 2026-09-05.

## Published preparation work

[Pull request #1](https://github.com/yashumani/scavenger/pull/1) was merged into `main` as commit `c435b8cfc068e72e59673db95f7a19baa4967c5c`. The reviewed candidate head is `f563cc0315acd09e6074ce1de997e4e4a7647b9f`; its 49-file source tree is `142a05b70a93e47b570b5266822d3e87e9bd7b3a`, matching the locally tested files byte-for-byte.

The work adds bounded parsing, strict URL/record checks, safer workspace writes, adversarial and integration tests, deterministic simulations, reproducible allowlisted packaging, MIT licensing, public onboarding, contributor/security policies, and a pre-mortem. The research-through-handoff scope remains unchanged. Merging this preparation is not a stable release or a supported-host certification.

## Local observations

Python 3.13.5 on Linux: **76 unit/integration tests passed**, with zero skips. The original 30-test suite remains included. Simulations passed 12 named scenarios, all 243 gate-state combinations, and 1,000 invalid-score mutations using seed 20260905. Two package builds were byte-identical, manifest verification passed, and five commands succeeded using extracted helpers from an unrelated working directory.

Branch-enabled coverage.py reported **91% combined coverage**: approximately 93% statement coverage and 85% branch coverage across developer/runtime scripts. This is in-process coverage; separate CLI subprocesses were not instrumented. Independent PyYAML parsing accepted the actual skill frontmatter and YAML configuration. Counts, scope, and runtime content hashes are recorded in [local validation](../reports/local-validation.json).

## Observed pull-request validation

[Validate Scavenger run 33992545726](https://github.com/yashumani/scavenger/actions/runs/33992545726) completed successfully for head `f563cc0315acd09e6074ce1de997e4e4a7647b9f`. GitHub checked out PR test-merge commit `32e370f8420516e9b93f2ae7c78ea7eac696f63a`, combining that head with base `26bb48956bafa843e4ebaa3d98b23681d2dca4d0`.

| Configuration | Observed outcome |
| --- | --- |
| Ubuntu / Python 3.11 | All validation, tests, simulation, and package-check steps passed. |
| Ubuntu / Python 3.12 | All validation, tests, simulation, and package-check steps passed. |
| Ubuntu / Python 3.13 | All validation, tests, simulation, and package-check steps passed. |
| macOS / Python 3.13 | All validation, tests, simulation, and package-check steps passed. |
| Windows / Python 3.13 | All steps passed; 76 tests discovered, 71 passed and five POSIX-specific cases explicitly skipped. |

[CodeQL run 33992545759](https://github.com/yashumani/scavenger/actions/runs/33992545759) also completed successfully for this head, including the step requiring a produced SARIF file and zero reported findings. This is scoped first-party static-analysis evidence, not an independent audit or proof that no vulnerabilities exist.

## Packaging defect caught and corrected

The first CI pass exposed a different Windows ZIP hash despite passing functional tests. Adding LF checkout normalization in `.gitattributes` corrected the cross-platform byte difference. The revised Windows job `101377220341` and the local Linux build produced the same 49-file package SHA-256:

```text
98294b99d6ec44299ef633b6fed3b214d9f31c9ff0ac0a33f3b0362d12f953cc
```

That hash applies to the exact candidate snapshot above, before this evidence-document update. Later documentation changes alter the package hash. Checksums are not publisher signatures. The package contains no production credentials, model weights, or third-party candidate implementations by design; its limited pattern lint is not comprehensive secret scanning.

## Evidence boundary and open launch gates

This follow-up changes only the status document. The remote results above are tied to the exact tested candidate and PR merge revision; they are not falsely attributed to an unobserved subsequent commit or a future release.

No stable tag/release, installed-agent certification, full live research pilot, rendered/generated-image validation, independent security audit, or owner-administered security-setting change is claimed. Main was unprotected and rulesets were empty at inspection; private-reporting and secret-protection status were not verified. Twelve host-evaluation cases are prepared but remain not-run.

[Issue #2](https://github.com/yashumani/scavenger/issues/2) tracks the repository controls and live/host validation still required before broad promotion. See [release readiness](RELEASE-READINESS.md), [validation details](VALIDATION.md), and [the pre-mortem](PREMORTEM.md).
