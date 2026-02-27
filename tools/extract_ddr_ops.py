#!/usr/bin/env python3
"""
extract_ddr_ops.py

Batch-extract DDR "Operations" table rows from Volve-style DDR HTML files and write JSONL events.

Key design choices:
- Deterministic extraction (no AI)
- Minimal dependencies (beautifulsoup4 only)
- report_date is derived from filename and treated as authoritative day label
- header period dates (period_start_date, period_end_date) are captured separately

Usage:
  pip install beautifulsoup4
  python tools/extract_ddr_ops.py --input "/path/to/ddr_html_folder" --output "./out_events" --recursive --overwrite

Safe test:
  python tools/extract_ddr_ops.py --input "/path/to/ddr_html_folder" --output "./out_events" --recursive --dry-run
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple

try:
    from bs4 import BeautifulSoup  # type: ignore
except ImportError:
    print("ERROR: Missing dependency 'beautifulsoup4'. Install with: pip install beautifulsoup4", file=sys.stderr)
    sys.exit(1)


@dataclass
class ExtractMeta:
    input_file: Path
    output_file: Optional[Path]
    events_written: int
    wellbore: Optional[str]
    report_date: Optional[str]
    period_start_date: Optional[str]
    period_end_date: Optional[str]
    error: Optional[str]


WELLBORE_RE = re.compile(r"Wellbore:\s*([0-9/.\-\sA-Za-z]+?)\s+Period:", re.IGNORECASE)
PERIOD_RE = re.compile(
    r"Period:\s*(\d{4}-\d{2}-\d{2})\s+\d{2}:\d{2}\s*-\s*(\d{4}-\d{2}-\d{2})\s+\d{2}:\d{2}",
    re.IGNORECASE,
)

# Example filenames:
# 15_9_19_A_1997_10_10.html
# 15_9_F_15_A_2008_12_22.html
FILENAME_DATE_RE = re.compile(r".*_(\d{4})_(\d{2})_(\d{2})\.html$", re.IGNORECASE)


def safe_read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def parse_header_wellbore(soup: BeautifulSoup) -> Optional[str]:
    text = soup.get_text(" ", strip=True)
    m = WELLBORE_RE.search(text)
    return m.group(1).strip() if m else None


def parse_header_period_dates(soup: BeautifulSoup) -> Tuple[Optional[str], Optional[str]]:
    text = soup.get_text(" ", strip=True)
    m = PERIOD_RE.search(text)
    if not m:
        return None, None
    return m.group(1), m.group(2)


def parse_report_date_from_filename(html_path: Path) -> Optional[str]:
    m = FILENAME_DATE_RE.match(html_path.name)
    if not m:
        return None
    y, mo, d = m.group(1), m.group(2), m.group(3)
    try:
        datetime(int(y), int(mo), int(d))
    except ValueError:
        return None
    return f"{y}-{mo}-{d}"


def parse_wellbore_from_filename(html_path: Path) -> Optional[str]:
    """
    Best-effort conversion:
      15_9_F_15_A_2008_12_22.html -> 15/9-F-15 A
    Header parsing is preferred.
    """
    stem = html_path.stem
    parts = stem.split("_")
    if len(parts) < 4:
        return None

    year_idx = None
    for i, p in enumerate(parts):
        if re.fullmatch(r"\d{4}", p):
            year_idx = i
            break
    if year_idx is None or year_idx < 2:
        return None

    well_tokens = parts[:year_idx]  # e.g. ["15","9","F","15","A"]
    if len(well_tokens) < 2:
        return None

    prefix = f"{well_tokens[0]}/{well_tokens[1]}"
    rest = well_tokens[2:]

    if not rest:
        return prefix

    suffix_letter = rest[-1] if len(rest[-1]) == 1 and rest[-1].isalpha() else None
    core = rest[:-1] if suffix_letter else rest

    core_str = "-".join(core) if core else ""
    wb = f"{prefix}-{core_str}" if core_str else prefix
    if suffix_letter:
        wb = f"{wb} {suffix_letter}"
    return wb


def find_operations_table(soup: BeautifulSoup):
    """
    Volve DDR HTML commonly uses id='operationsInfoTable'.
    Fallback: locate a table that appears to contain relevant headers.
    """
    table = soup.find("table", {"id": "operationsInfoTable"})
    if table is not None:
        return table

    for t in soup.find_all("table"):
        header_text = t.get_text(" ", strip=True).lower()
        if "remark" in header_text and "activity" in header_text and "state" in header_text:
            return t

    return None


def extract_events_from_html(html_path: Path) -> Tuple[ExtractMeta, List[Dict]]:
    try:
        html = safe_read_text(html_path)
        soup = BeautifulSoup(html, "html.parser")

        wellbore = parse_header_wellbore(soup) or parse_wellbore_from_filename(html_path)

        # Option 1: authoritative day label is filename date
        report_date = parse_report_date_from_filename(html_path)

        # Header period dates captured separately
        period_start_date, period_end_date = parse_header_period_dates(soup)

        table = find_operations_table(soup)
        if table is None:
            meta = ExtractMeta(
                input_file=html_path,
                output_file=None,
                events_written=0,
                wellbore=wellbore,
                report_date=report_date,
                period_start_date=period_start_date,
                period_end_date=period_end_date,
                error="Could not find Operations table (operationsInfoTable).",
            )
            return meta, []

        rows = table.find_all("tr")
        if len(rows) < 2:
            meta = ExtractMeta(
                input_file=html_path,
                output_file=None,
                events_written=0,
                wellbore=wellbore,
                report_date=report_date,
                period_start_date=period_start_date,
                period_end_date=period_end_date,
                error="Operations table has no data rows.",
            )
            return meta, []

        events: List[Dict] = []
        for r in rows[1:]:
            cols = [c.get_text(" ", strip=True) for c in r.find_all("td")]
            if len(cols) < 6:
                continue

            start, end, depth, activity, state, remark = cols[:6]

            event = {
                "wellbore": wellbore,
                "report_date": report_date,
                "period_start_date": period_start_date,
                "period_end_date": period_end_date,
                "start_time": start,
                "end_time": end,
                "activity_raw": activity,
                "state": state,
                "remark": remark,
                "end_depth_md": depth if depth != "" else None,
                "event_type": None,
                "source_file": html_path.name,
            }
            events.append(event)

        out_name = html_path.with_suffix("").name + "_events.jsonl"
        meta = ExtractMeta(
            input_file=html_path,
            output_file=Path(out_name),
            events_written=len(events),
            wellbore=wellbore,
            report_date=report_date,
            period_start_date=period_start_date,
            period_end_date=period_end_date,
            error=None,
        )
        return meta, events

    except Exception as e:
        meta = ExtractMeta(
            input_file=html_path,
            output_file=None,
            events_written=0,
            wellbore=None,
            report_date=None,
            period_start_date=None,
            period_end_date=None,
            error=str(e),
        )
        return meta, []


def iter_html_files(input_path: Path, recursive: bool) -> Iterable[Path]:
    if input_path.is_file() and input_path.suffix.lower() == ".html":
        yield input_path
        return

    if input_path.is_dir():
        pattern = "**/*.html" if recursive else "*.html"
        for p in sorted(input_path.glob(pattern)):
            if p.is_file():
                yield p
        return

    raise FileNotFoundError(f"Input path not found: {input_path}")


def write_jsonl(output_dir: Path, out_name: str, events: List[Dict], overwrite: bool) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    out_path = output_dir / out_name

    if out_path.exists() and not overwrite:
        raise FileExistsError(f"Output exists (use --overwrite): {out_path}")

    with out_path.open("w", encoding="utf-8") as f:
        for ev in events:
            f.write(json.dumps(ev, ensure_ascii=False) + "\n")

    return out_path


def main() -> int:
    parser = argparse.ArgumentParser(description="Extract DDR Operations table to JSONL events.")
    parser.add_argument("--input", required=True, help="Path to a DDR HTML file or a folder of HTML files.")
    parser.add_argument("--output", required=True, help="Output folder for JSONL files.")
    parser.add_argument("--recursive", action="store_true", help="Recursively search for .html files in subfolders.")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite existing output files.")
    parser.add_argument("--dry-run", action="store_true", help="Parse and report counts, but do not write outputs.")
    args = parser.parse_args()

    input_path = Path(args.input).expanduser().resolve()
    output_dir = Path(args.output).expanduser().resolve()

    html_files = list(iter_html_files(input_path, args.recursive))
    if not html_files:
        print("No .html files found.", file=sys.stderr)
        return 2

    total_events = 0
    ok_files = 0
    failed_files = 0

    for html_path in html_files:
        meta, events = extract_events_from_html(html_path)

        if meta.error:
            failed_files += 1
            print(f"[FAIL] {html_path.name} :: {meta.error}")
            continue

        out_name = html_path.with_suffix("").name + "_events.jsonl"
        if args.dry_run:
            print(f"[OK]   {html_path.name} -> {len(events)} events (dry-run)")
        else:
            out_path = write_jsonl(output_dir, out_name, events, overwrite=args.overwrite)
            print(f"[OK]   {html_path.name} -> {len(events)} events -> {out_path}")

        ok_files += 1
        total_events += len(events)

        print(
            f"       parsed: wellbore={meta.wellbore!r}, report_date={meta.report_date!r}, "
            f"period_start_date={meta.period_start_date!r}, period_end_date={meta.period_end_date!r}"
        )

    print("\nSummary")
    print(f"  HTML files: {len(html_files)}")
    print(f"  OK: {ok_files}")
    print(f"  Failed: {failed_files}")
    print(f"  Total events written: {total_events}" if not args.dry_run else f"  Total events parsed: {total_events}")

    return 0 if failed_files == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
