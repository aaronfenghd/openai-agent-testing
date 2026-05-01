# Oncology Model Structure Selection

## Definition and purpose
Model structure selection defines how clinical pathways, survival, costs, and health outcomes are represented. In an HE model development plan (MDP), structure choice should be aligned to the decision problem, available evidence, and expected HTA scrutiny.

## When each structure may be relevant
### Partitioned survival model (PSM)
May be appropriate when OS and PFS data are central and the decision context can be represented with progression-based states.

### State-transition (Markov) model
May be appropriate when explicit transition dynamics are needed (e.g., multiple post-progression pathways, treatment sequences, or event-history effects).

### Decision tree + long-term extrapolation
May be appropriate when an initial short-term decision phase is distinct, followed by long-term disease evolution.

### Semi-Markov / tunnel-state approaches
May be appropriate when time-since-event matters (e.g., post-progression risk patterns or time-dependent resource use).

### Microsimulation (brief note)
May be appropriate when individual-level heterogeneity or complex treatment pathways are critical and cohort approaches are insufficient.

## When a structure may be less appropriate
- A complex structure may not be appropriate when data are sparse and assumptions would dominate outputs.
- A simple structure may not be appropriate when key clinical dynamics are omitted.
- A structure chosen only for convenience requires justification and sensitivity testing.

## Typical implementation in oncology CEA
- Start with a base structure that aligns with trial endpoints and treatment pathway.
- Map expected costs/utilities to structural elements.
- Identify where structural assumptions are unavoidable and plan scenario analyses.

## Strengths, limitations, and data requirements
- PSM: transparent OS/PFS linkage; limitation is implicit post-progression transitions; requires reliable OS/PFS evidence.
- Markov: explicit transitions; limitation is greater parameter burden; requires transition evidence and validation.
- Hybrid decision-tree models: practical for staged problems; limitation is potential oversimplification of long-term dynamics.
- Semi-Markov/tunnel: captures time dependency; limitation is increased complexity and data needs.
- Microsimulation: flexible heterogeneity; limitation is computational and validation burden.

## Common oncology HTA considerations
- Whether structure reflects disease and treatment pathway plausibly.
- Whether structural complexity is proportionate to evidence.
- Whether alternative plausible structures are considered in scenarios.

## Questions the HE MDP Agent should ask
- What is the decision objective (HTA submission, internal planning, publication)?
- Which clinical endpoints are available and mature?
- Are explicit treatment sequences needed?
- Is time-since-event behavior important for outcomes or costs?
- Which structural alternatives should be tested as scenarios?

## MDP implications
- Structure choice should be documented with rationale and alternatives considered.
- Any major structural uncertainty should be tested in scenario analysis.
- Data requirements should be listed against structural components and flagged as to be confirmed where needed.

## Example wording
"A partitioned survival model may be appropriate for the base case given available OS/PFS evidence and a progression-based pathway. A state-transition alternative should be considered in scenario analysis if post-progression dynamics materially affect outcomes. Final structure selection requires confirmation based on data maturity and clinical validation."
