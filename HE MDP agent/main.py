import asyncio

from agents import Runner

from oncology_model_plan_agent import he_mdp_agent
from render import render_plan_as_markdown


USER_REQUEST = (
    "Create a model development plan for a cost-effectiveness analysis of Drug A versus "
    "docetaxel in second-line metastatic non-small cell lung cancer from a US payer perspective. "
    "The plan should specify model structure, assumptions, parameters required, data gaps, "
    "sensitivity analyses, scenario analyses, and validation checks."
)


async def main() -> None:
    result = await Runner.run(he_mdp_agent, USER_REQUEST)
    plan = result.final_output
    report = render_plan_as_markdown(plan)
    print(report)


if __name__ == "__main__":
    asyncio.run(main())
