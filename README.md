# openai-agent-testing

A first AI agent app built with the OpenAI Agents SDK and GitHub Codespaces.

## What it does

This repo now contains:
- a simple repo assistant in `agent/`
- an interactive **HE MDP Agent** workflow in `HE MDP agent/` for oncology CEA model planning
- a Streamlit chatbot UI for the HE MDP workflow, supporting pasted reference text or one uploaded PDF

## Run

### Install dependencies

```bash
pip install streamlit pypdf
```

### Repo assistant

```bash
python agent/main.py
```

### Interactive HE MDP agent (terminal)

```bash
python "./HE MDP agent/main.py"
```

### HE MDP chatbot (Streamlit)

```bash
streamlit run "HE MDP agent/app.py"
```

## Streamlit workflow

1. Open chatbot.
2. Choose one reference option:
   - paste reference text
   - upload one PDF
   - skip references
3. Describe the CEA model you want to build.
4. Answer follow-up questions.
5. Type `generate MDP` (or `create MDP` / `final MDP`) to create the final plan.

Notes:
- PDF upload is supported for text-based PDFs only.
- OCR/scanned PDFs are not supported yet.
- Only one PDF is supported for now.
- For this MVP, extraction uses up to ~50 pages or ~8,000 words from uploaded PDFs.
- Pasted reference text remains supported, ideally under ~5,000 words.
- The HE MDP tools use `Runner.run(...)` / `Runner.run_sync(...)`, so set `OPENAI_API_KEY` in your environment before running.

## Curated HE Knowledge Base

The HE MDP Agent includes a small curated health economics knowledge base under:

`HE MDP agent/knowledge_base/`

These markdown files provide general modeling guidance on:
- oncology model structures
- partitioned survival models
- model assumptions
- survival extrapolation
- costs and utilities
- scenario/sensitivity analysis
- validation checks
- common ERG/EAG critiques

The app uses lightweight keyword retrieval (`HE MDP agent/knowledge_retriever.py`) to pass
relevant snippets into the interview agent and final MDP generator prompts.

The curated knowledge base is general methodological guidance only. It does not replace
project-specific evidence, uploaded references, or user-provided information.

To update the knowledge base, edit or add markdown files in `HE MDP agent/knowledge_base/`.
