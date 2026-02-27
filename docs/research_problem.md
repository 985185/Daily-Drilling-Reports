# Research Problem

Legacy oil and gas wells contain critical operational knowledge within unstructured documents such as Daily Drilling Reports (DDRs), completion reports, and operational summaries.

These records describe how a well was actually constructed and operated, including drilling issues, losses, kicks, casing operations, cementing behaviour, and non-productive time (NPT). However, the information exists primarily as human-readable documents and cannot be queried across wells.

As a result, engineers and regulators must manually read large volumes of reports to understand well behaviour, well integrity risks, and construction history. This limits the ability to systematically analyse wells, particularly for decommissioning and CO₂ storage assessment.

There is currently no reproducible, open workflow for converting legacy well documentation into structured, machine-readable operational history.

## Objective

The objective of this project is to develop a reproducible workflow that reconstructs chronological well operational history from legacy field data.

The workflow aims to:

- identify operational events from drilling reports
- reconstruct well construction sequences
- enable cross-well comparison
- support well integrity and abandonment assessment
- support CO₂ storage and regulatory review

The system prioritises transparency and reproducibility over optimisation.

## Contribution

This project proposes that legacy well documentation can be transformed into structured engineering knowledge using a staged data workflow:

**raw field documents → indexed dataset → well-level manifests → operational event extraction → chronological well history**

The contribution is not a new machine learning model, but a reproducible engineering method for reconstructing subsurface operational history from real field records.
