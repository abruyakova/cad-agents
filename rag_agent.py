import time

from langchain.agents import create_agent
from langchain_core.tools import tool
from langchain_ollama import ChatOllama

from cli import run_dialog
from prompts import load_system_prompt
from rag_chain import MODEL, CHAT_OPTIONS
from vector_store import build_vector_store


def rag_chain(on_retrieval=None):
    vector_store = build_vector_store()

    @tool(response_format="content_and_artifact")
    def retrieve_context(query: str):
        """Retrieve CAD drawing rules, company defaults (e.g. default plate sizes,
        flange dimensions, bolt circle rules, solid thicknesses, spacer lengths)
        and fastener clearance tables from the knowledge base. ALWAYS call this
        tool when any dimension or fastener size is unspecified, to look up company
        defaults before asking questions or producing a drawing.
        Args:
            query: The query to retrieve information for
        """
        started = time.perf_counter()
        retrieved_docs = vector_store.similarity_search(query, k=4)
        if on_retrieval:
            on_retrieval(time.perf_counter() - started)
        serialized = "\n\n".join(
            (f"Source: {doc.metadata}\nContent: {doc.page_content}")
            for doc in retrieved_docs
        )
        return serialized, retrieved_docs

    agent_prompt = (
        load_system_prompt()
        + "\n\nTOOL USE INSTRUCTION: You have access to the tool 'retrieve_context'. "
        "Whenever any dimension or fastener size is not explicitly specified in the instruction, "
        "you MUST call 'retrieve_context' to look up the company design rules and defaults "
        "before asking clarification questions or outputting JSON."
    )

    return create_agent(model=ChatOllama(model=MODEL, **CHAT_OPTIONS),
                        tools=[retrieve_context],
                        system_prompt=agent_prompt)


if __name__ == "__main__":
    run_dialog(rag_chain())