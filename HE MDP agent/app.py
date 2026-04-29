import os

import streamlit as st
from agents import Runner

from oncology_model_plan_agent import he_mdp_agent, he_mdp_interview_agent
from render import render_plan_as_markdown


GENERATE_COMMANDS = {"generate mdp", "create mdp", "final mdp"}
WELCOME_MESSAGE = (
    "Tell me what cost-effectiveness model you want to build. "
    "I’ll ask follow-up questions and help you create the HE Model Development Plan."
)


def build_context(messages: list[dict[str, str]]) -> str:
    lines: list[str] = []
    for message in messages:
        lines.append(f"{message['role'].upper()}: {message['content']}")
    return "\n\n".join(lines)


def initialize_state() -> None:
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": WELCOME_MESSAGE}]
    if "final_mdp_markdown" not in st.session_state:
        st.session_state.final_mdp_markdown = None


def clear_state() -> None:
    st.session_state.messages = [{"role": "assistant", "content": WELCOME_MESSAGE}]
    st.session_state.final_mdp_markdown = None


def main() -> None:
    st.set_page_config(page_title="HE MDP Agent", page_icon="💬", layout="centered")

    with st.sidebar:
        st.title("HE MDP Agent")
        st.markdown(
            "Use this chatbot to define your oncology CEA model plan. "
            "Type details naturally, then type **generate MDP** (or **create MDP** / **final MDP**) "
            "to produce the final markdown plan."
        )
        if st.button("Clear conversation"):
            clear_state()
            st.rerun()

    initialize_state()

    if not os.getenv("OPENAI_API_KEY"):
        st.warning("OPENAI_API_KEY is not set. Set it in your environment before chatting.")

    st.title("HE MDP Agent Chat")

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    user_input = st.chat_input("Type your message...")
    if not user_input:
        return

    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    normalized = user_input.strip().lower()
    context = build_context(st.session_state.messages)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            if normalized in GENERATE_COMMANDS:
                final_prompt = (
                    "Create the final Health Economic Model Development Plan using the conversation "
                    "below. Mark missing information as 'to be confirmed'.\n\n"
                    f"{context}"
                )
                result = Runner.run_sync(he_mdp_agent, final_prompt)
                plan = result.final_output
                final_report = render_plan_as_markdown(plan)
                st.markdown(final_report)
                st.session_state.messages.append({"role": "assistant", "content": final_report})
                st.session_state.final_mdp_markdown = final_report
            else:
                interview_prompt = (
                    "Continue the HE MDP interview using the conversation below. Ask concise targeted "
                    "follow-up questions. Do not generate the final MDP yet. Ask no more than 5 "
                    f"questions at once.\n\n{context}"
                )
                result = Runner.run_sync(he_mdp_interview_agent, interview_prompt)
                reply = str(result.final_output)
                st.markdown(reply)
                st.session_state.messages.append({"role": "assistant", "content": reply})


if __name__ == "__main__":
    main()
