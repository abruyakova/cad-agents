from langchain.agents import create_agent
from langchain_ollama import ChatOllama

from cli import run_dialog
from main import MODEL, CHAT_OPTIONS
from prompts import load_system_prompt


def build_agent(on_retrieval=None):
    """Build a pure prompt agent with no RAG retrieval and no external tools."""
    return create_agent(
        model=ChatOllama(model=MODEL, **CHAT_OPTIONS),
        system_prompt=load_system_prompt(),
    )


if __name__ == "__main__":
    run_dialog(build_agent())
