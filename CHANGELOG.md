# Changelog

## 0.2.0-rc.1 — release preparation, not a tagged stable release

Add MIT licensing, public onboarding, contribution and security policies, issue/PR templates, a pre-mortem, and explicit launch gates. Harden offline parsing against nonfinite JSON, unknown fields, unsafe controls, excessive resource use, ambiguous/private URLs, and unsafe file types. Preserve the schema 0.1 documented fields while deliberately rejecting formerly accepted malformed inputs.

Use exclusive workspace creation, preload templates, roll back files created by failed writes, and make score output explicitly state that evidence truth is unverified. Add adversarial and integration regressions, deterministic record simulations, an allowlisted reproducible ZIP with per-file hashes, package verification, and an extracted-package smoke test. Expand CI to Linux/macOS/Windows and add commit-pinned CodeQL analysis and Dependabot configuration.

Host installation, real-model adversarial evaluation, image generation, independent security review, and owner-administered repository protections remain separately tracked. No benchmark or compatibility result is inferred from unit tests.

## 0.1.0 — 2026-09-05

Initial skill workflow, requirements and architecture, research templates, gate-aware scoring, and 30 contract tests. Implementation commit: `543065223ef0297405c892dc2ef528d4a00b4525`. The initial package had no selected distribution license; this release-preparation cycle adds MIT licensing.
