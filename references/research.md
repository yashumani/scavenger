# Research protocol

## Requirement-first discovery

Build a matrix of capability, mandatory constraints, search phrases, and expected evidence. Search both whole-project alternatives and smaller replaceable components. Match the user's language to implementation terms without changing the intent. An orchestration requirement, for example, may need state persistence, routing, retries, tool authorization, and evaluations rather than a project merely described as multi-agent.

For each critical capability, attempt a requirement phrase, a technical-pattern query, and a constraint/alternative query. These are starting points, not rigid minimum counts. Broaden or stop with a stated rationale. Do not discard niche projects solely for low popularity or infrequent releases.

## Inspect the shortlist

Read repository documentation, exact license files, relevant implementation paths, package/dependency manifests, tests, releases, and pertinent issues. Record documented limitations and contrary evidence. Identify whether a feature is implemented, planned, an enterprise add-on, or an external service dependency. Record repository archived status, dated maintenance signals, and version compatibility as observations, not permanent facts.

For AI assets, inspect the relevant model/dataset card, revision, license, intended uses, evaluation conditions, dependencies, and hardware needs. A paper's results do not prove the candidate runs in the target environment.

## Evidence ledger

Each source needs a stable ID, URL, accessed_on date, revision (or an explicit reason no immutable revision exists), and a claim-specific locator. Candidate evidence links to these IDs. Preserve short descriptions rather than copying entire copyrighted documents.

Evidence levels are claim-specific:

| Level | Meaning |
| --- | --- |
| discovered | Found a lead; relevant content has not been verified. |
| documented | Read primary documentation supporting the claim. |
| code-inspected | Read the specific implementation supporting the claim. |
| tested | Executed a permitted, scoped test and retained its result and environment. |

An agent must never promote a candidate's overall evidence level because one unrelated feature was tested. Contradictions remain visible until resolved. Record inaccessible sources, rate limits, failed queries, and other coverage limitations. Do not manufacture citations, file paths, commit SHAs, or measurements.

## Search log and stopping rule

Log query, date, source/platform, result summary, and requirement IDs. Group forks by upstream. Seek an independent alternative for high-risk decisions. End with a coverage statement: investigated capabilities, evidence depth, unresolved gaps, and why research stopped. A search budget can cap work, but unmet requirements must remain gaps rather than being declared satisfied.

Refresh volatile facts before a new recommendation. Reuse previous research only with its original timestamp and an explicit refresh status. Do not call cached metadata current without rechecking it.
