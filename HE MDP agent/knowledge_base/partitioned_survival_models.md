# Partitioned Survival Models (PSM) in Oncology

## Definition and purpose
A partitioned survival model estimates the proportion of patients in health states over time using survival curves rather than explicit transition probabilities.

## Why commonly used in oncology
PSMs are widely used when OS and PFS are key trial outcomes and the disease pathway can be summarized as progression-free, progressed disease, and death.

## Typical health states and occupancy logic
- Progression-free = PFS(t)
- Death = 1 - OS(t)
- Progressed disease = OS(t) - PFS(t)

This logic requires internally coherent OS and PFS modeling across time.

## Data requirements
- Trial or comparative evidence for OS and PFS.
- Justified extrapolation approach for long-term horizons.
- Inputs for state-based costs and utilities.
- Assumptions for treatment duration, discontinuation, and subsequent therapies.

## Advantages
- Transparent linkage to observed survival endpoints.
- Often understandable to clinical and HTA reviewers.
- Practical when transition-level evidence is limited.

## Limitations
- Post-progression transitions are implicit.
- PFS and OS extrapolation choices can drive results materially.
- Requires careful handling of treatment discontinuation and downstream therapies.

## Relationship between OS and PFS
- OS and PFS should be jointly reviewed for plausibility.
- Extrapolation should avoid implausible long-term divergence.
- Any structural inconsistency requires justification and validation checks.

## Treatment discontinuation and subsequent therapy considerations
- Discontinuation may not coincide with progression and should be explicitly addressed.
- Subsequent therapy effects may materially affect OS and post-progression costs.
- These assumptions should be considered for scenario analysis if uncertain.

## Common HTA / ERG / EAG concerns
- Immature OS and uncertain long-term extrapolation.
- Insufficient justification for treatment effect duration.
- Limited transparency around post-progression assumptions.

## Validation checks
- No negative progressed state occupancy.
- Occupancy proportions sum to 1 at each cycle.
- OS/PFS tail behavior remains clinically plausible.
- Cost/QALY patterns are directionally consistent with clinical expectations.

## Questions the HE MDP Agent should ask
- Are OS and PFS mature enough for base-case extrapolation?
- Is treatment effect waning needed and when?
- How will treatment discontinuation be represented?
- How are subsequent therapies incorporated?
- Which alternative extrapolation scenarios should be pre-specified?

## MDP implications
- The model plan should explicitly document OS/PFS evidence maturity, extrapolation choices, and key uncertainty drivers.
- Validation steps should include occupancy and survival consistency checks.

## Example wording
"The base-case structure may use a 3-state partitioned survival model (progression-free, progressed disease, death) because OS/PFS are available and aligned with the decision question. Extrapolation, treatment waning, and post-progression assumptions require scenario analysis and clinical review before finalization."
