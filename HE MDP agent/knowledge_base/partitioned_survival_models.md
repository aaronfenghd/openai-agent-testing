# Partitioned Survival Models in Oncology

Typical use:
- Common for oncology CEAs with trial-based OS and PFS curves.

Standard health states:
- Progression-free
- Progressed disease
- Death

State occupancy logic:
- Progression-free = PFS(t)
- Death = 1 - OS(t)
- Progressed disease = OS(t) - PFS(t)

Strengths:
- Direct use of observed survival endpoints.
- Often aligns with HTA expectations in oncology.

Limitations:
- Post-progression dynamics are implicit.
- May require assumptions for treatment effect waning and long-term extrapolation.

Common HTA concerns:
- Clinical plausibility of long-term OS/PFS tails.
- Inconsistency between PFS and OS extrapolations.
- Limited maturity of survival data.

Questions to ask:
- Are OS and PFS sufficiently mature?
- Is treatment effect waning needed?
- Should mortality constraints be applied?
- Are post-progression assumptions clinically defensible?
