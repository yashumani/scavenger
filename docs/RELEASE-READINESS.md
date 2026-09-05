# Release readiness: 0.2.0-rc.1

Target: public crowdsourcing and contributor review. This is a **release candidate**, not a declaration of independently audited security, universal host compatibility, or a completed stable launch.

## Gate checklist

| Gate | Evidence / state |
| --- | --- |
| Clear purpose, limits, and reproducible quick start | README and INSTALLATION.md implemented. |
| Distribution rights and provenance | MIT LICENSE, matching metadata, license decision, third-party notices. |
| Offline helper tests and adversarial simulations | Commands and exact observed results in VALIDATION.md. |
| Safe/reproducible packaging | Explicit allowlist, SHA-256 manifest, tamper/path tests, five extracted-helper commands; finalization adds a GitHub Actions artifact after the validation matrix. |
| CI and static analysis | Five validation configurations and CodeQL passed for the recorded preparation revision; see STATUS.md. Finalization changes require their own checks. |
| Contribution and responsible reporting | CONTRIBUTING, CODE_OF_CONDUCT, SECURITY, issue forms, PR template, CODEOWNERS. |
| Repository protections | OPEN: main was unprotected and rulesets empty at inspection on 2026-09-05. |
| Private vulnerability reporting | OPEN: availability could not be verified with the connector; enabling/testing requires owner administration. |
| Secret-protection configuration | OPEN: enabled status not established; review supported GitHub protection features before broad promotion. |
| Real-project research quality | OPEN: complete live pilot with independently checked evidence and handoff still required. |
| Installed agent host and adversarial tool traces | OPEN: 12 cases prepared, not executed in an installed host. |
| Renderer and image consistency | OPEN: technical source exists; tool execution and visual comparison not verified. |

## Owner-administered repository controls

Protect main with required pull requests and passing validation/security checks, prevent force pushes and deletion, and use an appropriate review policy. CODEOWNERS only requests review; it does not enable enforcement. Enable private vulnerability reporting and test the external reporter path. Review secret scanning/push protection availability and enable supported protections. Review pinned-action update PRs rather than auto-merging them.

The connected tool can read branch/ruleset status but does not expose administration writes for these controls. Its private-reporting endpoint read was rejected as unsupported. The repository does not claim that a configuration file enabled these settings.

## Publication decision

The source and validated GitHub Actions package can be inspected and contributed to as a clearly labeled community-review candidate with visible limitations. See [the candidate release notes](RELEASE-NOTES-0.2.0-rc.1.md). Do not promote a stable/supported-agent release, marketplace compatibility, or “secure to use” guarantee until the corresponding open gates have evidence. No GitHub release, tag, marketplace listing, broad announcement, paid service, or deployment is created by this preparation step.

## Versioning, rollback, and release evidence

Before tagging, inspect the exact diff, rerun all required checks on that revision, resolve release-blocking findings, and retain the package hash. Record host/model/tool versions and permission settings for behavior tests. A follow-up documentation-only commit must not be represented as having run code checks that only ran on its parent.

If a published candidate proves unsafe, withdraw the version publicly, recommend disabling it, publish a corrective release with migration guidance, and preserve sanitized evidence. See [the pre-mortem](PREMORTEM.md) for incident handling.
