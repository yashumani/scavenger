#!/usr/bin/env python3
"""Offline Scavenger record helpers. No network calls or third-party execution."""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path
from typing import Any
from guardrails import (Invalid, check_shape, check_record_fields, clean_text,
                        public_url, read_json, write_workspace)

WEIGHTS = {"requirement_fit": 35, "integration": 20, "maintenance": 15,
           "documentation": 10, "deployment": 10, "operating_cost": 10}
GATES = ("license", "security", "privacy", "deployment", "mandatory_fit")
LEVELS = {"discovered", "documented", "code-inspected", "tested"}
REUSE = {"adopt", "adapt", "fork"}
DISPOSITIONS = REUSE | {"reference-only", "build-new", "gap"}
ROOT = Path(__file__).resolve().parents[1]
MAX_BYTES = 2_000_000


def need(condition: bool, message: str) -> None:
    if not condition:
        raise Invalid(message)


def text(value: Any, where: str) -> str:
    return clean_text(value, where)


def obj(value: Any, where: str) -> dict:
    need(isinstance(value, dict), f"{where}: expected an object")
    return value


def seq(value: Any, where: str) -> list:
    need(isinstance(value, list), f"{where}: expected an array")
    return value


def iso_date(value: Any, where: str) -> date:
    text(value, where)
    need(bool(re.fullmatch(r"\d{4}-\d{2}-\d{2}", value)), f"{where}: use YYYY-MM-DD")
    try:
        return date.fromisoformat(value)
    except ValueError as exc:
        raise Invalid(f"{where}: invalid calendar date") from exc


def url(value: Any, where: str, synthetic: bool) -> None:
    public_url(value, where, synthetic)


def indexed(value: Any, where: str) -> dict[str, dict]:
    result: dict[str, dict] = {}
    for number, item in enumerate(seq(value, where)):
        row = obj(item, f"{where}[{number}]")
        key = text(row.get("id"), f"{where}[{number}].id")
        need(key not in result, f"{where}: duplicate id {key}")
        result[key] = row
    return result


def refs(value: Any, allowed: dict, where: str, nonempty: bool = True) -> list:
    items = seq(value, where)
    need(bool(items) or not nonempty, f"{where}: at least one reference is required")
    for item in items:
        text(item, where)
        need(item in allowed, f"{where}: unknown reference {item}")
    need(len(items) == len(set(items)), f"{where}: duplicate references")
    return items


def note(value: Any, sources: dict, where: str) -> None:
    row = obj(value, where)
    text(row.get("reason"), f"{where}.reason")
    refs(row.get("source_ids"), sources, f"{where}.source_ids")


def validate(record: Any) -> dict:
    """Validate declared evidence and traceability; never certify factual truth."""
    check_shape(record)
    r = obj(record, "record")
    check_record_fields(r)
    need(r.get("schema_version") == "0.1", "schema_version: expected 0.1")
    project = obj(r.get("project"), "project")
    text(project.get("name"), "project.name")
    as_of = iso_date(project.get("as_of"), "project.as_of")
    need(project.get("mode") in ("draft", "handoff"), "project.mode: draft or handoff required")
    need(type(project.get("synthetic")) is bool, "project.synthetic: boolean required")
    synthetic = project["synthetic"]
    requirements = indexed(r.get("requirements"), "requirements")
    sources = indexed(r.get("sources"), "sources")
    candidates = indexed(r.get("candidates"), "candidates")
    for rid, row in requirements.items():
        text(row.get("text"), f"{rid}.text")
        text(row.get("acceptance"), f"{rid}.acceptance")
        need(row.get("priority") in ("must", "should", "could"), f"{rid}: invalid priority")
    for sid, row in sources.items():
        url(row.get("url"), f"{sid}.url", synthetic)
        need(iso_date(row.get("accessed_on"), f"{sid}.accessed_on") <= as_of,
             f"{sid}: source access date is after project.as_of")
        text(row.get("revision"), f"{sid}.revision")
        text(row.get("locator"), f"{sid}.locator")
    queries = seq(r.get("query_log"), "query_log")
    for row in queries:
        obj(row, "query_log entry")
        need(iso_date(row.get("date"), "query.date") <= as_of, "query date is after project.as_of")
        for field in ("query", "platform", "outcome"):
            text(row.get(field), f"query.{field}")
    for cid, row in candidates.items():
        text(row.get("name"), f"{cid}.name")
        url(row.get("url"), f"{cid}.url", synthetic)
        mapped = refs(row.get("requirement_ids"), requirements, f"{cid}.requirement_ids")
        evidence = seq(row.get("evidence"), f"{cid}.evidence")
        need(bool(evidence), f"{cid}: evidence is required")
        for ev in evidence:
            obj(ev, f"{cid}.evidence entry")
            refs([ev.get("source_id")], sources, f"{cid}.evidence.source_id")
            refs(ev.get("requirement_ids"), {key: requirements[key] for key in mapped},
                 f"{cid}.evidence.requirement_ids")
            text(ev.get("claim"), f"{cid}.evidence.claim")
            need(isinstance(ev.get("level"), str) and ev.get("level") in LEVELS, f"{cid}: invalid evidence level")
            if ev["level"] == "tested":
                test = obj(ev.get("test"), f"{cid}.evidence.test")
                for field in ("command", "environment", "revision", "result"):
                    text(test.get(field), f"{cid}.test.{field}")
        gates = obj(row.get("gates"), f"{cid}.gates")
        gate_notes = obj(row.get("gate_notes"), f"{cid}.gate_notes")
        need(set(gates) == set(GATES), f"{cid}: unexpected or missing gates")
        need(set(gate_notes) == set(GATES), f"{cid}: unexpected or missing gate notes")
        for key in GATES:
            need(gates[key] in ("pass", "fail", "unknown"), f"{cid}.{key}: invalid gate state")
            note(gate_notes[key], sources, f"{cid}.gate_notes.{key}")
        scores = obj(row.get("scores"), f"{cid}.scores")
        score_notes = obj(row.get("score_notes"), f"{cid}.score_notes")
        need(set(scores) == set(WEIGHTS), f"{cid}: unexpected or missing score dimensions")
        need(set(score_notes) == set(WEIGHTS), f"{cid}: unexpected or missing score notes")
        for key, rating in scores.items():
            need(rating is None or (type(rating) is int and 0 <= rating <= 5),
                 f"{cid}.{key}: score must be an integer 0-5 or null")
            note(score_notes[key], sources, f"{cid}.score_notes.{key}")
    decisions = seq(r.get("decisions"), "decisions")
    decided = set()
    for row in decisions:
        obj(row, "decision")
        rid = text(row.get("requirement_id"), "decision.requirement_id")
        need(rid in requirements, f"decision: unknown requirement {rid}")
        need(rid not in decided, f"decision: duplicate disposition for {rid}")
        decided.add(rid)
        disposition = row.get("disposition")
        need(isinstance(disposition, str) and disposition in DISPOSITIONS, f"{rid}: invalid disposition")
        text(row.get("rationale"), f"{rid}.rationale")
        selected = refs(row.get("candidate_ids"), candidates, f"{rid}.candidate_ids",
                        nonempty=disposition in REUSE | {"reference-only"})
        for cid in selected:
            candidate = candidates[cid]
            need(rid in candidate["requirement_ids"], f"{cid}: not mapped to {rid}")
            if disposition in REUSE:
                need(all(v == "pass" for v in candidate["gates"].values()),
                     f"{cid}: reuse blocked by failed or unknown gate")
                need(all(v is not None for v in candidate["scores"].values()),
                     f"{cid}: reuse decision requires complete scores")
                need(any(ev["level"] in {"code-inspected", "tested"}
                         and rid in ev["requirement_ids"] for ev in candidate["evidence"]),
                     f"{cid}: reuse needs code-inspected or tested evidence for {rid}")
    for field in ("limitations", "proposed_enhancements"):
        for item in seq(r.get(field), field):
            text(item, field)
    if project["mode"] == "handoff":
        need(bool(requirements), "handoff: at least one requirement is required")
        need(bool(queries), "handoff: query_log is required")
        need(decided == set(requirements), "handoff: every requirement needs a disposition")
    return r


def score(record: Any) -> list[dict]:
    r = validate(record)
    result = []
    for candidate in r["candidates"]:
        states = list(candidate["gates"].values())
        status = "blocked" if "fail" in states else "review-required" if "unknown" in states else "eligible"
        ratings = candidate["scores"]
        complete = all(value is not None for value in ratings.values())
        if status == "eligible" and not complete:
            status = "unscored"
        value = round(sum(WEIGHTS[key] * ratings[key] / 5 for key in WEIGHTS), 2) if status == "eligible" else None
        result.append({"id": candidate["id"], "status": status, "score": value,
                       "synthetic": r["project"]["synthetic"], "evidence_truth_verified": False})
    return sorted(result, key=lambda row: (row["score"] is None, -(row["score"] or 0), row["id"]))


def unique_object(pairs: list[tuple]) -> dict:
    result = {}
    for key, value in pairs:
        need(key not in result, f"JSON: duplicate key {key}")
        result[key] = value
    return result


def load(path: Path) -> Any:
    return read_json(path)


def init_run(destination: Path, name: str) -> None:
    text(name, "project name")
    record = load(ROOT / "assets/research-record.json")
    record["project"].update(name=name, as_of=date.today().isoformat())
    record["limitations"] = ["Draft only. No research has been performed."]
    # Read and validate all templates before creating any output directory.
    validate(record)
    contents = {name: (ROOT / "assets" / name).read_text(encoding="utf-8")
                for name in ("project-brief.md", "handoff.md")}
    contents["research-record.json"] = json.dumps(record, indent=2, ensure_ascii=True) + "\n"
    write_workspace(destination, contents)


def check_skill(root: Path) -> None:
    """Repository-specific checks, not a general YAML or Agent Skills parser."""
    content = (root / "SKILL.md").read_text(encoding="utf-8")
    lines = content.splitlines()
    need(lines and lines[0] == "---", "SKILL.md: missing opening frontmatter")
    need("---" in lines[1:], "SKILL.md: missing closing frontmatter")
    end = lines.index("---", 1)
    fields = {}
    for line in lines[1:end]:
        if line and not line.startswith(" "):
            key, separator, value = line.partition(":")
            need(bool(separator), "SKILL.md: malformed frontmatter")
            need(key not in fields, f"SKILL.md: duplicate field {key}")
            fields[key] = value.strip()
    need(fields.get("name") == "scavenger", "SKILL.md: name must be scavenger")
    need(1 <= len(fields.get("description", "")) <= 1024, "SKILL.md: invalid description length")
    need(1 <= len(fields.get("compatibility", "")) <= 500, "SKILL.md: invalid compatibility length")
    need(len(lines) < 500, "SKILL.md: keep instructions under 500 lines")
    need(set(fields) <= {"name", "description", "compatibility", "license", "metadata", "allowed-tools"},
         "SKILL.md: unexpected frontmatter field")
    for target in re.findall(r"\]\(([^)]+)\)", content):
        if "://" not in target and not target.startswith("#"):
            file = (root / target.split("#", 1)[0]).resolve()
            need(file.is_relative_to(root.resolve()) and file.is_file(), f"SKILL.md: invalid local link {target}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    init = commands.add_parser("init", help="Create a draft research workspace; never overwrite")
    init.add_argument("path", type=Path)
    init.add_argument("--name", required=True)
    for command in ("validate", "score", "check-skill"):
        child = commands.add_parser(command)
        child.add_argument("path", type=Path)
    args = parser.parse_args(argv)
    try:
        if args.command == "init":
            init_run(args.path, args.name)
            print("Created draft research workspace (no research performed).")
        elif args.command == "check-skill":
            check_skill(args.path)
            print("Repository skill checks passed (not host installation validation).")
        elif args.command == "validate":
            record = validate(load(args.path))
            print(f"Valid {record['project']['mode']} record; synthetic={record['project']['synthetic']}. Evidence truth not verified.")
        else:
            print(json.dumps(score(load(args.path)), indent=2))
        return 0
    except (Invalid, OSError, ValueError, TypeError, RecursionError) as exc:
        # Escape and bound validation diagnostics; do not echo raw OS paths.
        message = str(exc) if isinstance(exc, Invalid) else type(exc).__name__ + ": operation failed"
        print("ERROR: " + message.encode("unicode_escape").decode("ascii")[:600], file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
