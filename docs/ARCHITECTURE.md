# Scavenger architecture

Status: initial design, 2026-09-05. Scavenger is a skill executed by an existing agent host, not a new model runtime. The Mermaid blocks below are editable technical source; no generated architecture image is included in v0.1.

## System context

```mermaid
flowchart LR
    U[User and authorized project brief] --> H[Agent host]
    S[Scavenger skill package] --> H
    H --> R[Live search and repository readers]
    R --> E[Untrusted external sources]
    E --> R
    R --> H
    H --> V[Offline record validator]
    V --> H
    H --> O[Authorized project handoff workspace]
    H -. optional .-> I[Diagram renderer or image generator]
    I -. reviewed visual .-> O
```

## Research and decision flow

```mermaid
flowchart TD
    A[Requirement baseline with stable IDs] --> B[Capability decomposition and query plan]
    B --> C[Discovery and source inspection]
    C --> D[Evidence ledger and candidate mappings]
    D --> E{License and risk gates}
    E -->|pass| F[Relevance comparison]
    E -->|fail or unknown| G[Reject or review-required]
    F --> H[Reuse decisions and build-new gaps]
    G --> H
    H --> J[Architecture and technical diagrams]
    J --> K[Validation and development backlog]
    K --> L[Project handoff with limitations]
```

## Contracts and boundaries

The agent controls intake, tool use, claim interpretation, search breadth, and synthesis. The skill supplies instructions, references, templates, and a deterministic record helper. Sources are untrusted input, not executable instructions. The helper reads local JSON; it performs no network requests and invokes no third-party commands.

A run connects requirement IDs to candidate IDs, evidence source IDs, decisions, architecture components, and implementation tasks. The JSON helper currently validates through the requirement/decision layer. Architecture contracts, rendered diagram consistency, evidence truth, and actual license/security review remain agent/reviewer responsibilities.

The project output workspace is separate from the reusable skill. Credentials remain in the host's authorized tool layer. Repository writes and publication are explicit operations, not effects of reading source files. Image generation is optional: technical diagram source stays authoritative and image labels/edges require review.

## Design decisions

Use a portable SKILL.md package rather than a hosted application for the initial deliverable. Use Markdown plus a JSON record for readable and machine-checkable outputs. Use Python's standard library for offline helpers to avoid installing dependencies. Prefer honest gaps over invented evidence. Do not add an LLM provider, database, crawler, or implementation orchestrator before the research workflow is evaluated.

## External format reference

Package layout follows the [Agent Skills specification](https://agentskills.io/specification), reviewed 2026-09-05. The local checker is repository-specific, not a complete implementation of the specification or a substitute for host compatibility testing.
