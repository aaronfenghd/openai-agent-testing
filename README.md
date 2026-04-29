# openai-agent-testing

A first AI agent app built with the OpenAI Agents SDK and GitHub Codespaces.

## What it does

This repo now contains:
- a simple repo assistant in `agent/`
- an interactive **HE MDP Agent** workflow in `HE MDP agent/` for oncology CEA model planning
- a simple Streamlit chatbot UI for the HE MDP workflow

The HE MDP workflow supports:
- iterative interview-style input gathering
- final structured model development plan generation on command
- markdown rendering of the generated plan

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

Install Streamlit if needed:

```bash
pip install streamlit
```

Run the chatbot app:

```bash
streamlit run "HE MDP agent/app.py"
```

In the chat UI:
- describe your CEA model
- answer follow-up interview questions
- type `generate MDP` (or `create MDP` / `final MDP`) to generate the final markdown model development plan

The HE MDP tools use `Runner.run(...)` / `Runner.run_sync(...)`, so set `OPENAI_API_KEY` in your environment before running.
