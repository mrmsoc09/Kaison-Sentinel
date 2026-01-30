# Reportability Scoring (OSINT)

Reportability is a heuristic score (0–100) used to prioritize OSINT findings for bug‑bounty reporting.

## Factors
- Confidence (base)
- Signal count (multi‑tool corroboration)
- Severity (if applicable)

Scores are computed in `kai11/core/reportability.py` and attached to each finding.
