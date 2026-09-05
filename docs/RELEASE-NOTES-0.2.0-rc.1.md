# Scavenger 0.2.0-rc.1 — community-review candidate

**Find what exists. Verify what fits. Design what is missing.**

This candidate opens Scavenger for source review, offline experimentation, and community contributions. It is not a stable supported-host release. The version is recorded in VERSION and SKILL.md; these notes do not create a Git tag or GitHub Release.

## What is included

A reusable requirements-first research skill, evidence and source-ledger templates, component relevance and reuse decisions, architecture/handoff guidance, and offline Python helpers. The original code and documentation are MIT-licensed. Contributor policies, security reporting guidance, issue forms, and a twelve-scenario pre-mortem are included.

The hardening cycle adds bounded parsing, strict URL/record validation, gate-aware scoring, safer workspace creation, no-overwrite and rollback checks, deterministic simulations, and an explicitly allowlisted reproducible package. No external Python runtime dependencies, LLM credentials, network client, or candidate-code executor are added to the offline helpers.

## Evidence and verification

The preparation revision passed 76 local unit/integration tests, 12 deterministic scenarios, 243 gate-state combinations, and 1,000 invalid-score mutations. Its five CI configurations and CodeQL analysis passed as recorded in [STATUS.md](STATUS.md). Windows explicitly skipped five POSIX-only tests. These are historical, scoped results rather than promises about every future commit.

Finalization leaves the runtime unchanged and adds downloadable GitHub Actions artifacts. For a candidate build, check both the **Validate Scavenger** and **CodeQL security analysis** outcomes for its exact commit. After all five validation configurations pass, the packaging job repeats package/simulation checks and publishes the versioned ZIP, `SHA256SUMS`, and `validation-evidence.json`. The evidence identifies the actual checkout, Git tree, run/attempt, helper checks, and scope limits. The artifact is retained for 30 days, subject to repository policy, and downloading requires GitHub sign-in. See [installation and verification](INSTALLATION.md).

The package's self-consistent manifest and hashes detect changes; they do not authenticate a publisher or certify research truth. GitHub's outer download container is not the reproducible inner ZIP. An artifact may exist before the separate CodeQL workflow finishes: inspect that workflow before relying on the build.

## Safe first use

Read the skill and scripts, run the synthetic offline demonstration, and create research output in a separate trusted directory. Use public or synthetic requirements for initial agent trials and restrict the host to authorized, read-only tools. Do not place production credentials or private client material in issues, public search queries, or test fixtures.

The helper validates declared structure and gate values. It does not verify citations, approve licenses, prove that tests ran, enforce agent permissions, or make a generated diagram accurate. Source inspection and scoped reviewer judgment remain necessary.

## Remaining gates and contributions

[Issue #2](https://github.com/yashumani/scavenger/issues/2) tracks main-branch protection, private vulnerability reporting, secret-protection settings, a full live research pilot, installed-host adversarial tests, and diagram/image validation. Do not close these based on green offline tests. No independent security audit or universal compatibility is claimed.

The most useful contributions are sanitized live-project walkthroughs, actual host test traces, focused regression cases, and evidence-backed rubric improvements. Follow [CONTRIBUTING.md](../CONTRIBUTING.md) and [SECURITY.md](../SECURITY.md). Report sensitive security details privately using the documented reporting process.

## Withdrawal and updates

For an unsafe candidate, disable it in the host, preserve sanitized evidence, and follow the [pre-mortem response plan](PREMORTEM.md). Future fixes must have their own tested revision and regenerated package; do not reuse an earlier checksum or silently rewrite a published version.
