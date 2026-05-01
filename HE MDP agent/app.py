import os

import streamlit as st
from agents import Runner

from oncology_model_plan_agent import (
    he_mdp_agent,
    he_mdp_interview_agent,
    reference_extraction_agent,
)
from render import render_plan_as_markdown
from schemas import ReferenceExtraction


GENERATE_COMMANDS = {"generate mdp", "create mdp", "final mdp"}
REFERENCE_PROMPT = (
    "Do you have any reference text to guide this HE Model Development Plan? For example, HTA "
    "appraisal text, ERG/EAG comments, CEA publication excerpts, or model description sections. "
    "Please paste the most relevant excerpts, ideally under 5,000 words, such as model structure, "
    "assumptions, survival extrapolation, utilities, costs, scenario analyses, or ERG/EAG comments. "
    "Type 'skip' to continue without references."
)


def build_context(messages: list[dict[str, str]]) -> str:
    return "\n\n".join([f"{m['role'].upper()}: {m['content']}" for m in messages])


def build_reference_context(reference_extraction: ReferenceExtraction | None) -> str:
    if not reference_extraction:
        return "No reference extraction available."

    return "\n".join(
        [
            "REFERENCE EXTRACTION CONTEXT:",
            f"- Reference type: {reference_extraction.reference_type}",
            f"- Indication: {reference_extraction.indication}",
            f"- Intervention: {reference_extraction.intervention}",
            f"- Comparator: {reference_extraction.comparator}",
            f"- Model structure used: {reference_extraction.model_structure_used}",
            f"- Model structure rationale: {reference_extraction.model_structure_rationale}",
            f"- Health states: {', '.join(reference_extraction.health_states)}",
            f"- Model assumptions: {', '.join(reference_extraction.model_assumptions)}",
            f"- Time horizon: {reference_extraction.time_horizon}",
            f"- Cycle length: {reference_extraction.cycle_length}",
            f"- Perspective: {reference_extraction.perspective}",
            f"- Discounting: {reference_extraction.discounting}",
            f"- Survival extrapolation approach: {reference_extraction.survival_extrapolation_approach}",
            f"- Utility assumptions: {', '.join(reference_extraction.utility_assumptions)}",
            f"- Cost categories: {', '.join(reference_extraction.cost_categories)}",
            "- Scenario/sensitivity analyses: "
            + ", ".join(reference_extraction.scenario_sensitivity_analyses),
            f"- Key ERG/EAG opinions: {', '.join(reference_extraction.key_erg_opinions)}",
            f"- Information gaps: {', '.join(reference_extraction.information_gaps)}",
            f"- Applicability to current MDP: {reference_extraction.applicability_to_current_mdp}",
        ]
    )


def summarize_reference_extraction(reference_extraction: ReferenceExtraction) -> str:
    assumptions = ", ".join(reference_extraction.model_assumptions[:4]) or "not reported"
    erg = ", ".join(reference_extraction.key_erg_opinions[:3]) or "not reported"
    gaps = ", ".join(reference_extraction.information_gaps[:4]) or "not reported"
    return "\n".join(
        [
            "### Reference extraction summary",
            f"- Reference type: {reference_extraction.reference_type}",
            f"- Indication: {reference_extraction.indication}",
            f"- Model structure used: {reference_extraction.model_structure_used}",
            f"- Key rationale: {reference_extraction.model_structure_rationale}",
            f"- Key assumptions: {assumptions}",
            f"- Key ERG/EAG opinions: {erg}",
            f"- Information gaps: {gaps}",
            f"- Applicability to current MDP: {reference_extraction.applicability_to_current_mdp}",
        ]
    )


def initialize_state() -> None:
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": REFERENCE_PROMPT}]
    if "reference_text" not in st.session_state:
        st.session_state.reference_text = ""
    if "reference_extraction" not in st.session_state:
        st.session_state.reference_extraction = None
    if "reference_step_completed" not in st.session_state:
        st.session_state.reference_step_completed = False
    if "final_mdp" not in st.session_state:
        st.session_state.final_mdp = None


def clear_state() -> None:
    st.session_state.messages = [{"role": "assistant", "content": REFERENCE_PROMPT}]
    st.session_state.reference_text = ""
    st.session_state.reference_extraction = None
    st.session_state.reference_step_completed = False
    st.session_state.final_mdp = None


def main() -> None:
    st.set_page_config(page_title="HE MDP Agent", page_icon="💬", layout="centered")
    initialize_state()

    with st.sidebar:
        st.title("HE MDP Agent")
        st.markdown(
            "Paste reference excerpts (optional, ideally <5,000 words), then continue interview "
            "chat and type **generate MDP** when ready."
        )
        if st.button("Clear conversation"):
            clear_state()
            st.rerun()

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

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            if not st.session_state.reference_step_completed:
                if normalized == "skip":
                    st.session_state.reference_text = ""
                    st.session_state.reference_extraction = None
                    st.session_state.reference_step_completed = True
                    reply = "No reference text added. Tell me what cost-effectiveness model you want to build."
                    st.markdown(reply)
                    st.session_state.messages.append({"role": "assistant", "content": reply})
                    return

                st.session_state.reference_text = user_input
                word_count = len(user_input.split())
                if word_count > 5000:
                    st.warning(
                        "Reference text appears long (>5,000 words). I will attempt extraction, "
                        "but speed and accuracy may be affected."
                    )

                extraction_prompt = (
                    "Extract structured HE model development insights from the pasted reference text "
                    "below. Mark missing or unclear items as 'not reported'.\n\n"
                    f"REFERENCE TEXT:\n{user_input}"
                )
                extraction_result = Runner.run_sync(reference_extraction_agent, extraction_prompt)
                extraction = extraction_result.final_output
                st.session_state.reference_extraction = extraction
                st.session_state.reference_step_completed = True

                summary = summarize_reference_extraction(extraction)
                follow_up = (
                    "Now tell me what cost-effectiveness model you want to build, and I'll use the "
                    "reference information where applicable."
                )
                st.markdown(summary)
                st.markdown(follow_up)
                st.session_state.messages.append({"role": "assistant", "content": summary})
                st.session_state.messages.append({"role": "assistant", "content": follow_up})
                return

            context = build_context(st.session_state.messages)
            reference_context = build_reference_context(st.session_state.reference_extraction)

            if normalized in GENERATE_COMMANDS:
                final_prompt = (
                    "Create the final Health Economic Model Development Plan using BOTH the "
                    "conversation and reference extraction context below. Explicitly explain how "
                    "reference information informed model structure, rationale, assumptions, "
                    "required parameters, scenario/sensitivity analyses, and validation checks. "
                    "Mark missing information as 'to be confirmed'. Do not invent clinical, cost, "
                    "utility, survival, or epidemiological data.\n\n"
                    f"{reference_context}\n\nCONVERSATION:\n{context}"
                )
                result = Runner.run_sync(he_mdp_agent, final_prompt)
                plan = result.final_output
                final_report = render_plan_as_markdown(plan)
                st.markdown(final_report)
                st.session_state.messages.append({"role": "assistant", "content": final_report})
                st.session_state.final_mdp = final_report
                return

            interview_prompt = (
                "Continue the HE MDP interview using the conversation and reference extraction "
                "context below. Ask concise targeted follow-up questions (max 5). Do not generate "
                "the final MDP yet. Do not ask again for information already clearly provided. "
                "Propose preliminary recommendations where reasonable.\n\n"
                f"{reference_context}\n\nCONVERSATION:\n{context}"
            )
            result = Runner.run_sync(he_mdp_interview_agent, interview_prompt)
            reply = str(result.final_output)
            st.markdown(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})


if __name__ == "__main__":
    main()
