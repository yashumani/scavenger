# Validation evidence

Date: 2026-09-05. Scope: first-party release hardening of the Scavenger skill and offline helpers. No independent audit, live-model benchmark, or installed-host certification is claimed.

## Baseline and reproduced findings

The audited starting point was commit `26bb48956bafa843e4ebaa3d98b23681d2dca4d0`. The locally reconstructed original `scripts/scavenger.py` matched Git blob `9c946ac36df525e98081274525571ac5333eefa4` byte-for-byte before changes.

That original URL validator accepted an IP-literal local target, a trailing-dot localhost name, a reserved example subdomain in non-synthetic mode, a malformed port, and a terminal escape in a path. Its JSON loader accepted nonfinite JSON. These were input/metadata validation gaps, not observed network exploitation: the runtime did not fetch URLs. New tests exercise the corrected behavior.

## Reproduction commands

```sh
python scripts/scavenger.py check-skill .
python -m unittest discover -s tests -v
python scripts/scavenger.py validate examples/demo-record.json
python scripts/scavenger.py score examples/demo-record.json
python scripts/simulate.py
python scripts/release_check.py
```

The unit/integration suite covers record structure, gate/scoring invariants, control/URL parsing, nonfinite numbers, nesting and size limits, regular-file requirements, workspace concurrency/rollback/no-overwrite, CLI behavior, archive integrity, and extracted-package operation. POSIX-specific file-type/mode tests are explicitly skipped on unsupported systems, not reported as executed there.

The deterministic simulation checks 12 named scenarios, all 243 combinations of the five three-state gates, and 1,000 invalid-score mutations with seed 20260905. It runs zero LLMs and performs zero live research studies. A deliberate scenario documents that a plausible fabricated claim can pass structural validation; scoring still declares evidence truth unverified.

The package check builds twice from an explicit allowlist, compares exact bytes, verifies paths and per-file hashes, then executes five commands using its own extracted helpers from an unrelated working directory. It does not install the skill into an agent host.

## Observed results and exact revisions

See [STATUS.md](STATUS.md) for the recorded local test count, coverage boundary, CI run IDs, and commit-specific remote outcomes. Workflow configuration is not a passing run. The repository policy lint is a limited allowlist/AST/known-pattern check, not comprehensive secret scanning or SAST. CodeQL results, when observed, are separate evidence and do not replace review.

## Not completed by these checks

A full live project research pilot, installed-host activation and adversarial tool traces, diagram rendering, architecture-image generation/review, independent penetration testing, signed release attestations, and verification of owner-controlled security settings are not established by these tests. Host cases in `evals/host-cases.json` remain explicitly not-run. See [release readiness](RELEASE-READINESS.md) before making launch claims.
