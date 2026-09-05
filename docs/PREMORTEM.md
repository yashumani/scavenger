# Public-release pre-mortem

Scenario: the project has been shared publicly, and a contributor reports that Scavenger caused a bad engineering decision or an unsafe tool action. Work backward before launching. Priorities below are qualitative engineering judgments, not measured probabilities.

| Failure scenario | Impact / priority | Prevention and evidence | Residual risk / release decision |
| --- | --- | --- | --- |
| A malicious README instructs an agent to reveal a secret or execute an installer. | Critical | Source-as-data policy; read-only defaults; H03/H08/H12 host cases. | Skill text cannot enforce permissions. Actual host traces and least-privilege configuration are required; not yet verified. |
| A fabricated citation or failed test is presented as proven support. | High | Evidence levels; required execution metadata; explicit `evidence_truth_verified: false`; simulation demonstrates that plausible lies still pass structure. | Review actual sources and test artifacts. The validator is not a truth detector. |
| An apparently open repository contains incompatible model/data/code terms. | High | Separate license gate before scoring; all 243 gate combinations tested; reference-only/gap remains available. | Legal compatibility is a scoped human decision, not a license-name lookup. |
| A private brief is sent to a public search engine or committed with a sample. | Critical | Query-redaction instructions, separate workspaces, explicit packaging allowlist, private-file exclusion test. | Pattern lint cannot find every secret or confidential concept. Human redaction and host controls remain necessary. |
| Malformed records exhaust resources, confuse validation, or inject terminal escapes. | Medium | Bounded bytes/depth/collections/strings; finite numbers; strict fields; control-character and CLI regression tests. | Limits may reject large legitimate research runs; split them deliberately rather than disabling safeguards. |
| A URL points to local infrastructure, uses ambiguous encoding, or leaks credentials. | High for a future fetcher | Offline ledger-URL checks reject local/IP targets, credential URLs, bad ports, and encoded controls. | Helpers never fetch these URLs. A future fetcher needs independent DNS/redirect/SSRF protections. |
| Workspace initialization overwrites files or leaves misleading partial output. | High | Exclusive creation, symlink checks, template preloading, rollback, concurrent-initialization and failure-injection tests. | Trusted-parent assumption remains; no defense against an attacker controlling the filesystem during writes. |
| A release ZIP includes private artifacts or is modified after testing. | High | Explicit file allowlist, per-file hashes, reproducible build, zip-slip and tamper rejection, extracted-package smoke test. | Self-supplied checksums are not signatures. No signed release or attestation is claimed. |
| A contributor or compromised action changes executable instructions without review. | High | SHA-pinned Actions, read-only validation permissions, no persisted checkout credentials, CODEOWNERS, Dependabot. | Main was unprotected and rulesets empty at inspection. Required checks/reviews and force-push protection need owner configuration. |
| Users assume the skill works in every agent host. | High | No universal installation claim; explicit host protocol and 12 cases marked not-run. | A real installed-host run is required before a supported-host release claim. |
| An architecture illustration invents a connection or hides a trust boundary. | Medium | Editable diagrams are authoritative; component/edge/label review and image-unavailable behavior are specified. | Renderer/image-tool execution and consistency review are not yet verified. |
| Vulnerability reports arrive through public issues because private reporting is unavailable. | High | SECURITY.md gives conditional private-reporting instructions and a no-details fallback. | Enable and test GitHub private reporting before broad promotion; no fake contact address or response SLA. |

## Stop conditions

Block a stable/supported release for unauthorized tool actions, exposed real credentials, destructive writes, a gate bypass, a failing required check, or missing license/provenance. Suspend the affected activity; preserve only sanitized evidence; correct the issue and rerun the relevant tests against the exact revision. Do not publish exploit details before coordinated review.

## Failure response and rollback

Do not rewrite public history to hide a defect. Mark the affected candidate/version as withdrawn in the README and release notes, provide a corrected commit, and recommend that users remove/disable the affected skill in their host. Rotate any genuinely exposed credentials through the affected service's authorized flow. Existing research outputs require review; fixing the helper does not retroactively validate old recommendations.

## Sources and evidence boundaries

This review uses the repository's code/tests and the [Agent Skills specification](https://agentskills.io/specification), [GitHub Actions secure-use reference](https://docs.github.com/en/actions/reference/security/secure-use), and [GitHub private reporting guidance](https://docs.github.com/code-security/security-advisories/guidance-on-reporting-and-writing/privately-reporting-a-security-vulnerability), checked 2026-09-05. It is a first-party pre-mortem, not an independent penetration test.
