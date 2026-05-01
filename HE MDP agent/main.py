import asyncio

from agents import Runner

from oncology_model_plan_agent import he_mdp_agent, he_mdp_interview_agent
from render import render_plan_as_markdown


GENERATE_COMMANDS = {"generate mdp", "create mdp", "final mdp"}
EXIT_COMMANDS = {"exit", "quit"}


def build_context(conversation_history: list[dict[str, str]]) -> str:
    lines: list[str] = []
    for message in conversation_history:
        lines.append(f"{message['role'].upper()}: {message['content']}")
    return "\n\n".join(lines)


async def main() -> None:
    conversation_history: list[dict[str, str]] = []

    print("HE MDP Agent")
    print("Tell me what cost-effectiveness model you want to build.")
    print('Type "generate MDP" when you are ready to create the final plan.')
    print('Type "exit" to quit.')
    print()

    while True:
        user_input = input("You: ").strip()
        if not user_input:
            continue

        normalized = user_input.lower()

        if normalized in EXIT_COMMANDS:
            print("Goodbye.")
            break

        if normalized in GENERATE_COMMANDS:
            context = build_context(conversation_history)
            final_prompt = (
                "Create the final Health Economic Model Development Plan using the conversation "
                "below. Mark missing information as 'to be confirmed'.\n\n"
                f"{context}"
            )
            result = await Runner.run(he_mdp_agent, final_prompt)
            plan = result.final_output
            report = render_plan_as_markdown(plan)
            print()
            print(report)
            print()
            continue

        conversation_history.append({"role": "user", "content": user_input})
        context = build_context(conversation_history)
        interview_prompt = (
            "Continue the HE MDP interview using the conversation below. Ask concise targeted "
            "follow-up questions. Do not generate the final MDP yet. Ask no more than 5 "
            f"questions at once.\n\n{context}"
        )

        result = await Runner.run(he_mdp_interview_agent, interview_prompt)
        agent_reply = str(result.final_output)

        print()
        print(f"Agent: {agent_reply}")
        print()

        conversation_history.append({"role": "assistant", "content": agent_reply})


if __name__ == "__main__":
    asyncio.run(main())
