#!/usr/bin/env python3
"""scan_mermaid.py — Detect GitHub-rendered mermaid syntax issues in Markdown.

Detects:
  1. Unquoted parentheses in rectangular node labels: id[text with (parens)]
  2. Reserved words as node IDs: end, subgraph, class, style, etc.
  3. HTML tags inside unquoted labels (need quoting)
  4. Nested square brackets inside unquoted labels
  5. Colons inside unquoted node labels
  6. Pipes with special chars in edge labels

NOTE: Mermaid shape syntax is NOT a false positive:
  - id[(text)]  = cylinder/database shape (parens are shape delimiters)
  - id((text))  = circle shape
  - id{text}    = rhombus
  - id[[text]]  = subroutine
  These shapes' delimiters are NOT flagged.

Exit codes:
  0 = clean
  1 = issues found
  2 = usage error

Usage:
  scan_mermaid.py [--version] [--exclude-glob PATTERN] <path> [<path> ...]

Options:
  --version              Print version and exit
  --exclude-glob PAT     Exclude files matching this glob pattern (repeatable)
"""

from __future__ import annotations

import fnmatch
import re
import sys
from pathlib import Path

VERSION = "1.0.0"

RESERVED_IDS = {
    "end",
    "subgraph",
    "graph",
    "flowchart",
    "sequenceDiagram",
    "class",
    "style",
    "linkStyle",
    "classDef",
    "click",
    "loop",
    "alt",
    "opt",
    "par",
    "and",
    "rect",
    "fill",
    "stroke",
}

NODE_SHAPE_RE = re.compile(
    r"(\b[A-Za-z][A-Za-z0-9_]*)"
    r"("
    r"\[\[([^\]]*?)\]\]"
    r"|\[\(([^)]*?)\)\]"
    r"|\[([^\]]*?)\]"
    r"|\(\(([^)]*?)\)\)"
    r"|\(\{([^}]*?)\}\)"
    r"|\(([^)]*?)\)"
    r"|\{\{([^}]*?)\}\}"
    r"|\{([^}]*?)\}"
    r")"
)

HTML_TAG_RE = re.compile(r"<\s*/?\s*\w+[^>]*>")


def is_quoted(label: str) -> bool:
    s = label.strip()
    return len(s) >= 2 and s.startswith('"') and s.endswith('"')


def find_label_issues(label: str, shape: str) -> list[str]:
    if is_quoted(label) or not label:
        return []
    issues: list[str] = []

    if shape == "rectangle":
        if "(" in label or ")" in label:
            issues.append("unquoted parens in [label]")
        if "[" in label or "]" in label:
            issues.append("nested brackets in [label]")

    if HTML_TAG_RE.search(label):
        issues.append(f"HTML tag in {shape} label (needs quoting)")

    if ":" in label and shape in ("rectangle", "stadium", "rounded_paren"):
        issues.append(f"colon in {shape} label")

    if "|" in label:
        issues.append(f"pipe in {shape} label")

    return issues


def parse_shape(shape_match: re.Match) -> tuple[str, str]:
    if shape_match.group(3) is not None:
        return "subroutine", shape_match.group(3)
    if shape_match.group(4) is not None:
        return "cylinder", shape_match.group(4)
    if shape_match.group(5) is not None:
        return "rectangle", shape_match.group(5)
    if shape_match.group(6) is not None:
        return "circle", shape_match.group(6)
    if shape_match.group(7) is not None:
        return "rounded_brace", shape_match.group(7)
    if shape_match.group(8) is not None:
        return "stadium", shape_match.group(8)
    if shape_match.group(9) is not None:
        return "hexagon", shape_match.group(9)
    if shape_match.group(10) is not None:
        return "rhombus", shape_match.group(10)
    return "unknown", ""


def scan_mermaid_block(block: list[tuple[int, str]]) -> list[tuple[int, str, str]]:
    findings: list[tuple[int, str, str]] = []

    for lineno, line in block:
        stripped = line.strip()
        if not stripped or stripped.startswith("%%") or stripped.startswith("---"):
            continue

        for m in re.finditer(r"\b([A-Za-z][A-Za-z0-9_]*)\b", stripped):
            word = m.group(1)
            if word.lower() in RESERVED_IDS:
                after = stripped[m.end() :]
                if after and after[0] in "[({":
                    findings.append(
                        (lineno, stripped, f"reserved word '{word}' as node ID")
                    )
                    break

        for m in NODE_SHAPE_RE.finditer(stripped):
            shape, label = parse_shape(m)
            for issue in find_label_issues(label, shape):
                findings.append((lineno, stripped, issue))

        for m in re.finditer(r"-+>\s*\|([^|]+?)\|\s*", stripped):
            edge_label = m.group(1)
            if not is_quoted(edge_label) and ("(" in edge_label or ")" in edge_label):
                findings.append((lineno, stripped, "unquoted parens in edge label"))

    return findings


def scan_file(path: Path) -> list[tuple[int, str, str]]:
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as e:
        print(f"WARN: cannot read {path}: {e}", file=sys.stderr)
        return []

    lines = text.splitlines()
    findings: list[tuple[int, str, str]] = []
    in_mermaid = False
    block_start = 0
    block: list[tuple[int, str]] = []

    for i, line in enumerate(lines, start=1):
        if re.match(r"^\s*```mermaid\b", line, re.IGNORECASE):
            in_mermaid = True
            block_start = i
            block = []
            continue
        if in_mermaid:
            if re.match(r"^\s*```\s*$", line):
                in_mermaid = False
                findings.extend(scan_mermaid_block(block))
                block = []
            else:
                block.append((i, line))

    if in_mermaid:
        findings.append(
            (block_start, "<unterminated mermaid block>", "missing closing ```")
        )

    return findings


def is_excluded(path: Path, patterns: list[str]) -> bool:
    """Check if path matches any exclude glob pattern."""
    s = str(path)
    for pattern in patterns:
        # Normalize pattern — strip leading ./
        p = pattern.lstrip("./")
        if fnmatch.fnmatch(s, f"*{p}*") or fnmatch.fnmatch(s, p):
            return True
    return False


def main() -> int:
    exclude_globs: list[str] = []
    paths_args: list[str] = []

    args = sys.argv[1:]
    i = 0
    while i < len(args):
        if args[i] == "--version":
            print(f"scan_mermaid.py v{VERSION}")
            return 0
        elif args[i] == "--exclude-glob" and i + 1 < len(args):
            exclude_globs.append(args[i + 1])
            i += 2
        elif args[i] == "--help" or args[i] == "-h":
            print(__doc__)
            return 0
        else:
            paths_args.append(args[i])
            i += 1

    if not paths_args:
        print(
            "Usage: scan_mermaid.py [--version] [--exclude-glob PATTERN] <path> [<path> ...]",
            file=sys.stderr,
        )
        return 2

    paths: list[Path] = []
    for arg in paths_args:
        p = Path(arg)
        if p.is_dir():
            for f in sorted(p.rglob("*.md")):
                if not is_excluded(f, exclude_globs):
                    paths.append(f)
        elif p.suffix == ".md" and not is_excluded(p, exclude_globs):
            paths.append(p)
        else:
            print(f"WARN: skipping {p}", file=sys.stderr)

    if not paths:
        print("No Markdown files to scan.", file=sys.stderr)
        return 0

    total_findings = 0
    clean_count = 0
    cwd = Path.cwd()

    for path in paths:
        try:
            rel = path.relative_to(cwd) if path.is_absolute() else path
        except ValueError:
            rel = path
        findings = scan_file(path)
        if not findings:
            clean_count += 1
            print(f"CLEAN: {rel}")
            continue
        print(f"FILE: {rel}")
        for lineno, snippet, reason in findings:
            display = snippet if len(snippet) <= 120 else snippet[:117] + "..."
            print(f"  LINE {lineno}: `{display}` — REASON: {reason}")
            total_findings += 1
        print()

    print(f"--- Summary ---")
    print(f"Scanned: {len(paths)} files")
    print(f"Clean:   {clean_count}")
    print(f"Issues:  {total_findings}")

    return 1 if total_findings > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
