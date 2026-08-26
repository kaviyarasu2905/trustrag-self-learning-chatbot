"""
TrustRAG - Retriever Agent Module
"""

from .retriever_agent import (
    initialize_chroma_db,
    populate_knowledge_base,
    retrieve_documents,
    SAMPLE_KNOWLEDGE_BASE,
)

__all__ = [
    "initialize_chroma_db",
    "populate_knowledge_base",
    "retrieve_documents",
    "SAMPLE_KNOWLEDGE_BASE",
]
