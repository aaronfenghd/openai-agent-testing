from pathlib import Path
from agents import function_tool

REPO_ROOT = Path(__file__).resolve().parents[1]

@function_tool
def list_repo_contents() -> str:
    """List the top-level files and folders in the repository."""
    items = []
    for path in sorted(REPO_ROOT.iterdir()):
        items.append(path.name + ("/" if path.is_dir() else ""))
    return "Top-level repository contents:\n" + "\n".join(items)

@function_tool
def suggest_plan(goal: str) -> str:
    """Suggest a short plan for the user's goal."""
    return (
        f"Goal: {goal}\n\n"
        "Plan:\n"
        "1. Inspect the repository\n"
        "2. Identify the smallest useful next change\n"
        "3. Implement it safely\n"
        "4. Test it\n"
        "5. Summarize what changed"
    )