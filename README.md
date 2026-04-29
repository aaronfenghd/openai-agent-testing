# openai-agent-testing

A first AI agent app built with the OpenAI Agents SDK and GitHub Codespaces.

## What it does

This repo now contains:
- a simple repo assistant in `agent/`
- an interactive **HE MDP Agent** workflow in `HE MDP agent/` for oncology CEA model planning

The HE MDP workflow supports:
- iterative interview-style input gathering
- final structured model development plan generation on command
- markdown rendering of the generated plan

## Run

### Repo assistant

```bash
python agent/main.py
```

### Interactive HE MDP agent

```bash
python "./HE MDP agent/main.py"
```

You will see:
- `HE MDP Agent`
- guidance to describe your CEA modeling need
- command hints:
  - `generate MDP` / `create MDP` / `final MDP` to generate the final structured plan
  - `exit` / `quit` to end the session

The script uses `Runner.run(...)` for both:
- interview turns (`he_mdp_interview_agent`)
- final structured plan generation (`he_mdp_agent`)

So you must set `OPENAI_API_KEY` before running.
