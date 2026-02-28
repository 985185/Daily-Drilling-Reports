# Subsurface Data Lab

**DDR HTML in. Engineering timeline out.**

An open, deterministic well-history reconstruction tool that converts Daily Drilling Reports into a machine-readable construction timeline — without manually reading 70+ days of logs.

---

## What it does

Daily Drilling Reports (DDRs) contain the complete operational history of a well. They are written for humans. This tool makes them usable for machines.

The pipeline takes raw DDR HTML, parses each operational entry, classifies it into a typed engineering event, and assembles those events into a smoothed phase-block timeline that reflects how the well was actually constructed.

The result is a reproducible, auditable sequence of what happened — drilling, casing, cementing, pressure tests, tripping, waiting — organised chronologically and ready for analysis.

---

## Who it's for

- **Regulators and auditors** reconstructing legacy well history from archived documents
- **Engineers** building well timelines or operational narratives for integrity review or abandonment planning
- **Researchers** who need a reproducible, citable method for operational data analysis (SPE-compatible workflow)

---

## What makes it different

**Deterministic and explainable.** Same input always produces the same output. No black-box inference. Every classification decision follows explicit rules that can be audited.

**Engineering-aware.** The classifier understands the difference between *construction progress* (drilling ahead, running casing, cementing) and *support activity* (waiting on cement, conditioning mud, wireline runs, trips). Support activity is recorded but does not advance the construction phase.

**Integrity tests are a first-class event type.** FIT, LOT, and pressure tests are classified separately so they cannot corrupt drilling-phase logic or be misread as operational progress.

**Reproducible for research.** The method is rule-based and versioned. Results can be independently verified and the approach can be cited.

---

## Output formats

**Event-level JSONL** — one typed operational event per DDR entry, preserving date, duration, classification, and source text.

Example event record:
```json
{
  "date": "2008-12-04",
  "day_number": 12,
  "event_type": "CEMENTING",
  "phase": "12-1/4\" HOLE",
  "duration_hrs": 6.5,
  "source_text": "Pumped 120 bbls lead slurry and 80 bbls tail slurry. WOC 8 hrs.",
  "is_construction_progress": true
}
```

**Phase blocks** — a smoothed macro-timeline of construction phases, suitable for well history charts or regulatory summaries.

Example phase block:
```json
{
  "phase": "12-1/4\" HOLE",
  "start_date": "2008-11-28",
  "end_date": "2008-12-06",
  "duration_days": 8,
  "key_events": ["DRILL_AHEAD", "WIPER_TRIP", "LOT", "CEMENTING"]
}
```

---

## Quickstart

**Requirements:** Python 3.9+, dependencies in `requirements.txt`

```bash
git clone https://github.com/985185/subsurface-data-lab.git
cd subsurface-data-lab
pip install -r requirements.txt
```

**Run the pipeline on the included example:**

```bash
[command to parse DDR HTML → structured rows]
[command to classify rows → event JSONL]
[command to convert events → phase blocks]
```

Output will appear in `examples/output/`.

See [`GETTING_STARTED.md`](GETTING_STARTED.md) for a full walkthrough using the Volve F-15A well (December 2008 drilling campaign).

---

## Repository structure

```
tools/          Core engine — DDR parser, event classifier, phase-block builder
examples/       Minimal worked example: input DDR → output JSONL and phase blocks
docs/           Method documentation, classification rules, design decisions
schema/         JSON schemas for event and phase-block output formats
```

---

## Data source

Initial development and the v1.0 release use the publicly available **Volve Field dataset** released by Equinor — one of the most complete open petroleum field data releases available, and a realistic test environment for reproducible subsurface workflows.

The v1.0 release reconstructs the **F-15A well, December 2008 drilling campaign**.

---

## Project status

Active research project. The pipeline is functional and versioned. Development prioritises transparency and reproducibility.

See [`VERSION.md`](VERSION.md) for what is currently frozen and what is in progress.

---

## Citation

If you use this work in research or regulatory analysis, please cite using [`CITATION.cff`](CITATION.cff).

---

## License

MIT — free to use, adapt, and build on.
