# Scope and Limitations

## Project Scope

Subsurface Data Lab is an open engineering workflow designed to reconstruct **chronological operational history** of wells from legacy field documentation.

The project focuses on transforming unstructured operational records into structured, human-understandable and machine-readable well history.

The system is intended to:

- extract operational events from drilling and completion documentation
- reconstruct well construction sequences
- identify major operational incidents (losses, kicks, NPT)
- allow cross-well comparison of operational history
- assist engineering review and regulatory understanding

The workflow emphasises **reproducibility, transparency, and interpretability** rather than automation accuracy or optimisation.

---

## Intended Use

The outputs produced by Subsurface Data Lab are designed to support:

- engineering understanding of legacy wells
- decommissioning review
- well integrity screening
- academic research
- CO₂ storage context assessment
- educational use

The system provides a structured interpretation of historical operational records.

It is a **decision-support and review tool**, not a decision-making system.

---

## Explicit Non-Goals

Subsurface Data Lab is **not** intended to:

- predict well failure
- perform reservoir simulation
- replace well integrity engineering assessment
- perform pressure modelling
- calculate abandonment design
- replace regulatory review
- act as a real-time monitoring system
- function as a commercial operational platform

The project reconstructs *what happened*, not *what will happen*.

---

## Limitations

The workflow depends on the quality and completeness of legacy records.

Known limitations include:

- incomplete daily drilling reports
- inconsistent reporting language
- missing dates or timestamps
- OCR errors in scanned documents
- ambiguous operational descriptions

Because the system extracts information from human-written reports, some operational events may be:

- misclassified
- partially reconstructed
- missing entirely

The system therefore cannot guarantee a complete operational history.

---

## Engineering Responsibility

The outputs of Subsurface Data Lab:

- are informational
- are interpretive
- require engineering judgement

They must not be used as the sole basis for operational, safety, abandonment, or regulatory decisions.

Qualified engineers and regulators remain responsible for evaluation of well integrity and risk.

---

## Philosophy

The project assumes:

Legacy well documentation contains valuable engineering knowledge, but it is locked inside human-readable records.

Subsurface Data Lab does not replace expert interpretation.  
It reduces the effort required to *reach* expert interpretation.

The system therefore supports engineers and regulators rather than replacing them.
