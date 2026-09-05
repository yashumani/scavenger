"""Bounded, offline input checks. These are not a sandbox or a truth verifier."""
from __future__ import annotations

import json
import math
import os
import re
import stat
from pathlib import Path
from typing import Any
from urllib.parse import unquote, urlsplit

MAX_BYTES = 2_000_000
MAX_TEXT = 16_384
MAX_DEPTH = 32
MAX_NODES = 100_000
MAX_ITEMS = 10_000


class Invalid(ValueError):
    """Rejected input; messages must not include secret-bearing values."""


def need(condition: bool, message: str) -> None:
    if not condition:
        raise Invalid(message)


def clean_text(value: Any, where: str, nonempty: bool = True) -> str:
    need(isinstance(value, str), f"{where}: expected nonempty text")
    need(bool(value.strip()) or not nonempty, f"{where}: expected nonempty text")
    need(len(value) <= MAX_TEXT, f"{where}: text exceeds {MAX_TEXT} characters")
    # Permit ordinary Unicode and multiline prose, but not terminal/bidi controls.
    need(not any((ord(c) < 32 and c not in '\n\t') or 127 <= ord(c) <= 159
                 or 0xD800 <= ord(c) <= 0xDFFF or c in '\u202a\u202b\u202c\u202d\u202e\u2066\u2067\u2068\u2069'
                 for c in value), f"{where}: control or surrogate characters are forbidden")
    return value


def check_shape(value: Any) -> None:
    """Iterative traversal also bounds cyclic objects supplied to the Python API."""
    stack = [(value, 0)]
    count = 0
    while stack:
        item, depth = stack.pop()
        count += 1
        need(count <= MAX_NODES, "JSON: too many values")
        need(depth <= MAX_DEPTH, "JSON: nesting exceeds 32 levels")
        if isinstance(item, dict):
            need(len(item) <= MAX_ITEMS, "JSON: object too large")
            for key, child in item.items():
                clean_text(key, "JSON key")
                stack.append((child, depth + 1))
        elif isinstance(item, list):
            need(len(item) <= MAX_ITEMS, "JSON: array too large")
            stack.extend((child, depth + 1) for child in item)
        elif isinstance(item, str):
            clean_text(item, "JSON string", nonempty=False)
        elif isinstance(item, float):
            need(math.isfinite(item), "JSON: nonfinite number; scores must be an integer 0-5 or null")
        else:
            need(item is None or type(item) in (bool, int), "JSON: unsupported value type")


def known_fields(value: Any, allowed: str, where: str) -> None:
    """Reject silently ignored fields; required-field diagnostics remain in the validator."""
    if isinstance(value, dict):
        need(set(value) <= set(allowed.split()), f"{where}: unexpected field")


def check_record_fields(r: dict) -> None:
    known_fields(r, 'schema_version project requirements sources query_log candidates decisions limitations proposed_enhancements', 'record')
    known_fields(r.get('project'), 'name as_of mode synthetic', 'project')
    specs = {
        'requirements': 'id text priority acceptance',
        'sources': 'id url accessed_on revision locator',
        'query_log': 'date query platform outcome',
        'candidates': 'id name url requirement_ids evidence gates gate_notes scores score_notes',
        'decisions': 'requirement_id disposition candidate_ids rationale',
    }
    for field, allowed in specs.items():
        rows = r.get(field)
        if not isinstance(rows, list):
            continue
        for row in rows:
            known_fields(row, allowed, field)
            if field != 'candidates' or not isinstance(row, dict):
                continue
            for field_name in ('gate_notes', 'score_notes'):
                notes = row.get(field_name)
                if isinstance(notes, dict):
                    for note in notes.values():
                        known_fields(note, 'reason source_ids', field_name)
            evidence = row.get('evidence')
            if isinstance(evidence, list):
                for ev in evidence:
                    known_fields(ev, 'source_id requirement_ids claim level test', 'evidence')
                    if isinstance(ev, dict):
                        known_fields(ev.get('test'), 'command environment revision result', 'test')


def public_url(value: Any, where: str, synthetic: bool) -> None:
    """Check ledger URLs only. No DNS or HTTP; not an SSRF defense for a fetcher."""
    clean_text(value, where)
    need(len(value) <= 4096, f"{where}: URL too long")
    try:
        parsed = urlsplit(value)
        host = parsed.hostname or ''
        need(parsed.scheme == 'https' and bool(host), f"{where}: use an HTTPS URL")
        need(parsed.username is None and parsed.password is None, f"{where}: credentials are forbidden")
        need(not parsed.query, f"{where}: use a canonical URL without query parameters")
        need(parsed.port in (None, 443), f"{where}: nonstandard port is forbidden")
        need(not any(c.isspace() for c in value), f"{where}: whitespace in URL")
        need('\\' not in value and '%' not in parsed.netloc, f"{where}: ambiguous URL encoding")
        need(not re.search(r'%(?![0-9a-fA-F]{2})', value), f"{where}: invalid percent encoding")
        decoded = unquote(value, errors='strict')
        clean_text(decoded, where)
        need(not any(ord(c) < 32 or ord(c) == 127 for c in decoded) and '\\' not in decoded,
             f"{where}: encoded control or backslash is forbidden")
        need(len(host) <= 253 and not host.endswith('.'), f"{where}: invalid hostname")
        labels = host.split('.')
        need(len(labels) >= 2 and all(re.fullmatch(r'[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?', label)
             for label in labels) and bool(re.fullmatch(r'[a-z]{2,63}', labels[-1])),
             f"{where}: require a DNS hostname, not a local host or IP literal")
        need(not any(host == suffix or host.endswith('.' + suffix)
             for suffix in ('local', 'internal', 'lan', 'home', 'localhost')),
             f"{where}: local host is forbidden")
        placeholders = ('example', 'invalid', 'test', 'example.com', 'example.org', 'example.net')
        if not synthetic:
            need(not any(host == suffix or host.endswith('.' + suffix) for suffix in placeholders),
                 f"{where}: placeholder host requires synthetic=true")
    except Invalid:
        raise
    except (ValueError, UnicodeError) as exc:
        raise Invalid(f"{where}: invalid URL") from exc


def no_duplicate_keys(pairs: list[tuple]) -> dict:
    result = {}
    for key, value in pairs:
        need(key not in result, "JSON: duplicate key")
        result[key] = value
    return result


def reject_constant(_: str) -> None:
    raise Invalid("JSON: NaN and Infinity are forbidden")


def read_json(path: Path) -> Any:
    """Read at most MAX_BYTES+1, reject symlinks/devices/FIFOs, and bind checks to the opened file."""
    before = path.lstat()
    need(stat.S_ISREG(before.st_mode), "JSON: expected a regular non-symlink file")
    flags = os.O_RDONLY | getattr(os, 'O_NOFOLLOW', 0) | getattr(os, 'O_NONBLOCK', 0) | getattr(os, 'O_BINARY', 0)
    fd = os.open(path, flags)
    with os.fdopen(fd, 'rb') as handle:
        opened = os.fstat(handle.fileno())
        need(stat.S_ISREG(opened.st_mode) and (before.st_dev, before.st_ino) == (opened.st_dev, opened.st_ino),
             "JSON: file changed while opening")
        raw = handle.read(MAX_BYTES + 1)
    need(len(raw) <= MAX_BYTES, "JSON: file exceeds 2 MB safety limit")
    # JSON grammar depth is checked before the recursive stdlib decoder runs.
    depth, quoted, escaped = 0, False, False
    for byte in raw:
        if quoted:
            if escaped:
                escaped = False
            elif byte == 92:
                escaped = True
            elif byte == 34:
                quoted = False
        elif byte == 34:
            quoted = True
        elif byte in (91, 123):
            depth += 1
            need(depth <= MAX_DEPTH, "JSON: nesting exceeds 32 levels")
        elif byte in (93, 125):
            depth -= 1
    try:
        value = json.loads(raw.decode('utf-8'), object_pairs_hook=no_duplicate_keys, parse_constant=reject_constant)
    except (UnicodeError, json.JSONDecodeError, RecursionError) as exc:
        raise Invalid("JSON: invalid UTF-8 or JSON syntax") from exc
    check_shape(value)
    return value


def no_symlink_ancestors(path: Path) -> None:
    # Inspect the user spelling before resolve() erases symlinks.
    for part in (path, *path.parents):
        need(not part.is_symlink(), "workspace: symlink paths are forbidden")


def write_workspace(destination: Path, contents: dict[str, str]) -> None:
    """Use an owned parent directory; protects against accidents, not a hostile filesystem owner."""
    no_symlink_ancestors(destination)
    destination.mkdir(parents=True, exist_ok=False, mode=0o700)
    created = []
    try:
        for name, content in contents.items():
            need(Path(name).name == name and name not in ('.', '..'), "workspace: invalid output filename")
            path = destination / name
            with path.open('x', encoding='utf-8', newline='\n') as handle:
                created.append(path)
                handle.write(content)
    except (OSError, ValueError):
        # Remove only files this call created, never recursively delete a directory.
        for path in created:
            try:
                path.unlink()
            except OSError:
                pass
        try:
            destination.rmdir()
        except OSError:
            pass
        raise
