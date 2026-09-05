# Scavenger requirements baseline

Origin: the project owner's Scavenger brief in the project conversation. Status: initial baseline, 2026-09-05. Research suggestions must not silently change it.

| ID | Requirement | Acceptance criterion | v0.1 implementation |
| --- | --- | --- | --- |
| SC-001 | Separate reusable skill repository named Scavenger. | Root SKILL.md and supporting resources form a self-contained package. | Skill and repository checks. |
| SC-002 | Accept project requirements and authorized existing project context. | Stable requirement IDs, constraints, assumptions, and acceptance criteria are recorded. | Intake instructions and brief template. |
| SC-003 | Deep research into existing online work. | Query log, primary-source evidence, alternatives, and coverage limits are retained. | Research protocol; live pilot pending. |
| SC-004 | Prioritize reusable open-source targets. | Applicable code/model/data/asset licenses and operating dependencies are reviewed separately. | Gate policy and declared-gate validation. |
| SC-005 | Find closest matches and improve relevance. | Evidence-backed mappings connect candidate components to individual requirements. | Rubric, evidence contract, and scoring helper. |
| SC-006 | Produce requirements and project architecture documentation. | Handoff includes components, interfaces, data flows, alternatives, and build-new gaps. | Handoff template and architecture instructions. |
| SC-007 | Produce architecture diagrams and generated illustrations. | Editable diagrams agree with documentation; requested images are generated and reviewed or explicitly marked unavailable. | Workflow instructions; image/host pilot pending. |
| SC-008 | Make results usable for development. | Backlog items trace to requirements and have acceptance tests/dependencies. | Handoff contract; live pilot pending. |

## Engineering safeguards added to support the brief

Preserve baseline versus proposed enhancements; retain source provenance; distinguish documented, code-inspected, and tested claims; keep private project outputs separate; never execute untrusted instructions by default; require explicit authorization for copying, publishing, spending, and deployment.

These safeguards do not expand Scavenger into an autonomous implementation agent. An implementation phase, UI, hosted service, persistent research database, or multi-agent runtime is not part of this initial version.

## Release acceptance

All offline contract tests must pass. A real project pilot must validate research usefulness, citation correctness, requirement coverage, and diagram consistency. The chosen agent host must load and invoke the skill successfully. The owner must choose the repository's distribution license before it is advertised as an open-source release. Passing unit tests alone does not satisfy these release criteria.
