"""
classify_event.py

Rule-based normalization of DDR events into controlled event_type vocabulary.

Design principles:
- Deterministic
- Interpretable
- Order-sensitive (more specific rules first)
- No ML
"""

def classify_event(activity_raw: str, remark: str) -> str:
    a = (activity_raw or "").lower()
    r = (remark or "").lower()

    # --- Critical / override conditions first ---

    if "fail" in r or "failed" in r:
        return "EQUIPMENT_FAILURE"

    if "kick" in r or "well control" in r:
        return "WELL_CONTROL"

    # --- Operational categories ---

    if "dst" in a or "dst" in r:
        return "DST"

    if "cement" in a or "cement" in r:
        return "CEMENTING"

    if "casing" in a or "casing" in r:
        return "CASING"

    if "perforat" in r:
        return "PERFORATION"

    if "wire" in a or "wireline" in r or "log" in r:
        return "WIRELINE"

    if "trip" in a or "rih" in r or "pooh" in r:
        return "TRIP"

    if "drill" in a:
        return "DRILLING"

    if "mud" in r or "circulation" in r or "circ." in r:
        return "MUD_CONDITIONING"

    if "test" in a or "test" in r:
        return "TESTING"

    if "rig up" in r or "rig down" in r or "r/u" in r or "r/d" in r:
        return "RIG_UP_DOWN"

    if "wait" in a or "wait" in r or "weather" in r:
        return "WAITING"

    # --- Default fallback ---
    return "OTHER"
