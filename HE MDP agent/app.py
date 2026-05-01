import os

import streamlit as st
from agents import Runner
from pypdf import PdfReader

from oncology_model_plan_agent import (
    he_mdp_agent,
    he_mdp_interview_agent,
    reference_extraction_agent,
)
from render import render_plan_as_markdown
from schemas import ReferenceExtraction


GENERATE_COMMANDS = {"generate mdp", "create mdp", "final mdp"}
PDF_MAX_PAGES = 50
PDF_MAX_WORDS = 8000
PASTE_SOFT_WORD_LIMIT = 5000


def build_context(messages: list[dict[str, str]]) -> str:
    return "\n\n".join([f"{m['role'].upper()}: {m['content']}" for m in messages])


def extract_text_from_pdf(uploaded_file, max_pages: int = PDF_MAX_PAGES, max_words: int = PDF_MAX_WORDS) -> str:
    try:
        uploaded_file.seek(0)
        reader = PdfReader(uploaded_file)
        chunks: list[str] = []
        word_count = 0

        for i, page in enumerate(reader.pages):
            if i >= max_pages or word_count >= max_words:
                break

            page_text = page.extract_text() or ""
            if not page_text.strip():
                continue

            words = page_text.split()
            remaining_words = max_words - word_count
            clipped = words[:remaining_words]
            if clipped:
                chunks.append(" ".join(clipped))
                word_count += len(clipped)

        return "\n\n".join(chunks).strip()
    except Exception:
        return ""


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
    return "\n".join(
        [
            "### Reference extraction summary",
            f"- Reference type: {reference_extraction.reference_type}",
            f"- Indication: {reference_extraction.indication}",
            f"- Model structure used: {reference_extraction.model_structure_used}",
            f"- Key rationale: {reference_extraction.model_structure_rationale}",
            f"- Key assumptions: {', '.join(reference_extraction.model_assumptions[:4]) or 'not reported'}",
            f"- Key ERG/EAG opinions: {', '.join(reference_extraction.key_erg_opinions[:3]) or 'not reported'}",
            f"- Information gaps: {', '.join(reference_extraction.information_gaps[:4]) or 'not reported'}",
            f"- Applicability to current MDP: {reference_extraction.applicability_to_current_mdp}",
        ]
    )


def initialize_state() -> None:
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "reference_text" not in st.session_state:
        st.session_state.reference_text = ""
    if "reference_file_name" not in st.session_state:
        st.session_state.reference_file_name = ""
    if "reference_extraction" not in st.session_state:
        st.session_state.reference_extraction = None
    if "reference_step_completed" not in st.session_state:
        st.session_state.reference_step_completed = False
    if "final_mdp" not in st.session_state:
        st.session_state.final_mdp = None


def clear_state() -> None:
    st.session_state.messages = []
    st.session_state.reference_text = ""
    st.session_state.reference_file_name = ""
    st.session_state.reference_extraction = None
    st.session_state.reference_step_completed = False
    st.session_state.final_mdp = None


def main() -> None:
    st.set_page_config(page_title="HE MDP Agent", page_icon="💬", layout="centered")
    initialize_state()

    with st.sidebar:
        st.title("HE MDP Agent")
        st.markdown("Choose a reference option, then continue interview chat. Type **generate MDP** when ready.")
        if st.button("Clear conversation"):
            clear_state()
            st.rerun()

    if not os.getenv("OPENAI_API_KEY"):
        st.warning("OPENAI_API_KEY is not set. Set it in your environment before chatting.")

    st.title("HE MDP Agent Chat")

    if not st.session_state.reference_step_completed:
        st.markdown("### Reference input")
        st.markdown(
            "Do you have any reference text to guide this HE Model Development Plan? Paste relevant excerpts "
            "(ideally under ~5,000 words) such as model structure, assumptions, survival extrapolation, "
            "utilities, costs, scenario analyses, and ERG/EAG comments."
        )
        ref_mode = st.radio(
            "How would you like to provide reference information?",
            ["Paste reference text", "Upload PDF", "Skip references"],
        )

        if ref_mode == "Paste reference text":
            pasted = st.text_area("Paste reference text", height=220)
            if st.button("Use pasted reference"):
                if not pasted.strip():
                    st.warning("Please paste text or choose Skip references.")
                else:
                    st.session_state.reference_text = pasted
                    st.session_state.reference_file_name = ""
                    if len(pasted.split()) > PASTE_SOFT_WORD_LIMIT:
                        st.warning(
                            "Reference text appears long (>5,000 words). Extraction will be attempted, "
                            "but speed and accuracy may be affected."
                        )
                    extraction_result = Runner.run_sync(
                        reference_extraction_agent,
                        "Extract structured HE model development insights. Mark missing/unclear as 'not reported'.\n\n"
                        f"REFERENCE TEXT:\n{pasted}",
                    )
                    extraction = extraction_result.final_output
                    st.session_state.reference_extraction = extraction
                    st.session_state.reference_step_completed = True
                    summary = summarize_reference_extraction(extraction)
                    st.session_state.messages.append({"role": "assistant", "content": summary})
                    st.session_state.messages.append(
                        {
                            "role": "assistant",
                            "content": "Now tell me what cost-effectiveness model you want to build, and I'll use the reference information where applicable.",
                        }
                    )
                    st.rerun()

        elif ref_mode == "Upload PDF":
            uploaded_file = st.file_uploader("Upload one PDF reference", type=["pdf"])
            if st.button("Use uploaded PDF"):
                if uploaded_file is None:
                    st.warning("Please upload one PDF or choose Skip references.")
                else:
                    extracted_text = extract_text_from_pdf(uploaded_file, PDF_MAX_PAGES, PDF_MAX_WORDS)
                    if not extracted_text.strip():
                        st.error(
                            "This PDF appears to be scanned or image-based, or no extractable text was found. "
                            "OCR is not supported yet. Please paste the relevant text manually or upload a text-based PDF."
                        )
                    else:
                        st.session_state.reference_text = extracted_text
                        st.session_state.reference_file_name = uploaded_file.name
                        if len(extracted_text.split()) >= PDF_MAX_WORDS:
                            st.warning(
                                "Only the first 50 pages or approximately 8,000 words were extracted for this MVP. "
                                "Please paste a more targeted excerpt if important sections were missed."
                            )
                        extraction_result = Runner.run_sync(
                            reference_extraction_agent,
                            "Extract structured HE model development insights. Mark missing/unclear as 'not reported'.\n\n"
                            f"REFERENCE TEXT FROM PDF ({uploaded_file.name}):\n{extracted_text}",
                        )
                        extraction = extraction_result.final_output
                        st.session_state.reference_extraction = extraction
                        st.session_state.reference_step_completed = True
                        summary = summarize_reference_extraction(extraction)
                        st.session_state.messages.append({"role": "assistant", "content": summary})
                        st.session_state.messages.append(
                            {
                                "role": "assistant",
                                "content": "Now tell me what cost-effectiveness model you want to build, and I'll use the reference information where applicable.",
                            }
                        )
                        st.rerun()
        else:
            if st.button("Continue without references"):
                st.session_state.reference_step_completed = True
                st.session_state.reference_text = ""
                st.session_state.reference_file_name = ""
                st.session_state.reference_extraction = None
                st.session_state.messages.append(
                    {"role": "assistant", "content": "No reference text added. Tell me what cost-effectiveness model you want to build."}
                )
                st.rerun()

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if not st.session_state.reference_step_completed:
        return

    user_input = st.chat_input("Type your message...")
    if not user_input:
        return

    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    context = build_context(st.session_state.messages)
    reference_context = build_reference_context(st.session_state.reference_extraction)
    normalized = user_input.strip().lower()

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            if normalized in GENERATE_COMMANDS:
                result = Runner.run_sync(
                    he_mdp_agent,
                    "Create the final Health Economic Model Development Plan using BOTH conversation and "
                    "reference extraction context. Explain how reference informed structure/rationale, assumptions, "
                    "required parameters, scenarios/sensitivity, and validation checks. Mark missing as 'to be confirmed'. "
                    "Do not invent data.\n\n"
                    f"{reference_context}\n\nCONVERSATION:\n{context}",
                )
                plan = result.final_output
                final_report = render_plan_as_markdown(plan)
                st.markdown(final_report)
                st.session_state.messages.append({"role": "assistant", "content": final_report})
                st.session_state.final_mdp = final_report
            else:
                result = Runner.run_sync(
                    he_mdp_interview_agent,
                    "Continue interview using conversation and reference extraction context. Ask concise targeted "
                    "follow-up questions (max 5), avoid re-asking known information, and do not generate final MDP yet.\n\n"
                    f"{reference_context}\n\nCONVERSATION:\n{context}",
                )
                reply = str(result.final_output)
                st.markdown(reply)
                st.session_state.messages.append({"role": "assistant", "content": reply})


if __name__ == "__main__":
    main()
