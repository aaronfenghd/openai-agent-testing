# Oncology CEA Model Structures

Common model types:
- Partitioned survival model (PSM)
- State-transition (Markov) model
- Decision tree with long-term extrapolation module

When to use:
- PSM: oncology settings with robust OS/PFS evidence and straightforward progression pathways.
- Markov: when transitions, treatment lines, or history-dependent states need explicit modeling.
- Decision tree + extrapolation: short-term treatment decisions with downstream long-term effects.

Key trade-offs:
- PSM is transparent for OS/PFS alignment but less explicit on transitions.
- Markov offers flexibility but needs more transition assumptions.
- Decision-tree hybrids can be practical but risk oversimplifying long-term disease dynamics.

Questions for the user:
- Is the objective HTA submission, internal decision support, or publication?
- How many treatment lines and post-progression pathways are needed?
- Is mature OS/PFS data available for a PSM framework?
- Are explicit transitions required for policy-relevant decisions?
