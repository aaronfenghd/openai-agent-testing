from pydantic import BaseModel, Field


class ModelAssumption(BaseModel):
    assumption_area: str = Field(..., description="Area of the model this assumption applies to.")
    assumption: str = Field(..., description="The assumption statement.")
    rationale: str = Field(..., description="Why this assumption is used.")
    status: str = Field(..., description="Status such as confirmed or to be confirmed.")


class ParameterRequirement(BaseModel):
    category: str = Field(..., description="Parameter category (clinical, cost, utility, etc.).")
    parameter: str = Field(..., description="Parameter name.")
    description: str = Field(..., description="How the parameter is used in the model.")
    preferred_source: str = Field(..., description="Preferred evidence source.")
    status: str = Field(..., description="Availability status such as available or to be confirmed.")


class ScenarioAnalysis(BaseModel):
    scenario_name: str = Field(..., description="Short scenario title.")
    description: str = Field(..., description="What changes versus base case.")
    rationale: str = Field(..., description="Why this scenario matters.")


class ValidationCheck(BaseModel):
    check_name: str = Field(..., description="Validation check name.")
    description: str = Field(..., description="How the validation check is performed.")
    importance: str = Field(..., description="Why this check is important.")


class ModelDevelopmentPlan(BaseModel):
    project_title: str
    indication: str
    target_population: str
    intervention: str
    comparator: str
    country_setting: str
    perspective: str
    model_type: str
    model_structure_summary: str
    health_states: list[str]
    time_horizon: str
    cycle_length: str
    discounting: str
    core_assumptions: list[ModelAssumption]
    required_parameters: list[ParameterRequirement]
    data_gaps: list[str]
    base_case_analysis: str
    scenario_analyses: list[ScenarioAnalysis]
    sensitivity_analyses: list[str]
    validation_checks: list[ValidationCheck]
    expected_deliverables: list[str]
    open_questions_for_user: list[str]
