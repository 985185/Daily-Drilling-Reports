"""
classify_event.py

Deterministic event typing for DDR operations.

Key improvements:
- Split "testing" into INTEGRITY_TEST vs true well TESTING (flow/DST context)
- Avoid false TESTING from choke/kill-line displacement operations (common in P&A / well control support)
"""

import re

SLOT_MOVE_RE = re.compile(
    r"""(
        \bskid(ding)?\b |
        \bslot\b.*\b(move|moving|relocat|shift)\b |
        \brig\b.*\b(move|moving)\b |
        \b(move|moving)\b.*\bslot\b
    )""",
    re.IGNORECASE | re.VERBOSE,
)

def _t(activity_raw: str, remark: str) -> str:
    return ((activity_raw or "") + " " + (remark or "")).lower()

def _is_integrity_test(t: str) -> bool:
    if "bop" in t and "test" in t:
        return True
    if "pressure" in t and "test" in t:
        return True
    if "leak" in t and "test" in t:
        return True
    if "function" in t and "test" in t:
        return True
    if "formation integrity test" in t:
        return True
    if "casing" in t and "test" in t:
        return True
    if "annular" in t and "test" in t:
        return True
    if re.search(r"\bfit\b", t):
        return True
    if re.search(r"\blot\b", t):
        return True
    return False

def _is_displacement_ops(t: str) -> bool:
    """
    Identify displacement / fluid swap operations that often mention choke/kill lines
    but are NOT well tests.
    """
    displacement_cues = [
        "displace", "displaced", "displacement",
        "kill line", "kill / choke", "kill/choke", "kill-",
        "choke line", "chokeline",
        "choke manifold", "chokemanifold", "chokemanifoild",  # seen typo in your data
        "manifold",
        "to obm", "from obm", "sg obm", "sg wbm", "brine", "seawater",
        "fluid swap", "mud weight", "sg ",
        "circulate to", "circulated to", "circulation"
    ]
    return any(c in t for c in displacement_cues)

def _is_well_test(t: str) -> bool:
    """
    True well testing cues (flow-related). Excludes displacement/well-control support ops.
    """
    # hard negative gate: displacement ops are not tests
    if _is_displacement_ops(t):
        return False

    if "well test" in t or "flow test" in t:
        return True

    flow_cues = [
        "flowing", "flowed", "choke", "separator", "flare",
        "buildup", "drawdown", "shut in", "shutin",
        "rate", "production test"
    ]
    if any(c in t for c in flow_cues):
        return True

    if re.search(r"\b(stb|bopd|sm3/d|m3/d)\b", t):
        return True

    return False

def classify_event(activity_raw: str, remark: str) -> str:
    a = (activity_raw or "").lower()
    r = (remark or "").lower()
    t = _t(activity_raw, remark)

    # flags (never dominant)
    if "fail" in r or "failed" in r:
        return "EQUIPMENT_FAILURE"
    if "kick" in r or "well control" in r:
        return "WELL_CONTROL"

    # slot move
    if SLOT_MOVE_RE.search(activity_raw or "") or SLOT_MOVE_RE.search(remark or ""):
        return "SLOT_MOVE"

    # DST explicit
    if "dst" in t:
        return "DST"

    # integrity tests
    if _is_integrity_test(t):
        return "INTEGRITY_TEST"

    # displacement ops: treat as mud conditioning (support)
    if _is_displacement_ops(t):
        return "MUD_CONDITIONING"

    # true well tests
    if _is_well_test(t):
        return "TESTING"

    # operations
    if "cement" in t:
        return "CEMENTING"
    if "casing" in t:
        return "CASING"
    if "perforat" in t:
        return "PERFORATION"
    if "wire" in a or "wireline" in t or "log" in t:
        return "WIRELINE"
    if "trip" in a or "rih" in t or "pooh" in t:
        return "TRIP"
    if "drill" in a:
        return "DRILLING"
    if "mud" in t or "circulation" in t or "circ." in t:
        return "MUD_CONDITIONING"
    if "rig up" in t or "rig down" in t or "r/u" in t or "r/d" in t:
        return "RIG_UP_DOWN"
    if "wait" in t or "weather" in t:
        return "WAITING"

    return "OTHER"
