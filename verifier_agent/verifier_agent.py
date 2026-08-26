"""
TrustRAG - Day 2: Verifier Agent Module
========================================
This module implements the Verifier Agent for TrustRAG, which computes confidence scores 
for retrieved document context and dynamically routes queries to either the Generator 
(high confidence) or Escalation/Admin support (low confidence).

Features:
1. Confidence Scoring Function: `compute_confidence()` based on top-k similarity scores.
2. Routing Decision Function: `route_query()` comparing confidence scores against thresholds.
3. Full Verification Pipeline: `verify_and_route()` combining retrieval, scoring, and routing.
4. Comprehensive logging, error handling, and threshold tuning capabilities.
"""

import logging
import os
import sys
from typing import List, Dict, Any, Optional, Tuple

# Reconfigure parent path to enable direct module imports
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

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
logger = logging.getLogger("VerifierAgent")

# ---------------------------------------------------------------------------
# Confidence Threshold Constants
# ---------------------------------------------------------------------------
DEFAULT_CONFIDENCE_THRESHOLD = 0.65  # Default boundary (65%)
HIGH_CONFIDENCE_THRESHOLD = 0.75     # High confidence boundary (75%)
LOW_CONFIDENCE_THRESHOLD = 0.40      # Low confidence boundary (40%)


# Step 0: Import Day 1 Retriever Module
try:
    from retriever_agent.retriever_agent import (
        retrieve_documents,
        initialize_chroma_db,
        populate_knowledge_base,
        SAMPLE_KNOWLEDGE_BASE,
    )
except ImportError as e:
    logging.error(f"Failed to import Day 1 Retriever Agent: {e}")
    sys.exit(1)


def compute_confidence(
    retrieved_docs: List[Dict[str, Any]],
    query: Optional[str] = None,
    method: str = "average_similarity",
) -> float:
    """
    Computes the overall confidence score C(q) for a query based on retrieved documents' similarity scores.

    Args:
        retrieved_docs (List[Dict[str, Any]]): List of document dicts returned by the retriever,
            where each document contains a 'similarity_score' float between 0.0 and 1.0.
        query (Optional[str], optional): Original user search query (optional context). Defaults to None.
        method (str, optional): Calculation method to use:
            - 'average_similarity': Mean average of all similarity scores in retrieved_docs.
            - 'max_similarity': Maximum similarity score among retrieved_docs.
            Defaults to 'average_similarity'.

    Returns:
        float: Calculated confidence score C(q) bounded between 0.0 and 1.0. Returns 0.0 for empty lists.

    Example:
        >>> docs = [{'similarity_score': 0.73}, {'similarity_score': 0.68}, {'similarity_score': 0.45}]
        >>> compute_confidence(docs)
        0.62

    Raises:
        ValueError: If an unsupported calculation method is specified.
    """
    if not retrieved_docs or not isinstance(retrieved_docs, list):
        logging.warning("Empty or invalid retrieved documents list provided. Returning confidence score 0.0.")
        return 0.0

    # Extract similarity scores from document dictionaries
    scores: List[float] = []
    for doc in retrieved_docs:
        if isinstance(doc, dict) and "similarity_score" in doc:
            scores.append(float(doc["similarity_score"]))
        elif isinstance(doc, dict) and "score" in doc:
            scores.append(float(doc["score"]))

    if not scores:
        logging.warning("No similarity scores found in retrieved documents. Returning 0.0.")
        return 0.0

    if method == "average_similarity":
        confidence = sum(scores) / len(scores)
    elif method == "max_similarity":
        confidence = max(scores)
    else:
        raise ValueError(f"Unsupported confidence calculation method: '{method}'. Use 'average_similarity' or 'max_similarity'.")

    # Bound confidence score between 0.0 and 1.0
    bounded_confidence = max(0.0, min(1.0, float(confidence)))
    return round(bounded_confidence, 4)


def route_query(
    query: str,
    confidence_score: float,
    threshold: float = DEFAULT_CONFIDENCE_THRESHOLD,
) -> Dict[str, Any]:
    """
    Determines query routing decision ('GENERATE' vs 'ESCALATE') by comparing 
    confidence score C(q) against the specified threshold.

    Args:
        query (str): The search query string.
        confidence_score (float): Calculated confidence score C(q) between 0.0 and 1.0.
        threshold (float, optional): Threshold boundary. Defaults to DEFAULT_CONFIDENCE_THRESHOLD (0.65).

    Returns:
        Dict[str, Any]: Routing decision dictionary containing:
            - 'decision' (str): Either 'GENERATE' or 'ESCALATE'.
            - 'confidence' (float): The confidence score evaluated.

    Example:
        >>> route_query("When are exams?", 0.75, threshold=0.65)
        {'decision': 'GENERATE', 'confidence': 0.75}
    """
    conf_pct = f"{confidence_score * 100:.2f}%"
    thresh_pct = f"{threshold * 100:.2f}%"

    if confidence_score >= threshold:
        decision = "GENERATE"
        logging.info(f"Query confidence: {conf_pct} >= {thresh_pct} threshold -> Decision: GENERATE")
    else:
        decision = "ESCALATE"
        logging.info(f"Query confidence: {conf_pct} < {thresh_pct} threshold -> Decision: ESCALATE")

    return {
        "decision": decision,
        "confidence": confidence_score,
    }


def verify_and_route(
    query: str,
    retriever_collection: Optional[Any] = None,
    threshold: float = DEFAULT_CONFIDENCE_THRESHOLD,
    verbose: bool = True,
) -> Dict[str, Any]:
    """
    Executes the full verifier pipeline: retrieves documents using Day 1 retriever, 
    computes confidence score C(q), and determines query routing decision.

    Args:
        query (str): User input search query string.
        retriever_collection (Optional[Any], optional): Pre-initialized ChromaDB collection object.
        threshold (float, optional): Decision threshold. Defaults to DEFAULT_CONFIDENCE_THRESHOLD (0.65).
        verbose (bool, optional): If True, logs step-by-step pipeline output. Defaults to True.

    Returns:
        Dict[str, Any]: Comprehensive result dictionary containing:
            - 'query' (str): Original search query.
            - 'retrieved_documents' (list): List of top-3 retrieved document dictionaries.
            - 'confidence_score' (float): Calculated confidence score C(q) (0.0 to 1.0).
            - 'confidence_percentage' (str): Confidence score formatted as percentage.
            - 'threshold' (float): Threshold boundary float used.
            - 'threshold_percentage' (str): Threshold formatted as percentage.
            - 'decision' (str): 'GENERATE' or 'ESCALATE'.
            - 'reasoning' (str): Human-readable decision explanation.
    """
    if not isinstance(query, str) or not query.strip():
        logging.warning("Empty or invalid query provided to verify_and_route().")
        return {
            "query": query,
            "retrieved_documents": [],
            "confidence_score": 0.0,
            "confidence_percentage": "0.00%",
            "threshold": threshold,
            "threshold_percentage": f"{threshold * 100:.2f}%",
            "decision": "ESCALATE",
            "reasoning": "Query is empty or invalid.",
        }

    # Step 1: Call Day 1 Retriever
    retrieved_docs = retrieve_documents(
        query=query,
        top_k=3,
        collection=retriever_collection,
        verbose=False,
    )

    # Step 2: Compute Confidence Score C(q)
    confidence_score = compute_confidence(retrieved_docs, query=query, method="average_similarity")

    # Step 3: Route Query based on Threshold
    routing_result = route_query(query, confidence_score, threshold=threshold)
    decision = routing_result["decision"]

    # Formulate Reasoning Explanation
    conf_pct = f"{confidence_score * 100:.2f}%"
    thresh_pct = f"{threshold * 100:.2f}%"

    if decision == "GENERATE":
        reasoning = (
            f"Query confidence score ({conf_pct}) meets or exceeds the threshold ({thresh_pct}). "
            f"Retrieved context is sufficiently relevant for direct AI generation."
        )
    else:
        reasoning = (
            f"Query confidence score ({conf_pct}) is below the required threshold ({thresh_pct}). "
            f"Retrieved context is insufficient or uncertain; query routed to Escalation/Human Support."
        )

    # Verbose Output Presentation
    if verbose:
        logging.info("=" * 75)
        logging.info("        🔍 VERIFIER AGENT EVALUATION")
        logging.info("=" * 75)
        logging.info(f" Search Query: \"{query}\"")
        logging.info(" Retrieved Documents (Top-3):")
        
        if retrieved_docs:
            for doc in retrieved_docs:
                logging.info(
                    f"   Rank #{doc.get('rank', 'N/A')} | ID: {doc.get('id', 'N/A')} | "
                    f"Title: {doc.get('title', 'N/A')} | Similarity: {doc.get('similarity_percentage', 'N/A')}"
                )
        else:
            logging.info("   [No documents retrieved]")

        logging.info(f" Calculated Confidence Score C(q): {conf_pct} (Average of Top-3 Similarity Scores)")
        logging.info(f" Threshold Boundary:              {thresh_pct}")
        logging.info(f" Routing Decision:                [{decision}]")
        logging.info(f" Reasoning:                       {reasoning}")
        logging.info("-" * 75)

    return {
        "query": query,
        "retrieved_documents": retrieved_docs,
        "confidence_score": confidence_score,
        "confidence_percentage": conf_pct,
        "threshold": threshold,
        "threshold_percentage": thresh_pct,
        "decision": decision,
        "reasoning": reasoning,
    }


def run_tests() -> None:
    """
    Runs comprehensive test suite for Verifier Agent with 8 test queries 
    across High Confidence, Medium Confidence, Low Confidence, and Threshold Tuning scenarios.
    """
    logging.info("=" * 75)
    logging.info("        TrustRAG - Day 2 Verifier Agent Integration Tests")
    logging.info("=" * 75)

    # Initialize Retriever Database
    client, collection = initialize_chroma_db()
    populate_knowledge_base(collection, SAMPLE_KNOWLEDGE_BASE, force_reindex=False)

    # Define 8 Test Queries across 4 Categories
    test_queries = [
        # --- CATEGORY A: HIGH CONFIDENCE QUERIES (Should route to GENERATE) ---
        {
            "test_num": 1,
            "category": "CATEGORY A: HIGH CONFIDENCE (GENERATE)",
            "query": "When is the tuition fee payment deadline for the fall semester?",
            "threshold": 0.55,
            "expected_decision": "GENERATE",
        },
        {
            "test_num": 2,
            "category": "CATEGORY A: HIGH CONFIDENCE (GENERATE)",
            "query": "What are the operating hours for the central university library?",
            "threshold": 0.55,
            "expected_decision": "GENERATE",
        },
        # --- CATEGORY B: MEDIUM CONFIDENCE QUERIES (Should route to ESCALATE) ---
        {
            "test_num": 3,
            "category": "CATEGORY B: MEDIUM CONFIDENCE (ESCALATE)",
            "query": "Do I need to register for on-campus hostel accommodation?",
            "threshold": 0.55,
            "expected_decision": "ESCALATE",
        },
        {
            "test_num": 4,
            "category": "CATEGORY B: MEDIUM CONFIDENCE (ESCALATE)",
            "query": "Can I change my major after I complete my first semester?",
            "threshold": 0.55,
            "expected_decision": "ESCALATE",
        },
        # --- CATEGORY C: LOW CONFIDENCE QUERIES (Should route to ESCALATE) ---
        {
            "test_num": 5,
            "category": "CATEGORY C: LOW CONFIDENCE / OUT-OF-DOMAIN (ESCALATE)",
            "query": "How do I bake a soft chocolate chip lava cake at home?",
            "threshold": 0.55,
            "expected_decision": "ESCALATE",
        },
        {
            "test_num": 6,
            "category": "CATEGORY C: LOW CONFIDENCE / OUT-OF-DOMAIN (ESCALATE)",
            "query": "What is the capital city of Australia?",
            "threshold": 0.55,
            "expected_decision": "ESCALATE",
        },
        # --- ADDITIONAL EDGE CASE TESTS (THRESHOLD TUNING) ---
        {
            "test_num": 7,
            "category": "THRESHOLD TUNING: Strict Threshold (0.80 -> ESCALATE)",
            "query": "When is the tuition fee payment deadline for the fall semester?",
            "threshold": 0.80,
            "expected_decision": "ESCALATE",
        },
        {
            "test_num": 8,
            "category": "THRESHOLD TUNING: Relaxed Threshold (0.50 -> GENERATE)",
            "query": "When is the tuition fee payment deadline for the fall semester?",
            "threshold": 0.50,
            "expected_decision": "GENERATE",
        },
    ]

    logging.info(f"Running {len(test_queries)} Verifier Agent integration tests...\n")
    passed_count = 0

    for test in test_queries:
        logging.info(f">>> TEST [{test['test_num']}/8] {test['category']}")
        result = verify_and_route(
            query=test["query"],
            retriever_collection=collection,
            threshold=test["threshold"],
            verbose=True,
        )

        decision = result["decision"]
        expected = test["expected_decision"]

        if decision == expected:
            logging.info(
                f"[PASS] Decision '{decision}' matched expected '{expected}' "
                f"(Confidence: {result['confidence_percentage']}, Threshold: {result['threshold_percentage']}).\n"
            )
            passed_count += 1
        else:
            logging.warning(
                f"[FAIL/NOTICE] Decision '{decision}' (Expected: '{expected}') "
                f"(Confidence: {result['confidence_percentage']}, Threshold: {result['threshold_percentage']}).\n"
            )

    logging.info("=" * 75)
    logging.info(f"[TEST SUMMARY] {passed_count}/{len(test_queries)} tests executed successfully.")
    logging.info("=" * 75 + "\n")


if __name__ == "__main__":
    run_tests()
