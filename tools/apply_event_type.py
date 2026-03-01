#!/usr/bin/env python3
"""
LW-DTRE
Deterministic event typing for DDR operational records.

Usage:
    python apply_event_type.py --in input.jsonl --out output.jsonl
"""

import argparse
import json
import re
from pathlib import Path

# -------------------------
# Rule Definitions
# -------------------------

PRIMARY_RULES = {
    "DRILLING": [
        r"\bdrill",
        r"\bdrilling",
        r"\bre-drill",
    ],
    "CASING": [
        r"\bcasing",
        r"\brunning casing",
        r"\bset casing",
    ],
    "CEMENTING": [
        r"\bcement",
        r"\bcementing",
        r"\bshoe track",
    ],
    "PERFORATION": [
        r"\bperforat",
    ],
    "DST": [
        r"\bdst\b",
        r"\bdrill stem test",
    ],
    "TESTING": [
        r"\bwell test",
        r"\bproduction test",
    ],
    "SLOT_MOVE": [
        r"\bslot move",
        r"\bskid rig",
    ],
}

SUPPORT_RULES = {
    "TRIP": [
        r"\btrip",
        r"\btripping",
    ],
    "WAITING": [
        r"\bwait",
        r"\bstandby",
    ],
    "WIRELINE": [
        r"\bwireline",
    ],
    "MUD_CONDITIONING": [
        r"\bmud",
        r"\bcondition",
        r"\bcirculate",
    ],
    "INTEGRITY_TEST": [
        r"\bfit\b",
        r"\blot\b",
        r"\bpressure test",
        r"\bnegative test",
    ],
    "WELL_CONTROL": [
        r"\bwell control",
        r"\bkill mud",
        r"\bkick",
    ],
    "EQUIPMENT_FAILURE": [
        r"\bfailure",
        r"\brepair",
        r"\bmalfunction",
    ],
}

# Order matters (primary before support)
ALL_RULES = [(k, v) for k, v in PRIMARY_RULES.items()] + \
            [(k, v) for k, v in SUPPORT_RULES.items()]

# -------------------------
# Classification
# -------------------------

def classify(activity: str, remark: str) -> str | None:
    text = f"{activity} {remark}".lower()

    for label, patterns in ALL_RULES:
        for pat in patterns:
            if re.search(pat, text):
                return label

    return None


# -------------------------
# Main
# -------------------------

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--in", dest="infile", required=True)
    parser.add_argument("--out", dest="outfile", required=True)
    args = parser.parse_args()

    infile = Path(args.infile)
    outfile = Path(args.outfile)

    if not infile.exists():
        raise FileNotFoundError(f"Input not found: {infile}")

    written = 0

    with infile.open("r", encoding="utf-8") as f_in, \
         outfile.open("w", encoding="utf-8") as f_out:

        for line in f_in:
            line = line.strip()
            if not line:
                continue

            obj = json.loads(line)

            activity = obj.get("activity_raw", "")
            remark = obj.get("remark", "")

            obj["event_type"] = classify(activity, remark)

            f_out.write(json.dumps(obj, ensure_ascii=False) + "\n")
            written += 1

    print(f"Wrote {written} typed events to {outfile}")


if __name__ == "__main__":
    main()
