# Event Type Vocabulary (v0.1)

This document defines the controlled vocabulary used for `event_type` in DDR day event JSONL outputs.

The goal is a small, stable set of engineering-meaningful categories that can be applied deterministically from `activity_raw` and `remark`.

## Rules

- Exactly one `event_type` per DDR Operations row.
- Prefer the most specific applicable type.
- Keep the vocabulary stable; extend only when necessary.
- If uncertain, use `OTHER`.

## Event Types

### DRILLING
Primary drilling operations (drilling ahead, drilling out, etc.).

### TRIP
Tripping operations and pipe movement (RIH, POOH, trips).

### WIRELINE
Wireline / logging activities (run logs, rig up/down wireline, logging tool handling).

### DST
Drill Stem Test operations and related DST setup/handling.

### CASING
Casing and liner related operations (run casing/liner, casing equipment handling).

### CEMENTING
Cementing operations and WOC (wait on cement) related reporting.

### PERFORATION
Perforating operations (perforate, perforating guns, shooting).

### MUD_CONDITIONING
Circulation, conditioning mud, mud treatment/weight changes, LCM, losses mitigation where primarily mud-focused.

### TESTING
Pressure tests and integrity tests (BOP test, FIT/LOT, pressure test) not classified as DST.

### RIG_UP_DOWN
Rig up / rig down of major equipment when that is the primary activity.

### WAITING
Waiting periods (waiting on weather, standby, waiting on orders/services) where no primary operation occurs.

### EQUIPMENT_FAILURE
Explicit equipment failures (failed, failure, malfunction) as the primary reported event.

### WELL_CONTROL
Well control events (kick, shut-in, well control actions).

### OTHER
Fallback when none of the above clearly applies.

## Mapping Source

v0.1 mapping is implemented in:
- `tools/classify_event.py`

This vocabulary file is the authoritative source. If the vocabulary changes, update this file first, then update the classifier.
