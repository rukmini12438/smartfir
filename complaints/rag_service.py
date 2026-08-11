import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document

from .bns_data import BNS_SECTIONS

load_dotenv()

embeddings = GoogleGenerativeAIEmbeddings(
    model="gemini-embedding-001",
    google_api_key=os.getenv("GEMINI_API_KEY"),
)

# Module-level cache — vector store sirf EK BAAR banega jab Django
# app start hoga, baar baar rebuild nahi hoga har request pe
_vector_store = None


def _get_vector_store():
    global _vector_store
    if _vector_store is None:
        # Har BNS section ko ek "Document" object mein convert karte hain —
        # LangChain ka standard format text + metadata ke liye
        documents = [
            Document(
                page_content=f"{item['section']} - {item['title']}: {item['text']}",
                metadata={"section": item["section"], "title": item["title"]},
            )
            for item in BNS_SECTIONS
        ]
        # FAISS.from_documents automatically har document ko embed karta hai
        # (text -> number vectors) aur ek searchable index bana deta hai
        _vector_store = FAISS.from_documents(documents, embeddings)
    return _vector_store


def retrieve_relevant_sections(query, k=4):
    """
    Query (complaint description) leke, sabse RELEVANT BNS sections
    dhundta hai — semantic similarity ke basis par (keyword match nahi,
    balki MEANING match, isliye "chori" aur "theft" dono match kar
    sakte hain even though spelling alag hai).

    Return karta hai top-k sections ka combined text — jo hum AI
    ko context ke roop mein denge.
    """
    store = _get_vector_store()
    results = store.similarity_search(query, k=k)
    return "\n\n".join([doc.page_content for doc in results])