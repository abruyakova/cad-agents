from pathlib import Path

SYSTEM_PROMPT_FILE = Path(__file__).parent / "data" / "system_promt.txt"


def load_system_prompt() -> str:
    return SYSTEM_PROMPT_FILE.read_text(encoding="utf-8").strip()


def build_system_prompt(context: str) -> str:
    return f"{load_system_prompt()}\n\nKnowledge base context\n{context}"
