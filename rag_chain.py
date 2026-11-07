import time
from langchain.agents import create_agent
from langchain.agents.middleware import dynamic_prompt
from langchain_ollama import ChatOllama

from cli import run_dialog
from main import MODEL, CHAT_OPTIONS
from prompts import build_system_prompt
from vector_store import build_vector_store



def build_agent(on_retrieval=None):
    vector_store = build_vector_store()

    @dynamic_prompt
    def prompt_with_context(request):
        user_text = "\n".join(
            m.text for m in request.state["messages"] if m.type == "human"
        )
        started = time.perf_counter()
        retrieved_docs = vector_store.similarity_search(user_text)
        if on_retrieval:
            on_retrieval(time.perf_counter() - started)
        docs_content = "\n\n".join(doc.page_content for doc in retrieved_docs)
        return build_system_prompt(docs_content)

    return create_agent(model=ChatOllama(model=MODEL, **CHAT_OPTIONS),
                        middleware=[prompt_with_context])


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    run_dialog(build_agent())
