# Development roadmap

Statuses distinguish implemented instructions/helpers from behavior validated in a real agent run.

| Step | Deliverable | Acceptance evidence | Status |
| --- | --- | --- | --- |
| 1 | Establish requirements and boundaries. | Baseline preserves the owner's requested scope. | Implemented. |
| 2 | Package the reusable skill. | SKILL.md and all local reference links validate. | Implemented. |
| 3 | Define intake and handoff templates. | Draft workspace initializes without overwriting files. | Implemented and unit-tested. |
| 4 | Define source/evidence record. | Broken references and unsupported evidence levels are rejected. | Implemented and unit-tested. |
| 5 | Add gate-aware scoring. | Unknown/failed gates cannot produce eligible scores or reuse decisions. | Implemented and unit-tested. |
| 6 | Add CI. | Python 3.11, 3.12, and 3.13 jobs run against the repository commit. | Workflow defined; see STATUS.md for observed result. |
| 7 | Run one real project pilot. | Dated live sources, inspected code, alternatives, and a reviewed project handoff. | Next implementation cycle. |
| 8 | Exercise architecture visual workflow. | Editable source, rendered diagrams, requested generated illustration, and consistency review. | Pending pilot. |
| 9 | Add agent-level evaluations. | Positive/negative activation, prompt injection, sparse results, conflicting licenses, unavailable tools, and refresh scenarios are reviewed. | Planned; not covered by unit tests. |
| 10 | Verify installation on a chosen agent host. | Host loads the complete package and invokes the intended workflow. | Pending host selection. |
| 11 | Finalize distribution license. | Owner approves a license; repository license and metadata agree. | Owner decision pending. |
| 12 | Publish versioned release. | Pilot and host checks pass; license, documentation, and release notes are complete. | Blocked on release criteria. |

Future possibilities, not committed scope: automated metadata adapters, a JSON Schema, diagram validation, richer cost models, and cross-project research refresh. Build these only when pilot evidence justifies them.
