from schemas import ModelDevelopmentPlan


def render_plan_as_markdown(plan: ModelDevelopmentPlan) -> str:
    lines: list[str] = []
    lines.append(f"# {plan.project_title}")
    lines.append("")
    lines.append("## 1. Project Overview")
    lines.append(f"- **Indication:** {plan.indication}")
    lines.append(f"- **Target Population:** {plan.target_population}")
    lines.append(f"- **Intervention:** {plan.intervention}")
    lines.append(f"- **Comparator:** {plan.comparator}")
    lines.append(f"- **Country/Setting:** {plan.country_setting}")
    lines.append(f"- **Perspective:** {plan.perspective}")
    lines.append("")

    lines.append("## 2. Model Structure")
    lines.append(f"- **Recommended Model Type:** {plan.model_type}")
    lines.append(f"- **Structure Summary:** {plan.model_structure_summary}")
    lines.append("- **Health States:**")
    lines.extend([f"  - {state}" for state in plan.health_states])
    lines.append(f"- **Time Horizon:** {plan.time_horizon}")
    lines.append(f"- **Cycle Length:** {plan.cycle_length}")
    lines.append(f"- **Discounting:** {plan.discounting}")
    lines.append("")

    lines.append("## 3. Core Assumptions")
    for item in plan.core_assumptions:
        lines.append(f"- **{item.assumption_area}**")
        lines.append(f"  - Assumption: {item.assumption}")
        lines.append(f"  - Rationale: {item.rationale}")
        lines.append(f"  - Status: {item.status}")
    lines.append("")

    lines.append("## 4. Required Parameters")
    for param in plan.required_parameters:
        lines.append(f"- **{param.parameter}** ({param.category})")
        lines.append(f"  - Description: {param.description}")
        lines.append(f"  - Preferred Source: {param.preferred_source}")
        lines.append(f"  - Status: {param.status}")
    lines.append("")

    lines.append("## 5. Data Gaps")
    lines.extend([f"- {gap}" for gap in plan.data_gaps])
    lines.append("")

    lines.append("## 6. Base-Case Analysis")
    lines.append(plan.base_case_analysis)
    lines.append("")

    lines.append("## 7. Scenario Analyses")
    for scenario in plan.scenario_analyses:
        lines.append(f"- **{scenario.scenario_name}**")
        lines.append(f"  - Description: {scenario.description}")
        lines.append(f"  - Rationale: {scenario.rationale}")
    lines.append("")

    lines.append("## 8. Sensitivity Analyses")
    lines.extend([f"- {item}" for item in plan.sensitivity_analyses])
    lines.append("")

    lines.append("## 9. Validation Checks")
    for check in plan.validation_checks:
        lines.append(f"- **{check.check_name}**")
        lines.append(f"  - Description: {check.description}")
        lines.append(f"  - Importance: {check.importance}")
    lines.append("")

    lines.append("## 10. Expected Deliverables")
    lines.extend([f"- {item}" for item in plan.expected_deliverables])
    lines.append("")

    lines.append("## 11. Open Questions")
    lines.extend([f"- {item}" for item in plan.open_questions_for_user])

    return "\n".join(lines)
