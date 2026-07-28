#!/usr/bin/env python3
"""
pull_transcripts.py — Extract Wispr Flow dictation transcripts from the local
SQLite database and emit a clean bundle (JSON + Markdown) for downstream
project-planning.

Wispr Flow stores every dictation locally in `flow.sqlite`, in a `History`
table (transcript text, timestamps, source app, word counts). This script:

  1. Locates flow.sqlite across macOS / Windows / Linux (or a --db override).
  2. Introspects the schema at runtime, so it keeps working even if Wispr
     renames columns between versions.
  3. Filters by date range, source app, keyword, and minimum word count.
  4. Writes a machine-readable transcripts.json and a human/agent-readable
     transcripts.md to the output directory.

Standard library only. No dependencies, no network, nothing leaves the machine.

Usage examples
--------------
  # Everything from the last 7 days
  python3 pull_transcripts.py --since 7d --out ./bundle

  # A specific window, only dictations of 15+ words
  python3 pull_transcripts.py --from 2026-07-01 --to 2026-07-23 --min-words 15 --out ./bundle

  # Only transcripts mentioning a project keyword
  python3 pull_transcripts.py --since 30d --contains "onboarding flow" --out ./bundle

  # Point at a copied/backup DB explicitly
  python3 pull_transcripts.py --db "/path/to/flow.sqlite" --out ./bundle
"""

import argparse
import json
import os
import re
import shutil
import sqlite3
import sys
import tempfile
from datetime import datetime, timedelta, timezone
from pathlib import Path

# ----------------------------------------------------------------------------
# Locating the database
# ----------------------------------------------------------------------------

def candidate_db_paths():
    """Return likely flow.sqlite locations across platforms."""
    home = Path.home()
    paths = []
    # macOS
    paths.append(home / "Library" / "Application Support" / "Wispr Flow" / "flow.sqlite")
    # Windows (%APPDATA%\Wispr Flow)
    appdata = os.environ.get("APPDATA")
    if appdata:
        paths.append(Path(appdata) / "Wispr Flow" / "flow.sqlite")
    paths.append(home / "AppData" / "Roaming" / "Wispr Flow" / "flow.sqlite")
    # Linux (best-effort)
    paths.append(home / ".config" / "Wispr Flow" / "flow.sqlite")
    paths.append(home / ".config" / "wispr-flow" / "flow.sqlite")
    return paths


def find_db(explicit):
    if explicit:
        p = Path(explicit).expanduser()
        if not p.exists():
            sys.exit(f"ERROR: --db path does not exist: {p}")
        return p
    for p in candidate_db_paths():
        if p.exists():
            return p
    tried = "\n  ".join(str(p) for p in candidate_db_paths())
    sys.exit(
        "ERROR: Could not find flow.sqlite automatically. Tried:\n  "
        + tried
        + "\n\nMake sure Wispr Flow is installed with local history enabled, "
        "or pass --db /path/to/flow.sqlite. If Wispr Flow is running and the "
        "DB is locked, quit it or copy the file first."
    )


def open_readonly(db_path):
    """Open the DB read-only. Falls back to a temp copy if the live file is locked."""
    uri = f"file:{db_path}?mode=ro&immutable=1"
    try:
        conn = sqlite3.connect(uri, uri=True)
        conn.execute("SELECT 1")
        return conn, db_path
    except sqlite3.Error:
        # Copy sidecar files too (-wal/-shm) so a live DB reads cleanly.
        tmpdir = Path(tempfile.mkdtemp(prefix="wispr_"))
        for suffix in ("", "-wal", "-shm"):
            src = Path(str(db_path) + suffix)
            if src.exists():
                shutil.copy2(src, tmpdir / (db_path.name + suffix))
        copy = tmpdir / db_path.name
        conn = sqlite3.connect(f"file:{copy}?mode=ro", uri=True)
        return conn, copy


# ----------------------------------------------------------------------------
# Schema introspection
# ----------------------------------------------------------------------------

def list_tables(conn):
    rows = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table'"
    ).fetchall()
    return [r[0] for r in rows]


def find_history_table(conn):
    tables = list_tables(conn)
    # Prefer an exact/most-likely match, then anything that looks like history.
    for want in ("History", "history", "Transcriptions", "transcripts", "dictations"):
        for t in tables:
            if t.lower() == want.lower():
                return t
    for t in tables:
        if any(k in t.lower() for k in ("history", "transcri", "dictat")):
            return t
    return tables[0] if tables else None


def columns(conn, table):
    rows = conn.execute(f'PRAGMA table_info("{table}")').fetchall()
    return [r[1] for r in rows]  # column names


def pick(colnames, wanted_substrings):
    """Return the first column whose lowercased name contains any wanted substring."""
    low = {c.lower(): c for c in colnames}
    for want in wanted_substrings:
        for lc, orig in low.items():
            if want in lc:
                return orig
    return None


# ----------------------------------------------------------------------------
# Time parsing / filtering
# ----------------------------------------------------------------------------

def parse_since(value):
    """Accept '7d', '48h', '30m', or an ISO date, return a datetime (UTC)."""
    now = datetime.now(timezone.utc)
    m = re.fullmatch(r"(\d+)\s*([dhm])", value.strip().lower())
    if m:
        n, unit = int(m.group(1)), m.group(2)
        delta = {"d": timedelta(days=n), "h": timedelta(hours=n), "m": timedelta(minutes=n)}[unit]
        return now - delta
    return parse_date(value)


def parse_date(value):
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d"):
        try:
            return datetime.strptime(value, fmt).replace(tzinfo=timezone.utc)
        except ValueError:
            continue
    sys.exit(f"ERROR: Could not parse date/time: {value!r}")


def to_datetime(raw):
    """Best-effort conversion of a DB timestamp value into a datetime (UTC)."""
    if raw is None:
        return None
    # Numeric epoch (seconds, millis, or micros)
    if isinstance(raw, (int, float)):
        v = float(raw)
        if v > 1e17:      # nanoseconds
            v /= 1e9
        elif v > 1e14:    # microseconds
            v /= 1e6
        elif v > 1e11:    # milliseconds
            v /= 1e3
        try:
            return datetime.fromtimestamp(v, tz=timezone.utc)
        except (OverflowError, OSError, ValueError):
            return None
    s = str(raw).strip()
    if not s:
        return None
    if s.isdigit():
        return to_datetime(int(s))
    s = s.replace("Z", "+00:00")
    # Normalise a space before the UTC offset: "... .835 +00:00" -> "... .835+00:00"
    s = re.sub(r"\s+([+-]\d{2}:?\d{2})$", r"\1", s)
    for fmt in ("%Y-%m-%d %H:%M:%S.%f%z", "%Y-%m-%d %H:%M:%S%z",
                "%Y-%m-%d %H:%M:%S.%f", "%Y-%m-%d %H:%M:%S",
                "%Y-%m-%dT%H:%M:%S.%f%z", "%Y-%m-%dT%H:%M:%S%z",
                "%Y-%m-%dT%H:%M:%S.%f", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d"):
        try:
            dt = datetime.strptime(s, fmt)
            return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)
        except ValueError:
            continue
    try:
        dt = datetime.fromisoformat(s)
        return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)
    except ValueError:
        return None


# ----------------------------------------------------------------------------
# App id -> friendly name (best-effort; unknown ids pass through)
# ----------------------------------------------------------------------------

APP_NAMES = {
    "com.tinyspeck.slackmacgap": "Slack",
    "com.microsoft.vscode": "VS Code",
    "com.google.chrome": "Chrome",
    "com.apple.mail": "Mail",
    "com.apple.notes": "Notes",
    "com.apple.dt.xcode": "Xcode",
    "notion.id": "Notion",
    "com.linear": "Linear",
    "com.figma.desktop": "Figma",
    "com.hnc.discord": "Discord",
    "com.apple.safari": "Safari",
    "com.microsoft.teams2": "Microsoft Teams",
    "md.obsidian": "Obsidian",
    "com.openai.chat": "ChatGPT",
    "com.anthropic.claudefordesktop": "Claude",
}


def friendly_app(raw):
    if not raw:
        return "Unknown"
    return APP_NAMES.get(str(raw).lower().strip(), str(raw))


# ----------------------------------------------------------------------------
# Main extraction
# ----------------------------------------------------------------------------

def extract(conn, args):
    table = find_history_table(conn)
    if not table:
        sys.exit("ERROR: No tables found in the database.")
    cols = columns(conn, table)

    text_col = pick(cols, ["asr_text", "formatted", "transcript", "text", "content", "result", "output"])
    time_col = pick(cols, ["timestamp", "created", "date", "time", "start"])
    app_col = pick(cols, ["app", "bundle", "source", "context"])
    words_col = pick(cols, ["word", "num_words", "count"])

    if not text_col:
        sys.exit(
            f"ERROR: Could not find a transcript text column in table '{table}'.\n"
            f"Columns present: {cols}\n"
            "Re-run with --db and inspect, or open an issue with the column list."
        )

    rows = conn.execute(f'SELECT * FROM "{table}"').fetchall()
    idx = {c: i for i, c in enumerate(cols)}

    since_dt = parse_since(args.since) if args.since else None
    from_dt = parse_date(getattr(args, "from")) if getattr(args, "from") else None
    to_dt = parse_date(args.to) if args.to else None
    contains = args.contains.lower() if args.contains else None

    records = []
    for r in rows:
        text = r[idx[text_col]]
        if text is None or not str(text).strip():
            continue
        text = str(text).strip()

        dt = to_datetime(r[idx[time_col]]) if time_col else None
        if since_dt and (dt is None or dt < since_dt):
            continue
        if from_dt and (dt is None or dt < from_dt):
            continue
        if to_dt and (dt is None or dt > to_dt + timedelta(days=1)):
            continue

        app = friendly_app(r[idx[app_col]]) if app_col else "Unknown"
        if args.app and args.app.lower() not in app.lower():
            continue

        wc = None
        if words_col and r[idx[words_col]] is not None:
            try:
                wc = int(r[idx[words_col]])
            except (ValueError, TypeError):
                wc = None
        if wc is None:
            wc = len(text.split())
        if args.min_words and wc < args.min_words:
            continue

        if contains and contains not in text.lower():
            continue

        records.append({
            "timestamp": dt.isoformat() if dt else None,
            "app": app,
            "words": wc,
            "text": text,
        })

    # Chronological order (undated entries last).
    records.sort(key=lambda x: (x["timestamp"] is None, x["timestamp"] or ""))
    return table, records


def write_outputs(records, table, db_path, outdir):
    outdir = Path(outdir).expanduser()
    outdir.mkdir(parents=True, exist_ok=True)

    total_words = sum(r["words"] for r in records)
    dated = [r["timestamp"] for r in records if r["timestamp"]]
    meta = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source_db": str(db_path),
        "source_table": table,
        "transcript_count": len(records),
        "total_words": total_words,
        "earliest": min(dated) if dated else None,
        "latest": max(dated) if dated else None,
    }

    json_path = outdir / "transcripts.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump({"meta": meta, "transcripts": records}, f, indent=2, ensure_ascii=False)

    md_path = outdir / "transcripts.md"
    with open(md_path, "w", encoding="utf-8") as f:
        f.write("# Wispr Flow transcript bundle\n\n")
        f.write(f"- Generated: {meta['generated_at']}\n")
        f.write(f"- Transcripts: {meta['transcript_count']}\n")
        f.write(f"- Total words: {meta['total_words']:,}\n")
        if meta["earliest"]:
            f.write(f"- Range: {meta['earliest']} to {meta['latest']}\n")
        f.write("\n---\n\n")
        for i, r in enumerate(records, 1):
            ts = r["timestamp"] or "undated"
            f.write(f"## {i}. {ts} - {r['app']} ({r['words']} words)\n\n")
            f.write(r["text"].strip() + "\n\n")

    return json_path, md_path, meta


def main():
    ap = argparse.ArgumentParser(description="Pull Wispr Flow transcripts into a clean bundle.")
    ap.add_argument("--db", help="Path to flow.sqlite (auto-detected if omitted)")
    ap.add_argument("--out", default="./wispr_bundle", help="Output directory")
    ap.add_argument("--since", help="Relative window, e.g. 7d, 48h, 30m")
    ap.add_argument("--from", dest="from", help="Start date YYYY-MM-DD")
    ap.add_argument("--to", help="End date YYYY-MM-DD (inclusive)")
    ap.add_argument("--app", help="Only include a source app (substring match)")
    ap.add_argument("--contains", help="Only include transcripts containing this text")
    ap.add_argument("--min-words", type=int, default=0, help="Drop transcripts under N words")
    args = ap.parse_args()

    db_path = find_db(args.db)
    conn, opened = open_readonly(db_path)
    try:
        table, records = extract(conn, args)
    finally:
        conn.close()

    json_path, md_path, meta = write_outputs(records, table, db_path, args.out)

    print(f"Source DB : {db_path}")
    print(f"Table     : {table}")
    print(f"Extracted : {meta['transcript_count']} transcripts, {meta['total_words']:,} words")
    if meta["earliest"]:
        print(f"Range     : {meta['earliest']} -> {meta['latest']}")
    print(f"JSON      : {json_path}")
    print(f"Markdown  : {md_path}")
    if meta["transcript_count"] == 0:
        print("\nNOTE: 0 transcripts matched. Loosen filters (--since, --min-words, --contains) "
              "or check that the DB has history.")


if __name__ == "__main__":
    main()
