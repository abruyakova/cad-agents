# This is a sample Python script.
from langchain_core.callbacks import get_usage_metadata_callback
# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
from ollama import chat
import time
from pathlib import Path
from langchain_chroma import Chroma
from langchain.agents import create_agent
from langchain.agents.middleware import dynamic_prompt
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from metrics import record_metrics, start_metrics_server
from prompts import build_system_prompt

DATA_DIR = Path(__file__).parent / "data"
CHROMA_DIR = Path(__file__).parent / "chroma_langchain_db"

# qwen3-embedding
EMBEDDING_MODEL = "qwen3-embedding"
MODEL = 'qwen3:4b-instruct'


def build_vector_store():
    embeddings = OllamaEmbeddings(model=EMBEDDING_MODEL)
    return Chroma(
        collection_name="example_collection",
        embedding_function=embeddings,
        persist_directory= CHROMA_DIR,
    )

def load_data(path=DATA_DIR):
    documents = [
        Document(page_content=f.read_text(encoding="utf-8"), metadata={"source": str(f)})
        for f in sorted(Path(path).glob("**/*.md"))
    ]
    print(f"Total characters: {len(documents[0].page_content)}")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        add_start_index=True,
    )
    all_splits = text_splitter.split_documents(documents)
    print(f"Split blog post into {len(all_splits)} sub-documents.")

    vector_store = build_vector_store();
    vector_store.add_documents(all_splits)

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

    return create_agent(model=ChatOllama(model=MODEL),
                        middleware=[prompt_with_context])


def agentDialog(agent):

    start_metrics_server(model=MODEL)
    print("Enter a drawing instruction (empty line or 'exit' to quit).")
    messages = []
    while True:
        try:
            user_content = input("\n> ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if not user_content or user_content.lower() in ("exit", "quit"):
            break

        messages.append({"role": "user", "content": user_content})

        with get_usage_metadata_callback() as cb:
            started = time.perf_counter()
            result = agent.invoke({"messages": messages})
            seconds = time.perf_counter() - started

            for model_name, usage in cb.usage_metadata.items():
                print(f"Model: {model_name}")
                print(f"Total Tokens: {usage['total_tokens']}")
                print(f"Prompt Tokens: {usage['input_tokens']}")
                print(f"Completion Tokens: {usage['output_tokens']}")

        messages = result["messages"]
        final_message = messages[-1]
        print(final_message.content)

        is_question = final_message.text.lstrip().startswith("QUESTION:")
        record_metrics(final_message, cb.usage_metadata, seconds,
                       "question" if is_question else "json")

        # Keep the conversation while the agent is asking questions;
        # start a new one once it returns the final JSON.
        if not is_question:
            messages = []


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
   #load_data()
    agentDialog(build_agent())
