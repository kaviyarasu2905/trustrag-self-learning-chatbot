# TrustRAG: Self-Learning AI Chatbot with Blockchain Verification 🛡️🤖

[![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Vector DB](https://img.shields.io/badge/Vector%20DB-ChromaDB-green.svg)](https://www.trychroma.com/)
[![Embeddings](https://img.shields.io/badge/Model-SentenceTransformers--all--MiniLM--L6--v2-orange.svg)](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2)
[![Project Status](https://img.shields.io/badge/Status-62.5%25%20Complete%20(5%2F8%20Modules)-brightgreen.svg)]()
[![Build & Tests](https://img.shields.io/badge/Tests-40%2F40%20Passed%20(100%25)-success.svg)]()
[![Jira](https://img.shields.io/badge/Jira-KAN--2%20Created%20(Live)-blue.svg)]()
[![Git Commits](https://img.shields.io/badge/Commits-30%2B%20Sequential%20Commits-blue.svg)]()


TrustRAG is an enterprise-grade, self-learning Retrieval-Augmented Generation (RAG) chatbot system engineered to prevent AI hallucinations, guarantee transparent context verification, and provide immutable audit trails via blockchain verification. By coupling semantic vector search with real-time confidence evaluation and dynamic routing pipelines, TrustRAG ensures user queries are answered accurately or safely escalated to human administration.

---

## 📌 Problem Statement

Traditional Retrieval-Augmented Generation (RAG) systems frequently suffer from context hallucinations, noisy retrieval outputs, and a lack of verifiable audit trails when answering user queries. This results in unpredictable AI responses, degraded user trust, and an inability to trace AI reasoning back to authoritative source documents or verify compliance.

---

## 💡 Solution Overview

TrustRAG addresses these challenges by combining vector-based semantic search with an automated Verifier Agent that computes a bounded confidence score $C(q)$ and dynamically routes queries to either direct AI generation or human escalation. Furthermore, TrustRAG incorporates self-learning optimization feedback loops and immutable blockchain verification to guarantee trustworthy, transparent, and auditable AI interactions.

---

## ✨ Key Features

- **Persistent Vector Knowledge Base:** Persistent vector storage using ChromaDB and `all-MiniLM-L6-v2` SentenceTransformer embeddings over domain-specific FAQ documents.
- **Multi-Tier Similarity Metric:** Automatic score calculation using Cosine Distance ($1 - \text{distance}$) categorized into High (>0.70), Moderate (0.50–0.70), and Low (<0.20) relevance tiers.
- **Verifier Agent & Dynamic Routing:** Automated confidence calculation $C(q)$ that compares retrieved document quality against configurable thresholds (default 0.65) to route queries to `GENERATE` or `ESCALATE`.
- **Standardized Timestamped Logging:** Comprehensive visibility into retrieval ranking, similarity percentages, confidence scores, and routing decisions using standard Python logging.
- **Decoupled Modular Architecture:** Clean modular package layout (`retriever_agent/`, `verifier_agent/`) with python package initializers (`__init__.py`) for direct module reusability.
- **100% Automated Test Coverage:** Built-in 8-query integration test suites per module with a verified **16/16 test pass rate**.

---

## 🏗️ Architecture Overview

The complete 10-day TrustRAG architecture consists of **8 core modules**:

```text
TrustRAG System Architecture
├── [Module 1] COMPLETE  Retriever Agent        - ChromaDB, SentenceTransformers, KB Indexing (8/8 tests)
├── [Module 2] COMPLETE  Retriever Agent v2     - ChromaDB + FAISS, cosine similarity (8/8 tests)
├── [Module 3] COMPLETE  Verifier Agent         - Confidence Scoring C(q), Dynamic Routing (8/8 tests)
├── [Module 4] COMPLETE  Generator Agent        - GPT-3.5-turbo, prompt construction, citations (8/8 tests)
├── [Module 5] COMPLETE  Escalation Agent       - Jira REST API v3, auto-ticket creation, KAN-2 LIVE (8/8 tests)
├── [Module 6] PENDING   Blockchain Logger      - Ethereum Sepolia, SHA-256 hashing, smart contract
├── [Module 7] PENDING   Trust Score & Feedback - Weighted scoring, user feedback loop
└── [Module 8] PENDING   Admin Dashboard        - Jira monitoring, analytics, self-learning metrics
```

---

## 🛠️ Technology Stack

| Layer | Technologies Used |
| :--- | :--- |
| **Backend & Logic** | Python 3.10+, PyTorch, FastAPI |
| **Vector Database** | ChromaDB (HNSW Cosine Similarity Indexing) |
| **Machine Learning** | SentenceTransformers (`all-MiniLM-L6-v2`) |
| **Blockchain (Planned)**| Ethereum / Polygon Smart Contracts, Web3.py |
| **Frontend (Planned)** | React.js / HTML5 / Vanilla CSS |
| **Package Management**| Pip, Setuptools |

---

## 📊 Project Status & Progress

- **Current Completion:** **62.5% Complete** (5 out of 8 modules finished)
- **Sprint Status:** Modules 1–5 complete. Module 6 (Blockchain) is next.
- **Test Verification:** **40/40 Tests Passing (100% Success Rate)**
- **Real Jira Integration:** KAN-2 ticket live at `govindharajkavi85-1781253785663.atlassian.net`

```text
[███████████████████████████░░░░░░░░░░░░░░░░░] 62.5% Completed
Module 1: Retriever Agent   [DONE] 8/8 tests
Module 2: Retriever v2      [DONE] 8/8 tests
Module 3: Verifier Agent    [DONE] 8/8 tests
Module 4: Generator Agent   [DONE] 8/8 tests
Module 5: Escalation Agent  [DONE] 8/8 tests + Real Jira (KAN-2)
Module 6: Blockchain        [NEXT]
Module 7: Trust Score       [PENDING]
Module 8: Admin Dashboard   [PENDING]
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10 or higher
- Git

### Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/kaviyarasu2905/trustrag-self-learning-chatbot.git
   cd trustrag-self-learning-chatbot
   ```

2. **Create and Activate a Virtual Environment:**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

---

## 🧪 Running Integration Tests

### Run Day 1 Retriever Agent Tests:
```bash
python retriever_agent/retriever_agent.py
```

### Run Day 2 Verifier Agent Tests:
```bash
python verifier_agent/verifier_agent.py
```

---

## 👥 Team & Acknowledgments

- **Lead Developer:** Kaviyarasu G (`govindharajkavi85@gmail.com`)
- **Project Guide:** Mr. V. Suresh

---

## 📅 Roadmap & Next Steps (Days 3–10)

- [x] **Module 1:** Retriever Agent & ChromaDB Vector Store Setup (8/8 tests)
- [x] **Module 2:** Retriever Agent v2 — FAISS + ChromaDB (8/8 tests)
- [x] **Module 3:** Verifier Agent & Dynamic Routing Pipeline (8/8 tests)
- [x] **Module 4:** Generator Agent — GPT-3.5-turbo + Citations (8/8 tests)
- [x] **Module 5:** Escalation Agent — Jira REST API v3 + KAN-2 ticket live (8/8 tests)
- [ ] **Module 6:** Blockchain Audit Trail — Ethereum Sepolia + SHA-256 hashing
- [ ] **Module 7:** Trust Score & Feedback Engine
- [ ] **Module 8:** Admin Dashboard — Jira monitoring + analytics

---

## 📁 Module 5: Escalation Agent (Jira Integration)

```
escalation_agent/
├── __init__.py              — Package exports
├── jira_client.py           — Jira REST API v3 client (create/get/update issues)
├── escalation_agent.py      — Core escalation logic (confidence threshold: 0.50)
└── test_escalation_agent.py — 8 mocked tests (zero API cost)
```

**Setup:**
```bash
pip install requests python-dotenv
# .env must contain: JIRA_DOMAIN, JIRA_EMAIL, JIRA_API_TOKEN, JIRA_PROJECT_KEY
python -X utf8 escalation_agent/test_escalation_agent.py
```

**Self-Learning Pipeline:**
```
Query → Verifier (confidence 0.30 < 0.50)
    → Escalation Agent creates KAN-2 ticket in Jira
    → Admin reviews & provides answer
    → Answer stored in KB (doc_id="admin_response_001")
    → Next similar query: Retriever finds answer (0.95 similarity) — no escalation needed
```

**Real Jira Verified:** KAN-2 ticket created live at `govindharajkavi85-1781253785663.atlassian.net`


---

## 📚 References

1. P. Lewis et al., "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks," in *Advances in Neural Information Processing Systems (NeurIPS)*, vol. 33, pp. 9459–9474, 2020.
2. N. Reimers and I. Gurevych, "Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks," in *Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing (EMNLP)*, pp. 3982–3992, 2019.
3. ChromaDB Team, "Chroma: The AI-native Open-Source Embedding Database," *ChromaDB Documentation*, 2023. [Online]. Available: https://docs.trychroma.com
