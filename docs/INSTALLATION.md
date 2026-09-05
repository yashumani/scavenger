# Installation and a first safe run

The release candidate is a repository package, not a deployed application or a promise of universal agent-host compatibility. No stable GitHub release or marketplace listing is implied.

## Inspect and exercise the helpers

Clone this repository into a directory named `scavenger`, or inspect an explicitly versioned ZIP built by `scripts/build_release.py`. Read SKILL.md, scripts, references, and SECURITY.md before allowing execution. The helpers need Python 3.11+ and no additional Python packages. On systems where `python` is unavailable, use the appropriate Python 3 interpreter command, such as `py -3` on Windows.

Run `python scripts/scavenger.py check-skill .`, then validate and score `examples/demo-record.json`. That fixture is synthetic. Run the test suite and `python scripts/release_check.py` from the repository root for the developer checks. These tests do not run an LLM.

Create a workspace using `python scripts/scavenger.py init ../my-project-research --name "My project"`. The path must not already exist. Choose a trusted, user-owned parent directory; symlink-bearing paths are rejected. On systems where temporary or home directories are aliases, use their canonical filesystem path. The draft is valid as a draft, not a completed handoff.

## Load the skill in a host

Keep SKILL.md, references, assets, and scripts together under the `scavenger/` directory. Use the chosen host's documented skill-loading mechanism. A chat containing the instruction text is not proof that the host installed the package or exposed its assets and tools.

Verify that the host can read all local references, browse primary sources, and access only the authorized project context. Begin with public or synthetic data, read-only repository permissions, and no production secrets. The skill does not supply credentials, a model, search, rendering, or image generation. Those capabilities and any service costs belong to the host.

Complete [the host evaluation protocol](../references/host-evaluation.md) before advertising support for that host. No installed host has yet been certified by this repository's release-preparation tests.

## Packaging and integrity

`python scripts/build_release.py ../scavenger-0.2.0-rc.1.zip` refuses to overwrite an existing file. `python scripts/build_release.py ../scavenger-0.2.0-rc.1.zip --verify` verifies archive paths and per-file hashes without executing archive contents. The allowlist is `release-files.txt`.

A checksum proves consistency only when the expected checksum came from a trusted source. It is not a publisher signature. Do not execute a ZIP merely because it contains a self-consistent manifest. The repository's package smoke test executes only the package it just built from the local reviewed source.
