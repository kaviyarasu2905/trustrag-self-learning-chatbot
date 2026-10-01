# TrustRAG Frontend (Module 1 - React + Tailwind CSS) 🛡️💬

Production-ready React user interface for the **TrustRAG Self-Learning RAG Framework**. Built for **Day 7** of the 10-day development sprint, providing a verified conversational UI with real-time confidence scores, knowledge base citations, blockchain auditability, and active user feedback collection.

---

## 🚀 Features

- **Modern Chat Interface:** Responsive chat pane with auto-scrolling, query suggestions, markdown rendering, and user question / system answer pairing.
- **Visual Trust Score Gauge:** Circular SVG gauge displaying scores between 0.00 and 1.00 with color-coded classification:
  - 🟢 **High Trust (0.67 – 1.00):** `#27ae60`
  - 🟡 **Medium Trust (0.34 – 0.66):** `#f39c12`
  - 🔴 **Low Trust (0.00 – 0.33):** `#e74c3c`
- **Collapsible Source Citations:** Formatted knowledge base sources `Sources: doc_1 (0.85), doc_2 (0.72)` with top-match badges, snippet viewer, and one-click clipboard copy.
- **Verification & Blockchain Badges:** Visual proof of Verifier Agent clearance (`Verified & Accurate`, `Pending Human Review`, `Blockchain Verified`, `Escalated to Admin`) with interactive transaction audit inspection modal.
- **Self-Learning Feedback Loop:** Thumbs up/down and 1-5 star rating selector that dispatches query evaluation metrics to `/feedback`.
- **Intelligent Fallback Architecture:** Automatically queries FastAPI on `http://localhost:8000` while providing responsive client-side fallbacks during offline local development.

---

## 📁 Project Structure

```text
frontend/
├── src/
│   ├── components/
│   │   ├── ChatInterface.jsx         # Conversational interface with input & history
│   │   ├── ResponseDisplay.jsx       # Answer card, markdown & streaming animation
│   │   ├── TrustScoreDisplay.jsx     # Circular gauge & color-coded trust score
│   │   ├── SourceCitations.jsx       # Collapsible vector DB document citations
│   │   ├── VerificationBadge.jsx     # Blockchain & Verifier Agent status badge
│   │   └── LoadingSpinner.jsx        # Animated query processing indicator
│   ├── services/
│   │   └── api.js                    # Axios client for FastAPI (localhost:8000)
│   ├── App.jsx                       # Master state management & modal controller
│   ├── App.css                       # Animations & custom scrollbar styles
│   ├── index.css                     # Tailwind CSS base & utilities
│   ├── index.jsx                     # Application entrypoint
│   └── main.jsx                      # Vite module bridge
├── tailwind.config.js                # TrustRAG color system and theme config
├── postcss.config.js                 # Tailwind & Autoprefixer configuration
├── package.json                      # Dependencies & scripts
└── test-runner.js                    # Automated 8-test verification runner
```

---

## 🛠️ Getting Started

### 1. Install Dependencies
```bash
npm install
```

### 2. Start Vite Development Server
```bash
npm run dev
```
Navigate to `http://localhost:5173` in your browser.

### 3. Run Automated Test Suite
```bash
npm test
```

### 4. Build for Production
```bash
npm run build
```

---

## 🧪 Automated Test Verification

All 8 required test cases pass with a 100% success rate:

```text
Test 1 (Chat interface renders): PASSED ✓
Test 2 (Send query works): PASSED ✓
Test 3 (Trust Score displays): PASSED ✓
Test 4 (Source citations format): PASSED ✓
Test 5 (Verification badge shows): PASSED ✓
Test 6 (Responsive design): PASSED ✓
Test 7 (Error handling): PASSED ✓
Test 8 (Feedback submission): PASSED ✓

✅ ALL 8 TESTS PASSED - Module 1 Complete!
```
