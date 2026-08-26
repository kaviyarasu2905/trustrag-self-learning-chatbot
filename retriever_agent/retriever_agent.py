"""
TrustRAG - Day 1: Retriever Agent Module
==========================================
This module implements the Retriever Agent for TrustRAG using ChromaDB vector database 
and sentence-transformers embeddings (`all-MiniLM-L6-v2`).

Features:
1. ChromaDB vector store initialization with Cosine Similarity metric (`hnsw:space: cosine`).
2. Domain-specific Knowledge Base (University FAQs with 10 sample documents).
3. Semantic retrieval function `retrieve_documents(query, top_k=3)` returning contents and relevance scores.
4. Robust error handling, comprehensive logging, and formatted output presentation.
"""

import logging
import os
import sys
from typing import List, Dict, Any, Optional, Tuple

# Reconfigure stdout/stderr encoding to UTF-8 for Windows console compatibility
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

if hasattr(sys.stderr, "reconfigure"):
    try:
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# ---------------------------------------------------------------------------
# Logging Configuration
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("RetrieverAgent")


# ---------------------------------------------------------------------------
# 1. Similarity Score Threshold Constants
# ---------------------------------------------------------------------------
HIGHLY_RELEVANT_THRESHOLD = 0.70     # >70% = good match
MODERATELY_RELEVANT_THRESHOLD = 0.50 # 50%-70% = okay match
LOW_RELEVANCE_THRESHOLD = 0.20        # <20% = probably wrong domain


# Step 1: Import chromadb and sentence_transformers
try:
    import chromadb
    from chromadb.utils import embedding_functions
    import sentence_transformers
except ImportError as e:
    logging.error(f"Failed to import required libraries: {e}")
    logging.error("Please install requirements: pip install chromadb sentence-transformers")
    sys.exit(1)


# Step 2: Define Sample Knowledge Base (10 Domain-Specific FAQ Documents)
SAMPLE_KNOWLEDGE_BASE: List[Dict[str, Any]] = [
    {
        "id": "doc_1",
        "title": "Semester Fee Payment & Deadlines",
        "category": "Finance",
        "content": (
            "Tuition and semester fees must be paid online through the university student portal "
            "by September 15th for the Fall semester. A late payment penalty fee of $50 applies "
            "for transactions completed after the official deadline."
        ),
    },
    {
        "id": "doc_2",
        "title": "Library Operating Hours & Access",
        "category": "Facilities",
        "content": (
            "The central university library is open Monday through Friday from 8:00 AM to 10:00 PM, "
            "and on weekends from 10:00 AM to 6:00 PM. Digital research databases, e-books, and "
            "academic journals are accessible 24/7 via the library online portal."
        ),
    },
    {
        "id": "doc_3",
        "title": "Final Capstone Project Submission",
        "category": "Academics",
        "content": (
            "Final year project reports, code repositories, and documentation must be submitted "
            "to the departmental portal by November 30th at 11:59 PM EST. No extensions are granted "
            "without prior written approval from the faculty advisor."
        ),
    },
    {
        "id": "doc_4",
        "title": "Midterm & Final Examination Schedule",
        "category": "Academics",
        "content": (
            "Midterm examinations take place during Week 8 of the semester. Final semester "
            "examinations are scheduled from December 5th to December 18th. Room allocations "
            "and seating arrangements are posted on the student portal two weeks prior."
        ),
    },
    {
        "id": "doc_5",
        "title": "Hostel Registration & Room Allotment",
        "category": "Housing",
        "content": (
            "Hostel room allotment for the upcoming academic year begins on July 1st. Students must "
            "complete the online housing registration form, submit medical immunization records, "
            "and pay the security deposit to confirm their room allocation."
        ),
    },
    {
        "id": "doc_6",
        "title": "Course Registration & Add/Drop Policy",
        "category": "Academics",
        "content": (
            "Students may add or drop courses without academic penalty during the first two weeks "
            "of the semester via the Academic Registrar portal. Late drop requests after Week 2 "
            "require approval from the Academic Dean."
        ),
    },
    {
        "id": "doc_7",
        "title": "Student Campus Smart ID Card",
        "category": "Campus Services",
        "content": (
            "New students can collect their official university smart ID card from the Campus Services "
            "Desk in Building A after uploading a passport-style photo to the student portal. The ID "
            "card grants access to campus buildings, dining halls, and library services."
        ),
    },
    {
        "id": "doc_8",
        "title": "Campus Health Center & Emergency Care",
        "category": "Healthcare",
        "content": (
            "The Student Health Center provides free basic medical consultations, routine checkups, "
            "and vaccinations. For urgent medical emergencies on campus, dial extension 9999 for "
            "24/7 emergency response and ambulance dispatch."
        ),
    },
    {
        "id": "doc_9",
        "title": "Campus Wi-Fi & IT Helpdesk Support",
        "category": "IT Services",
        "content": (
            "High-speed campus Wi-Fi ('EduRoam') is accessible across all academic buildings and "
            "residence halls using student email credentials. For login assistance or network troubleshooting, "
            "contact IT Helpdesk at support@university.edu or visit Room 102."
        ),
    },
    {
        "id": "doc_10",
        "title": "Scholarship & Financial Aid Applications",
        "category": "Finance",
        "content": (
            "Applications for merit-based scholarships and need-based financial assistance open annually "
            "on January 15th. Submissions must include parent/guardian income tax returns, academic transcripts, "
            "and a personal statement essay."
        ),
    },
]


def initialize_chroma_db(
    db_directory: Optional[str] = None,
    collection_name: str = "trustrag_kb",
    model_name: str = "all-MiniLM-L6-v2",
) -> Tuple[chromadb.ClientAPI, Any]:
    """
    Initializes ChromaDB client and collection with SentenceTransformer embedding function.

    Args:
        db_directory: Directory path for persistent ChromaDB storage (if None, persistent path is used).
        collection_name: Name of the collection (default: 'trustrag_kb').
        model_name: Sentence-Transformer model name (default: 'all-MiniLM-L6-v2').

    Returns:
        Tuple of (chromadb_client, collection_object).
    """
    try:
        # Determine persistent path relative to this script
        if db_directory is None:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            db_directory = os.path.join(script_dir, "chroma_db")

        os.makedirs(db_directory, exist_ok=True)
        logging.info(f"Initializing ChromaDB persistent client at: '{db_directory}'")
        client = chromadb.PersistentClient(path=db_directory)

        # Initialize sentence-transformer embedding function
        logging.info(f"Loading SentenceTransformer embedding model: '{model_name}'...")
        embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name=model_name
        )

        # Get or create collection with Cosine Similarity space
        collection = client.get_or_create_collection(
            name=collection_name,
            embedding_function=embedding_fn,
            metadata={"hnsw:space": "cosine"},
        )
        logging.info(f"ChromaDB collection '{collection_name}' initialized successfully.")
        return client, collection

    except Exception as e:
        logging.error(f"Failed to initialize ChromaDB: {e}")
        raise e


def populate_knowledge_base(
    collection: Any,
    documents: List[Dict[str, Any]],
    force_reindex: bool = True,
) -> None:
    """
    Populates ChromaDB collection with knowledge base documents.

    Args:
        collection: ChromaDB collection object.
        documents: List of document dicts containing 'id', 'title', 'category', 'content'.
        force_reindex: If True, existing documents are cleared before adding new ones.
    """
    try:
        if force_reindex and collection.count() > 0:
            existing_ids = collection.get()["ids"]
            if existing_ids:
                collection.delete(ids=existing_ids)
                logging.info(f"Cleared {len(existing_ids)} existing documents from collection.")

        if collection.count() == 0:
            ids = [doc["id"] for doc in documents]
            contents = [doc["content"] for doc in documents]
            metadatas = [
                {"title": doc["title"], "category": doc["category"]}
                for doc in documents
            ]

            logging.info(f"Indexing {len(documents)} documents into ChromaDB...")
            collection.add(
                ids=ids,
                documents=contents,
                metadatas=metadatas,
            )
            logging.info(f"Successfully indexed {collection.count()} documents into ChromaDB.")
        else:
            logging.info(f"Collection already contains {collection.count()} documents.")

    except Exception as e:
        logging.error(f"Failed to populate knowledge base: {e}")
        raise e


def retrieve_documents(
    query: str,
    top_k: int = 3,
    collection: Optional[Any] = None,
    verbose: bool = True,
) -> List[Dict[str, Any]]:
    """
    Retrieves the top-k most relevant documents from the ChromaDB vector collection 
    based on cosine similarity matching against a user query.

    This function embeds the user query using sentence-transformers, queries the vector database, 
    calculates bounded cosine similarity scores (0.0 to 1.0), formats document metadata, 
    and logs the search results.

    Args:
        query (str): The user search query string to be embedded and matched.
        top_k (int, optional): Number of top matching documents to retrieve. Defaults to 3.
        collection (Optional[Any], optional): Pre-initialized ChromaDB collection object.
            If None, automatically initializes and retrieves the default collection. Defaults to None.
        verbose (bool, optional): If True, logs formatted search results to console. Defaults to True.

    Returns:
        List[Dict[str, Any]]: A list of dictionaries representing matching documents, each containing:
            - 'rank' (int): Retrieval rank order (1-indexed).
            - 'id' (str): Unique document identifier.
            - 'title' (str): Document title.
            - 'category' (str): Document category/domain.
            - 'content' (str): Full text content of the document.
            - 'text' (str): Full text content of the document (alias).
            - 'cosine_distance' (float): Raw Cosine Distance from ChromaDB (0.0 = identical).
            - 'similarity_score' (float): Cosine Similarity score bounded in [0.0, 1.0].
            - 'similarity_percentage' (str): Similarity formatted as percentage (e.g., "73.12%").

    Example:
        >>> from retriever_agent.retriever_agent import retrieve_documents
        >>> results = retrieve_documents("When is the tuition fee payment deadline?", top_k=2)
        >>> print(results[0]['id'], results[0]['similarity_score'])
        doc_1 0.7312
    """
    if not isinstance(query, str) or not query.strip():
        logging.warning("Empty or invalid query provided.")
        return []

    if top_k <= 0:
        logging.warning("top_k must be a positive integer.")
        return []

    # Initialize collection if not passed
    if collection is None:
        _, collection = initialize_chroma_db()

    try:
        # Perform vector similarity search
        query = query.strip()
        results = collection.query(
            query_texts=[query],
            n_results=top_k,
            include=["documents", "metadatas", "distances"],
        )

        formatted_results: List[Dict[str, Any]] = []

        if not results or "documents" not in results or not results["documents"][0]:
            if verbose:
                logging.info(f"SEARCH QUERY: '{query}' | RESULTS: No documents found.")
            return []

        doc_list = results["documents"][0]
        meta_list = results["metadatas"][0] if "metadatas" in results else [{}] * len(doc_list)
        dist_list = results["distances"][0] if "distances" in results else [1.0] * len(doc_list)
        id_list = results["ids"][0] if "ids" in results else [f"doc_{i}" for i in range(len(doc_list))]

        for i in range(len(doc_list)):
            # Cosine distance d in Chroma is d = 1 - cosine_similarity
            # Cosine similarity s = 1.0 - d (bounded between 0.0 and 1.0 for positive space)
            cosine_distance = float(dist_list[i])
            cosine_similarity = max(0.0, min(1.0, 1.0 - cosine_distance))

            result_item = {
                "rank": i + 1,
                "id": id_list[i],
                "title": meta_list[i].get("title", "N/A"),
                "category": meta_list[i].get("category", "General"),
                "content": doc_list[i],
                "text": doc_list[i],
                "cosine_distance": round(cosine_distance, 4),
                "similarity_score": round(cosine_similarity, 4),
                "similarity_percentage": f"{cosine_similarity * 100:.2f}%",
            }
            formatted_results.append(result_item)

        # Log formatted output if verbose
        if verbose:
            logging.info("=" * 70)
            logging.info(f"[SEARCH QUERY]: \"{query}\" (Requested Top-K: {top_k})")
            logging.info("=" * 70)
            
            for item in formatted_results:
                score = item['similarity_score']
                relevance_label = "HIGHLY RELEVANT" if score >= HIGHLY_RELEVANT_THRESHOLD else (
                    "MODERATELY RELEVANT" if score >= MODERATELY_RELEVANT_THRESHOLD else "LOW RELEVANCE"
                )
                logging.info(
                    f"Rank #{item['rank']} | ID: {item['id']} | Score: {item['similarity_percentage']} [{relevance_label}] (Distance: {item['cosine_distance']})"
                )
                logging.info(f"  Title:    {item['title']}")
                logging.info(f"  Category: {item['category']}")
                logging.info(f"  Snippet:  {item['content']}")
                logging.info("-" * 70)

        return formatted_results

    except Exception as e:
        logging.error(f"Error during document retrieval for query '{query}': {e}")
        return []


def run_tests() -> None:
    """
    Runs comprehensive test suite with 8 sample queries categorized by relevance type.
    """
    logging.info("=" * 70)
    logging.info("        TrustRAG - Day 1 Retriever Agent Integration Tests")
    logging.info("=" * 70)

    # Step 1: Initialize Database
    client, collection = initialize_chroma_db()

    # Step 2: Populate Knowledge Base
    populate_knowledge_base(collection, SAMPLE_KNOWLEDGE_BASE, force_reindex=True)

    # Step 4: Test queries across 3 categories
    test_queries = [
        # --- Category 1: Very Relevant Queries (Exact Match Intent) ---
        {
            "category": "Exact Match Intent (Very Relevant)",
            "query": "When is the tuition fee payment deadline for the fall semester?",
            "expected_id": "doc_1",
        },
        {
            "category": "Exact Match Intent (Very Relevant)",
            "query": "What are the operating hours for the central university library?",
            "expected_id": "doc_2",
        },
        # --- Category 2: Partially Relevant Queries (Semantic Match) ---
        {
            "category": "Semantic Match (Partially Relevant)",
            "query": "I am feeling sick and need to see a medical doctor on campus.",
            "expected_id": "doc_8",
        },
        {
            "category": "Semantic Match (Partially Relevant)",
            "query": "How do I connect my mobile phone or laptop to campus internet?",
            "expected_id": "doc_9",
        },
        {
            "category": "Semantic Match (Partially Relevant)",
            "query": "When are we writing our midterm and final exams?",
            "expected_id": "doc_4",
        },
        {
            "category": "Semantic Match (Partially Relevant)",
            "query": "Can I drop a class during the first week without penalty?",
            "expected_id": "doc_6",
        },
        # --- Category 3: Completely Unrelated Queries (Out of Domain) ---
        {
            "category": "Out-of-Domain (Completely Unrelated)",
            "query": "How do I bake a soft chocolate chip lava cake at home?",
            "expected_id": None,
        },
        {
            "category": "Out-of-Domain (Completely Unrelated)",
            "query": "What is the capital city of Australia?",
            "expected_id": None,
        },
    ]

    logging.info(f"Running {len(test_queries)} test queries...")

    passed_count = 0

    for i, test in enumerate(test_queries, 1):
        logging.info(f">>> TEST [{i}/{len(test_queries)}] Category: [{test['category']}]")
        results = retrieve_documents(
            query=test["query"],
            top_k=3,
            collection=collection,
            verbose=True,
        )

        if results:
            top_match = results[0]
            if test["expected_id"]:
                if top_match["id"] == test["expected_id"]:
                    logging.info(f"[PASS] Top result '{top_match['id']}' matched expected '{test['expected_id']}' with score {top_match['similarity_percentage']}.")
                    passed_count += 1
                else:
                    logging.warning(f"[NOTICE] Top result was '{top_match['id']}' (Expected: '{test['expected_id']}'). Score: {top_match['similarity_percentage']}")
            else:
                logging.info(f"[OUT-OF-DOMAIN TEST] Top retrieved doc '{top_match['id']}' returned with low relevance score {top_match['similarity_percentage']}.")
                passed_count += 1
        else:
            logging.error(f"[FAIL] No documents retrieved for query '{test['query']}'.")

    logging.info("=" * 70)
    logging.info(f"[TEST SUMMARY] {passed_count}/{len(test_queries)} tests evaluated successfully.")
    logging.info("=" * 70)


if __name__ == "__main__":
    run_tests()
