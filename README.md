# Scavenger

**Requirements in. Evidence-backed, open-source-first architecture out.**

Scavenger is a reusable agent skill for finding relevant existing work, verifying what can be reused, and turning those findings into a documented project blueprint. It searches at both whole-project and component level. It is not an autonomous crawler, a repository copier, or a deployed application.

## Start here

[Skill instructions](SKILL.md) · [Requirements](docs/REQUIREMENTS.md) · [Architecture](docs/ARCHITECTURE.md) · [Roadmap](docs/ROADMAP.md) · [Development status](docs/STATUS.md)

Ask an agent that has loaded this skill:

> Use Scavenger on the following project requirements. Research existing open-source implementations, inspect the strongest candidates, map reusable components to each requirement, and produce an architecture and development handoff. Preserve my requirements, make proposed enhancements explicit, and do not execute third-party code or modify the target project.

Then provide the actual project brief or authorized repository. The skill guides intake, live research, evidence review, licensing and risk gates, relevance scoring, reuse decisions, documentation, editable diagrams, and implementation planning.

## Use the skill

The repository root is the skill directory: `SKILL.md`, `references/`, `assets/`, and `scripts/` belong together. Load or copy the complete directory as `scavenger` using your agent host's supported skill mechanism. No universal installation command or cross-host compatibility is claimed. Installation behavior must be verified in the chosen host.

Live research requires host-provided web search and repository/document reading. Architecture illustrations require an available image-generation tool; the skill also supports editable technical diagram source. The repository does not supply these services or access credentials. The Python helpers use only the standard library and do not call an LLM or access the network.

## Offline helpers

With Python 3.11 or later, from the repository root:

```sh
python scripts/scavenger.py check-skill .
python -m unittest discover -s tests -v
python scripts/scavenger.py init ../my-project-research --name "My project"
python scripts/scavenger.py validate ../my-project-research/research-record.json
python scripts/scavenger.py score examples/demo-record.json
```

`init` creates a draft record, brief, and handoff template. It refuses to overwrite an existing directory. Update the draft with actual research before changing its mode to `handoff`. Run `validate` and `score` against your completed record.

Validation checks declared structure, source references, gate states, and requirement dispositions. It does **not** verify that claims are true, that code works, that a license is compatible, or that a dependency is secure. The included demo is explicitly synthetic, not a completed research study. See [the record contract and rubric](references/evaluation.md).

## Outputs and safety

A research run produces a requirements baseline, query log and source ledger, candidate comparison, requirement-to-component mapping, reuse/attribution decisions, architecture and diagram source, risks, and a testable development backlog. Generated illustrations are optional and must be reviewed against the technical diagram.

Research results stay in the authorized project workspace, not in this reusable skill repository by default. Unresolved licensing or security gates block reuse recommendations. Third-party execution, code copying, publication, paid services, and deployment require separate authorization. See [the security boundaries](references/security.md).

## Status and licensing

Version 0.1.0 is an initial skill package plus offline validation helpers. Live end-to-end research quality, agent-host installation, and image-generation workflows still need pilot evaluation. Automated checks are defined in `.github/workflows/validate.yml`; observed results belong in [development status](docs/STATUS.md).

**Scavenger's own distribution license has not yet been selected by the owner.** No open-source license grant is implied by repository visibility. The open-source-first description refers to the research workflow. See [the pending license decision](docs/LICENSE-DECISION.md). Third-party candidates retain their own licenses.
