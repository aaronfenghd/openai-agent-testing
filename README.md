# openai-agent-testing

A first AI agent app built with the OpenAI Agents SDK and GitHub Codespaces.

## What it does

This repo now contains:
- a simple repo assistant in `agent/`
- an interactive **HE MDP Agent** workflow in `HE MDP agent/` for oncology CEA model planning
- a Streamlit chatbot UI for the HE MDP workflow, including optional pasted reference text extraction

## Run

### Repo assistant

```bash
python agent/main.py
```

### Interactive HE MDP agent (terminal)

```bash
python "./HE MDP agent/main.py"
```

### HE MDP chatbot (Streamlit)

Run:

```bash
streamlit run "HE MDP agent/app.py"
```

## Streamlit workflow

1. Open the chatbot.
2. Paste reference text (or type `skip`).
3. Describe the CEA model you want to build.
4. Answer follow-up questions.
5. Type `generate MDP` (or `create MDP` / `final MDP`) to create the final plan.

Notes:
- Pasted reference text is supported.
- Ideal pasted reference length is under approximately 5,000 words.
- PDF upload and URL retrieval are not yet supported.
- The HE MDP tools use `Runner.run(...)` / `Runner.run_sync(...)`, so set `OPENAI_API_KEY` in your environment before running.
