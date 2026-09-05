# Contributing to Scavenger

Help turn existing work into better engineering decisions—not unsupported claims or indiscriminate code copying.

## A useful first contribution

Reproduce an issue using synthetic inputs; add a failing regression test; improve an unclear requirement or safety instruction; or submit a sanitized real-world research walkthrough with sources, limitations, and acceptance criteria. Host reports must identify the host, model, skill commit, tool permissions, cases run, and actual results. Planned cases are not passing cases.

Open an issue for substantial scope changes before implementing a new crawler, paid service, database, or model integration. Never enable paid resources or publish private data to reproduce a bug. Follow [SECURITY.md](SECURITY.md) for vulnerabilities and [our conduct expectations](CODE_OF_CONDUCT.md).

## Development workflow

Use Python 3.11 or newer; the declared CI matrix covers 3.11–3.13 on Linux and 3.13 on macOS/Windows. Work on a branch and open a pull request. Runtime dependencies must remain standard-library-only unless a separately reviewed requirement justifies a change.

```sh
python scripts/scavenger.py check-skill .
python -m unittest discover -s tests -v
python scripts/simulate.py
python scripts/release_check.py
```

When adding a public repository file, review whether it belongs in the distribution and update `release-files.txt` explicitly. Do not use a glob to scoop up workspaces, `.env` files, downloaded models, caches, or credentials. Keep temporary outputs outside the repository. The release checker must pass against the exact candidate commit.

## Review requirements

Explain the requirement, behavior change, tests actually run, compatibility implications, and remaining risks. Include evidence for new claims. Preserve the distinction between declared, documented, code-inspected, and tested evidence. Keep user requirements separate from proposed enhancements.

Retain copyright, provenance, and applicable notices for any permitted upstream material. Do not contribute unlicensed code or relabel a non-open model/dataset as open source. Contributions to original project files are submitted under the repository's MIT license; only submit material you have the right to contribute. AI-assisted contributions receive the same human review and evidence requirements as other submissions.

Do not weaken tests or gates merely to make CI pass. Changes to instructions, executable scripts, workflows, licensing, or publication behavior deserve focused maintainer review. CODEOWNERS requests reviews; it does not enforce branch protection by itself.
