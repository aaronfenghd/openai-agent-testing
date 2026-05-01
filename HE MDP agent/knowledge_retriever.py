from pathlib import Path
import re

KNOWLEDGE_DIR = Path(__file__).parent / "knowledge_base"


def normalize_terms(text: str) -> set[str]:
    words = re.findall(r"[a-zA-Z][a-zA-Z0-9_-]+", text.lower())
    stopwords = {
        "the", "and", "for", "with", "from", "that", "this", "are", "was",
        "were", "have", "has", "had", "will", "would", "could", "should",
        "about", "into", "using", "used", "model", "models", "analysis",
        "health", "economic", "cost", "effectiveness",
    }
    return {w for w in words if w not in stopwords and len(w) > 2}


def load_knowledge_files() -> dict[str, str]:
    if not KNOWLEDGE_DIR.exists():
        return {}

    knowledge: dict[str, str] = {}
    for path in sorted(KNOWLEDGE_DIR.glob("*.md")):
        try:
            knowledge[path.name] = path.read_text(encoding="utf-8")
        except OSError:
            continue
    return knowledge


def retrieve_knowledge(query: str, max_files: int = 4) -> str:
    knowledge = load_knowledge_files()
    if not knowledge:
        return ""

    query_terms = normalize_terms(query)
    if not query_terms:
        return ""

    scored = []
    query_lower = query.lower()
    phrases = [
        "partitioned survival", "treatment waning", "cure", "proportional hazards",
        "survival extrapolation", "utility", "cost", "erg", "eag", "validation",
        "scenario", "sensitivity",
    ]

    for file_name, content in knowledge.items():
        file_terms = normalize_terms(file_name.replace("_", " ") + " " + content)
        score = len(query_terms.intersection(file_terms))
        content_lower = content.lower()
        for phrase in phrases:
            if phrase in query_lower and phrase in content_lower:
                score += 3
        if score > 0:
            scored.append((score, file_name, content))

    scored.sort(key=lambda x: x[0], reverse=True)
    selected = [f"## Curated knowledge source: {name}\n\n{content}" for _, name, content in scored[:max_files]]
    return "\n\n---\n\n".join(selected)
