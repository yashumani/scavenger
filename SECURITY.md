# Security policy

Scavenger is a research skill plus offline Python helpers. It is not a sandbox, a secret-management system, a license-approval service, or a certification that recommended code is safe. No independent security audit is claimed.

## Report a vulnerability privately

Use GitHub's **Report a vulnerability** option in [Security advisories](https://github.com/yashumani/scavenger/security/advisories) when private reporting is enabled. Its availability is a repository setting, not a consequence of this file existing.

If private reporting is unavailable, open a public issue **only asking the maintainer for a private reporting channel**. Do not include exploit details, tokens, sensitive inputs, or vulnerable customer repositories in that issue. No private contact address or response-time guarantee is invented here. Enabling and testing private reporting is a tracked launch gate.

For a private report, include the affected commit, environment, minimal synthetic reproduction, observed impact, and suggested mitigation. Stop testing after demonstrating the problem. Do not access others' data, probe connected services, or use real secrets as test payloads.

## Supported scope

During the release-candidate phase, fixes target the latest candidate/main branch. Older snapshots are not promised backports. There is no stable supported-host compatibility claim yet. The [release-readiness checklist](docs/RELEASE-READINESS.md) records unresolved checks.

## Threat boundaries

The runtime helpers read local JSON and create explicitly requested workspaces. They do not make network requests, call an LLM, execute candidate commands, or collect telemetry. Developer release checks run this repository's own helper code in a temporary directory; CI uses separately pinned GitHub Actions. Review all code before executing it.

Research itself uses the host's connected tools and may send queries or documents to external services. Keep secrets and private project data out of public queries. Use read-only access, approval prompts, a trusted workspace, and a least-privilege sandbox. Never load unreviewed skills into a host with unrestricted production credentials.

Input validation is not evidence verification. License/security gate values are declarations requiring review. Canonical URL validation applies to stored metadata only; a future fetcher needs its own DNS, redirect, size, and network-address protections. Filesystem protections assume a trusted parent directory, not an attacker controlling the operating system.

## Verification and limitations

See [validation](docs/VALIDATION.md), [safety details](references/security.md), and [the pre-mortem](docs/PREMORTEM.md). A clean test or scan is scoped evidence, not a guarantee of absence of vulnerabilities. Prompt-injection resistance must be tested in the actual host; instruction text alone cannot enforce it.

Maintainers should require reviewed pull requests and passing checks, protect main against force pushes/deletion, enable private vulnerability reporting and supported secret-protection features, and review pinned-action updates. These settings must be enabled and verified separately.
