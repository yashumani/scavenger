# Scavenger

### Find what exists. Verify what fits. Design what is missing.

**A reusable agent skill for turning project requirements into an evidence-backed, open-source-first architecture and development plan.**

[![Validation](https://github.com/yashumani/scavenger/actions/workflows/validate.yml/badge.svg)](https://github.com/yashumani/scavenger/actions/workflows/validate.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

**Release candidate: `0.2.0-rc.1`.** Built for community review, not advertised as an independently audited or universally compatible agent. See [verification evidence](docs/VALIDATION.md) and [remaining launch gates](docs/RELEASE-READINESS.md).

[Start using it](docs/INSTALLATION.md) · [Read the skill](SKILL.md) · [Contribute](CONTRIBUTING.md) · [Security](SECURITY.md)

## Why Scavenger?

Finding repositories is easy. Deciding which parts actually satisfy your requirements—and what it takes to combine them—is harder.

Scavenger guides an agent to research entire solutions **and individual components**, inspect primary evidence, separate usable code from promising claims, and explain what to adopt, adapt, reference, reject, or build yourself. The result is a development handoff, not a pile of links.

| Ordinary repository search | A Scavenger research handoff |
| --- | --- |
| Similar project names and popularity | Requirement-by-requirement relevance and evidence |
| README claims | Explicitly labeled documented, code-inspected, or tested claims |
| “Open source” assumed from visibility | Separate license, security, privacy, deployment, and mandatory-fit gates |
| A ranked list | Reuse decisions, integration work, original development, and alternatives |
| A diagram without provenance | Architecture traced to requirements, sources, and acceptance tests |

## What you get

A run should produce a requirements baseline, dated search log and source ledger, candidate comparison, requirement-to-component mapping, reuse and attribution plan, architecture documentation, editable technical diagrams, risks, and a sequenced implementation backlog. Requested architecture illustrations depend on the host's image tools and must be reviewed against the technical design.

Scavenger preserves your original requirements. Research-driven enhancements are proposals, not silent scope changes.

## Try the offline demonstration

Inspect the repository before executing its scripts. The helpers use **Python's standard library only**: no package installation, model key, telemetry, network calls, or candidate-code execution.

```sh
git clone https://github.com/yashumani/scavenger.git
cd scavenger
python scripts/scavenger.py check-skill .
python scripts/scavenger.py validate examples/demo-record.json
python scripts/scavenger.py score examples/demo-record.json
```

The example is **fictional test data**, not completed project research. It demonstrates a useful rule:

| Candidate | Declared situation | Result |
| --- | --- | --- |
| C-001 | All fixture gates pass; mixed relevance ratings | 84 / 100 |
| C-002 | Maximum relevance ratings, but license is unknown | Review required; score withheld |

A high score cannot override an unresolved gate. Every result includes `evidence_truth_verified: false`: structural validation does not prove that a citation is true or that a test ran.

Create an independent workspace for your own project:

```sh
python scripts/scavenger.py init ../my-project-research --name "My project"
```

This creates a draft brief, evidence record, and handoff template. It refuses existing destinations. Use a trusted directory, keep private outputs outside this public repository, and review the [input limits and safety boundaries](references/security.md).

## Use it with an agent

Load the **complete `scavenger/` directory** with your agent host's supported skill mechanism, then provide a brief or authorized repository:

> Use Scavenger to investigate these project requirements. Find and inspect relevant open-source work, map reusable components to each requirement, and produce an architecture and development handoff. Preserve my constraints, cite the evidence, show gaps, and do not execute third-party code or modify the target project.

Live research needs host-provided web search and repository/document reading. The skill itself does not supply a browser, model runtime, accounts, or credentials. Host services can have their own costs. No particular host installation is yet certified; [the installation guide](docs/INSTALLATION.md) and [12 host-evaluation cases](evals/host-cases.json) make that verification explicit.

## Safety by design, not a security guarantee

The default workflow is **read-only research through handoff**. Source text is untrusted evidence, not permission to execute commands, expose credentials, publish private work, buy services, or deploy. Host-enforced permissions remain essential.

The offline helpers enforce bounded inputs, strict record fields, canonical ledger URLs, gate-aware scoring, and overwrite protection. A correctly formatted record can still contain fabricated claims. Review the sources, license terms, and test evidence before using a recommendation. This project has not undergone an independent security audit.

## Test and inspect a release package

```sh
python -m unittest discover -s tests -v
python scripts/simulate.py
python scripts/release_check.py
python scripts/build_release.py ../scavenger-0.2.0-rc.1.zip
python scripts/build_release.py ../scavenger-0.2.0-rc.1.zip --verify
```

The release checker audits declared repository policies, builds the package twice, checks byte-for-byte reproducibility, and runs five helper commands from a clean extracted package. The ZIP is built from an explicit allowlist and carries a per-file SHA-256 manifest. **Checksums detect changes; they are not signatures or a substitute for trusting the source.**

Offline tests, deterministic simulations, a package smoke test, and an installed-agent evaluation are different kinds of evidence. [Validation](docs/VALIDATION.md) records which actually ran; the [pre-mortem](docs/PREMORTEM.md) records remaining risks.

## Help make it better

Useful contributions include sanitized real-project walkthroughs, host compatibility reports with actual tool traces, relevance-rubric improvements, new adversarial tests, clearer documentation, and reviewed fixes. Start with [CONTRIBUTING.md](CONTRIBUTING.md). No production data or credentials belong in issues, pull requests, or fixtures. Report vulnerabilities through [SECURITY.md](SECURITY.md), not public exploit details.

## Project map

`SKILL.md` is the agent workflow. `references/` defines research, evaluation, safety, and host testing. `assets/` contains project templates. `scripts/` supplies offline helpers and release checks. `tests/` and `evals/` separate automated checks from host-evaluation plans. `docs/` retains requirements, architecture, roadmap, pre-mortem, and release evidence.

## License

Scavenger's original code and documentation are licensed under [MIT](LICENSE). Third-party code, models, datasets, and assets investigated by Scavenger retain their own licenses; this project does not relicense them. See [third-party notices](docs/THIRD-PARTY-NOTICES.md).
