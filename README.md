# TrustRAG: Self-Learning AI Chatbot with Blockchain Verification 🛡️🤖

[![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Vector DB](https://img.shields.io/badge/Vector%20DB-ChromaDB-green.svg)](https://www.trychroma.com/)
[![Embeddings](https://img.shields.io/badge/Model-SentenceTransformers--all--MiniLM--L6--v2-orange.svg)](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2)
[![Project Status](https://img.shields.io/badge/Status-25%25%20Complete%20(Days%201--2)-brightgreen.svg)]()
[![Build & Tests](https://img.shields.io/badge/Tests-16%2F16%20Passed%20(100%25)-success.svg)]()
[![Git Commits](https://img.shields.io/badge/Commits-27%20Sequential%20Commits-blue.svg)]()

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
├── [Module 1] 🟢 Retriever Agent (Day 1 - Completed)
│   └── Vector DB Storage (ChromaDB), SentenceTransformers, KB Indexing
├── [Module 2] 🟢 Verifier Agent (Day 2 - Completed)
│   └── Confidence Scoring C(q), Dynamic Routing Engine (GENERATE / ESCALATE)
├── [Module 3] ⏳ Generator Agent (Day 3 - Planned)
│   └── Prompt Construction, Context Injection, LLM Response Generation
├── [Module 4] ⏳ Feedback & Self-Learning Agent (Day 4 - Planned)
│   └── User Rating Collector, Vector Store Fine-tuning & Re-ranking
├── [Module 5] ⏳ Admin & Escalation Dashboard (Day 5 - Planned)
│   └── Human-in-the-Loop Review, Query Resolution Queue
├── [Module 6] ⏳ Blockchain Verification Logger (Day 6 - Planned)
│   └── Immutable Audit Trail, Smart Contract Verification Logs
├── [Module 7] ⏳ API Gateway & FastAPI Service (Day 7 - Planned)
│   └── REST Endpoints, Authentication, Async Pipeline Execution
└── [Module 8] ⏳ Web UI Frontend Interface (Days 8-10 - Planned)
    └── Dynamic Interactive Dashboard, Chat UI, Real-Time Confidence Visualizer
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

- **Current Completion:** **25% Complete** (2 out of 8 modules finished)
- **Sprint Status:** Days 1 & 2 of 10-day sprint complete.
- **Test Verification:** **16/16 Tests Passing (100% Success Rate)**

```text
[██████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░] 25% Completed
Days Completed: Day 1 (Retriever) & Day 2 (Verifier)
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

- [x] **Day 1:** Retriever Agent & ChromaDB Vector Store Setup (Completed)
- [x] **Day 2:** Verifier Agent & Dynamic Routing Pipeline (Completed)
- [ ] **Day 3:** Generator Agent & LLM Prompt Context Integration
- [ ] **Day 4:** Feedback Engine & Vector Index Fine-tuning
- [ ] **Day 5:** Admin & Escalation Console
- [ ] **Day 6:** Blockchain Audit Trail & Web3 Integration
- [ ] **Day 7:** FastAPI REST Gateway
- [ ] **Days 8–10:** Interactive Frontend UI & End-to-End System Evaluation

---

## 📚 References

1. P. Lewis et al., "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks," in *Advances in Neural Information Processing Systems (NeurIPS)*, vol. 33, pp. 9459–9474, 2020.
2. N. Reimers and I. Gurevych, "Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks," in *Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing (EMNLP)*, pp. 3982–3992, 2019.
3. ChromaDB Team, "Chroma: The AI-native Open-Source Embedding Database," *ChromaDB Documentation*, 2023. [Online]. Available: https://docs.trychroma.com
