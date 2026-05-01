# Survival Extrapolation in Oncology CEA

## Purpose
Survival extrapolation projects outcomes beyond observed follow-up and is often a major driver of incremental QALYs and cost-effectiveness.

## Core considerations
- OS, PFS, and TTD relationships should be coherent.
- Independent versus dependent curve fitting should be selected based on evidence and plausibility.
- PH-based modeling versus independently fitted curves requires justification.

## Candidate approaches
- Standard parametric models (e.g., common monotonic distributions).
- Flexible spline models where hazard shapes are complex.
- Cure or mixture-cure models when clinically plausible.

AIC/BIC may be supportive for fit comparison but are not sufficient alone for selection.

## Treatment waning and long-term constraints
- Waning assumptions may be appropriate when durability is uncertain.
- General population mortality constraints should be considered when long-term tails risk implausible survival.
- Long-term tails should be clinically reviewed and not justified by statistical fit alone.

## Validation and plausibility
- External validation using long-term evidence or registries may be appropriate when available.
- Clinical expert validation should be planned for long-term hazard behavior.
- Internal consistency between OS/PFS/TTD should be checked.

## Scenario analysis planning
- Alternative parametric families.
- PH versus non-PH assumptions.
- Waning timing/intensity alternatives.
- Cure versus non-cure structures where relevant.

## Common HTA / ERG / EAG concerns
- Immature survival data extrapolated too far.
- Over-reliance on favorable statistical fit without clinical plausibility.
- Insufficient exploration of structural survival uncertainty.

## Questions the HE MDP Agent should ask
- What is data maturity for OS and PFS?
- Are PH assumptions clinically plausible?
- Is treatment waning required?
- What external anchors are available for long-term validation?
- Which extrapolation scenarios should be mandatory in the plan?

## MDP implications
The MDP should pre-specify extrapolation candidates, validation checks, and scenario sets before final model implementation.

## Example wording
"Survival extrapolation approach is to be confirmed based on fit diagnostics and clinical plausibility. Parametric, spline, and waning scenarios should be assessed where uncertainty is material, with external validation considered if suitable data are available."
