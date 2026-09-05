# Third-party provenance and notices

Scavenger's own source, templates, synthetic fixtures, and original documentation are MIT-licensed. No third-party candidate implementation, model weights, datasets, or generated architecture images are bundled in this release candidate. Python is supplied by the user's environment; the runtime helpers use its standard library rather than vendored dependencies.

The workflow follows the public [Agent Skills specification](https://agentskills.io/specification). Research guidance links to authoritative documentation rather than copying complete source documents. Investigated candidates retain their licenses; a future code contribution that incorporates upstream material must add provenance and required notices here.

CI references official `actions/checkout`, `actions/setup-python`, and `github/codeql-action` at pinned revisions. Those actions and the hosted services they invoke have their own terms. Their code is not bundled into Scavenger's runtime. Do not infer that the CodeQL action's license is a license for every underlying analysis tool, or that hosted analysis makes this an independently audited product.

The SPDX identifier MIT and license text identify the project's distribution grant. Project names and trademarks are not transferred by that grant.

The finalization artifact uploader uses GitHub's [actions/upload-artifact](https://github.com/actions/upload-artifact) pinned to `043fb46d1a93c77aae656e7c1c64a875d1fc6a0a` (v7 resolved 2026-09-05). It runs in CI, not in the offline helper, and is not vendored into the skill. Its source and license remain with the upstream repository. Downloads follow [GitHub artifact access and retention rules](https://docs.github.com/en/actions/how-tos/manage-workflow-runs/download-workflow-artifacts).
