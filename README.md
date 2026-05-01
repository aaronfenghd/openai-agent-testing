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
