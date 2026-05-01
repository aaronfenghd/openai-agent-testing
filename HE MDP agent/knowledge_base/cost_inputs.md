# Cost Inputs for Oncology CEA

## Purpose
Cost inputs should reflect the decision perspective and relevant resource use across the treatment pathway.

## Typical cost components
- Drug acquisition costs
- Dosing assumptions and relative dose intensity
- Wastage assumptions
- Administration costs
- Monitoring and routine follow-up
- Disease management by health state
- Adverse event management
- Subsequent treatment costs
- Terminal/end-of-life care
- Testing or biomarker costs where relevant

## Relevance and limitations
A broad cost framework may be appropriate when pathway complexity is high. Simpler cost frameworks may be appropriate only when omissions are unlikely to affect decisions.

## Typical implementation in oncology CEA
- Align inclusion rules to perspective (e.g., payer-relevant categories).
- Define price year/currency year and inflation handling.
- Document source hierarchy and fallback assumptions where evidence is limited.

## Source hierarchy and perspective
- Preferred sources may include jurisdiction-relevant price/tariff sources and validated literature.
- Inclusion of categories should be perspective-specific and justified.

## Common HTA / ERG / EAG concerns
- Omitted cost categories with likely material impact.
- Unclear dosing or wastage assumptions.
- Weak justification for subsequent therapy and terminal-care costs.
- Inconsistent price-year handling.

## Questions the HE MDP Agent should ask
- What perspective and price year should be used?
- Are confidential discounts or local contracting effects relevant?
- Which costs are evidence-based versus assumption-based?
- How are dosing, wastage, and treatment duration represented?

## MDP implications
The MDP should include a parameter map by category, preferred sources, uncertainty flags, and scenario plans for high-impact cost assumptions.

## Example wording
"Cost inputs will include acquisition, administration, monitoring, disease management, adverse events, subsequent therapy, and terminal care in line with the selected perspective. Source hierarchy, price-year conventions, and key assumptions (dose intensity, wastage, duration) will be explicitly documented and stress-tested where uncertain."
