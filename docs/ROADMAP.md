# Development roadmap

Statuses separate implemented helpers/instructions from behavior observed in an actual agent host.

| Step | Deliverable | Current status |
| --- | --- | --- |
| 1 | Preserve project requirements and authorization boundaries. | Implemented; extended with the public-crowdsourcing goal. |
| 2 | Package a reusable Scavenger skill. | Implemented; complete directory and versioned metadata. |
| 3 | Intake and handoff templates. | Implemented; no-overwrite and failed-write tests. |
| 4 | Source/evidence record contract. | Implemented; strict inputs, provenance references, and resource limits. |
| 5 | Gate-aware relevance scoring. | Implemented; complete gate-state simulation and malformed-score mutations. |
| 6 | Continuous validation. | Expanded to five Python/OS jobs plus separate CodeQL; observed results in STATUS.md. |
| 7 | Full real-project research pilot. | Still required; offline simulations are not a substitute. |
| 8 | Architecture visual workflow. | Editable source provided; renderer and generated-image review not yet exercised. |
| 9 | Agent-level evaluation. | Twelve cases and review protocol prepared; installed-host execution pending. |
| 10 | Named-host installation verification. | Pending; extracted-helper smoke is a different test. |
| 11 | Distribution license and community documentation. | MIT selected; README, security policy, contributor guidance, and templates implemented. |
| 12 | Release gate review and versioned publication. | Reproducible packaging and pre-mortem implemented; owner settings and live/host gates remain open. |

Future scope remains uncommitted: network adapters, JSON Schema integration, richer cost models, diagram automation, and cross-project refresh. Add them only when research or pilot evidence justifies the complexity.
