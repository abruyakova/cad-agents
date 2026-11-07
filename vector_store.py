from pathlib import Path

from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_ollama import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

EMBEDDING_MODEL = "qwen3-embedding"
CHROMA_DIR = Path(__file__).parent / "chroma_langchain_db"
DATA_DIR = Path(__file__).parent / "data"

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