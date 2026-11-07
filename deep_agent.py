from deepagents import create_deep_agent
from langchain_ollama import ChatOllama

from cli import run_dialog
from main import MODEL, CHAT_OPTIONS
from vector_store import build_vector_store


def build_agent(on_retrieval=None):
    vector_store = build_vector_store()
    return create_deep_agent(
        model=ChatOllama(model=MODEL, **CHAT_OPTIONS),

    )

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    run_dialog(build_agent())