# Validation Checks for Oncology HE Models

## Purpose
Validation assesses whether model structure, implementation, and outputs are credible for decision use.

## Validation domains
- Face validity (clinical and methodological plausibility)
- Internal validity (logic and arithmetic consistency)
- External validity (alignment with external evidence where available)
- Technical validation (implementation correctness)

## Practical checks
- Health-state occupancy sums to 1 each cycle.
- No negative health-state occupancy.
- OS/PFS relationships remain coherent.
- Survival tail behavior is clinically plausible.
- Cost and QALY outputs are directionally plausible.
- Discounting is applied correctly.
- Half-cycle correction is handled appropriately if relevant to structure.
- Inputs and assumptions are traceable to source/rationale.

## Additional checks
- Cross-validation against published models or prior submissions may be considered when comparable contexts exist.
- Review logs should capture model changes and rationale.

## Common HTA / ERG / EAG concerns
- Incomplete validation evidence.
- Inconsistent survival logic or implausible long-term outcomes.
- Weak traceability between assumptions, inputs, and outputs.

## Questions the HE MDP Agent should ask
- What validation standards are expected by the end user?
- Which checks are required before base-case sign-off?
- Is external benchmarking feasible?
- How will assumption and parameter traceability be maintained?

## MDP implications
Validation should be a defined workstream in the MDP with responsibilities, timing, and acceptance criteria.

## Example wording
"Validation will include face, internal, external, and technical checks, including occupancy consistency, survival plausibility, cost/QALY reasonableness, and discounting verification. A traceability log will document assumptions, sources, and model revisions."
