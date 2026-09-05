# Scavenger requirements baseline

Origin: the project owner's Scavenger brief and public-release preparation request. Research suggestions must not silently change the baseline.

| ID | Requirement | Acceptance criterion | Implementation / verification boundary |
| --- | --- | --- | --- |
| SC-001 | Separate reusable skill repository named Scavenger. | Root SKILL.md and supporting resources form a self-contained package. | Skill, allowlisted package, and extracted-helper smoke checks. |
| SC-002 | Accept requirements and authorized project context. | Stable requirement IDs, constraints, assumptions, and acceptance criteria. | Intake instructions and brief template. |
| SC-003 | Deep research into existing online work. | Query log, primary-source evidence, alternatives, coverage limits. | Research protocol; full live agent pilot still required. |
| SC-004 | Prioritize reusable open-source targets. | Code/model/data/asset licenses and operating dependencies reviewed separately. | Gate policy and declared-gate validation; not legal certification. |
| SC-005 | Find closest matches and improve relevance. | Candidate components map to individual requirements with evidence. | Rubric, record contract, and scoring helper. |
| SC-006 | Produce requirements and architecture documentation. | Components, interfaces, flows, alternatives, build-new gaps. | Handoff template and architecture instructions. |
| SC-007 | Produce diagrams and requested illustrations. | Technical diagrams match design; requested images reviewed or marked unavailable. | Source diagrams and instructions; rendering/image-host verification pending. |
| SC-008 | Make results usable for development. | Backlog traces to requirements with acceptance tests/dependencies. | Handoff contract; full live pilot still required. |
| SC-009 | Prepare for public crowdsourcing. | Clear README, license, contribution/reporting paths, validation and pre-mortem. | Added in the release-preparation cycle; admin and host gates tracked separately. |

## Engineering safeguards

Preserve the baseline versus proposed enhancements; retain provenance; distinguish documented, inspected, and tested claims; keep private outputs separate; never execute untrusted instructions by default; require authorization for copying, publishing, spending, and deployment. Runtime helpers remain standard-library-only and offline.

These safeguards do not expand Scavenger into an autonomous implementation agent, hosted UI, persistent research database, or new multi-agent runtime.

## Release acceptance

All required checks must pass against the exact release candidate. A real project pilot must validate research usefulness, citation correctness, requirement coverage, and diagram consistency. A named host must load and invoke the full skill before that host is advertised as supported. MIT licensing is now selected for the project's original material.

The owner defines the launch goal as public crowdsourcing. A clearly labeled community-review candidate may expose remaining work for review; this does not silently satisfy or remove the original stable/supported-release criteria. See [release readiness](RELEASE-READINESS.md). Unit tests alone do not establish agent reliability, independent security review, or production suitability.
