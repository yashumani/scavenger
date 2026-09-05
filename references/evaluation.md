# Relevance, gates, and record contract

## Gates precede scores

For each candidate record gate states `pass`, `fail`, or `unknown` for `license`, `security`, `privacy`, `deployment`, and `mandatory_fit`. `pass` means the scoped review has sufficient evidence, not that risk is zero. Each gate requires a written reason and evidence references. Unknown gates are unresolved, not implicit passes.

Only candidates with every gate recorded as pass are eligible for scored reuse recommendations. A failed gate blocks selection. An unknown gate needs review. A license identifier alone is not a compatibility decision: inspect the exact license, affected artifact, obligations, planned modification/distribution, and dependencies. No license is not permission to reuse. Keep legally ambiguous cases review-required and consult qualified counsel when needed.

## Rubric

Rate each dimension 0-5 with a written rationale. Unknown scores are null and are NOT silently imputed or renormalized. Use equal evidence standards across candidates. The helper's weights are fixed defaults, not an objective measurement:

| Dimension | Weight | A high score means |
| --- | ---: | --- |
| requirement_fit | 35 | Strong evidence for the particular mapped capabilities. |
| integration | 20 | Compatible interfaces and limited adaptation work. |
| maintenance | 15 | Evidence of sustainable maintenance for the intended use. |
| documentation | 10 | Clear implementation and operational documentation/tests. |
| deployment | 10 | Fits the required platform and deployment constraints. |
| operating_cost | 10 | Low supported operating burden within the user's budget. |

Score = sum(weight * rating / 5), on a 0-100 scale. Scores are a decision aid, not a confidence percentage. Preserve unknowns and explain close tradeoffs; do not let a numeric ranking substitute for architecture judgment. Estimate cost and implementation effort separately with assumptions and ranges.

## JSON research record v0.1

`schema_version` is `0.1`. `project` contains `name`, `as_of` (YYYY-MM-DD), `mode` (`draft` or `handoff`), and `synthetic` (boolean). Synthetic fixtures are for testing only; never present them as real research.

`requirements` contains unique `id`, `text`, `priority` (`must`, `should`, `could`), and `acceptance` fields. `sources` contains unique `id`, credential-free canonical HTTPS `url` without query parameters, `accessed_on`, `revision`, and `locator`. `query_log` contains dated `query`, `platform`, and `outcome` records; keep search terms redacted.

`candidates` contains unique `id`, `name`, `url`, `requirement_ids`, `evidence`, `gates`, `gate_notes`, `scores`, and `score_notes`. Evidence entries contain `source_id`, `requirement_ids`, `claim`, and `level`; tested evidence also contains a `test` object with `command`, `environment`, `revision`, and `result`. Gate and score notes each contain a `reason` and nonempty `source_ids` that resolve to the ledger. Unknown gates/scores may cite evidence of the limitation.

`decisions` contains one entry per requirement in handoff mode: `requirement_id`, `disposition` (`adopt`, `adapt`, `fork`, `reference-only`, `build-new`, `gap`), `candidate_ids`, and `rationale`. Reuse decisions require at least one candidate mapped to that requirement, all gates passed, complete scores, and code-inspected or tested evidence mapped to the particular requirement. A gap requires an explicit reason. Reference-only is not authorization to copy code. `limitations` and `proposed_enhancements` are arrays of nonempty strings.

The helper checks record structure, references, dates, gates, and basic handoff completeness. It does not fetch sources, judge the truth of claims, approve a license, scan vulnerabilities, prove tests ran, or verify rendered diagrams. Draft records may intentionally be incomplete; handoff mode requires decisions and a query log. Requirement disposition is NOT proof that implementation acceptance criteria have passed.

## Hardening in 0.2.0-rc.1

The schema version remains 0.1; previously documented fields remain supported. Unexpected fields, nonfinite numbers, duplicate keys, unsafe controls, oversized strings/collections, and excessive nesting are now rejected rather than ignored. URLs require canonical ASCII DNS names, HTTPS, and no credentials or query parameters; local hosts, IP literals, ambiguous encodings, and nonstandard ports are rejected. Reserved example domains are permitted only in synthetic records. This intentionally tightens validation of formerly accepted invalid inputs.

Every scoring row includes `evidence_truth_verified: false`. Even a fabricated but well-formed record can pass structural validation. A `tested` entry records an execution claim, not independently verified execution or a guarantee of a passing result. Evidence reviewers must inspect the result and reject failed tests as support for a capability claim. Unknown or failed gates must never be overridden by ranking.

## Authoritative references

Checked 2026-09-05. Recheck applicable sources during an actual run.

- [GitHub repository licensing](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/licensing-a-repository).
- [Hugging Face repository licenses](https://huggingface.co/docs/hub/repositories-licenses).
- [Agent Skills specification](https://agentskills.io/specification).
