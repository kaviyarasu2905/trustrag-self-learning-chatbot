# -*- coding: utf-8 -*-
import sys
import os
from unittest.mock import MagicMock, patch

# Force UTF-8 output on Windows
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from generator_agent import GeneratorAgent

print("\n" + "=" * 60)
print("🧪 MODULE 4: GENERATOR AGENT - TEST SUITE")
print("🔄 Using MOCKED API (no credits needed)")
print("=" * 60 + "\n")

passed = 0
failed = 0

try:
    print("Initializing Generator Agent...")
    generator = GeneratorAgent()
    print("✓ Generator initialized\n")
except Exception as e:
    print(f"❌ Failed to initialize: {e}")
    sys.exit(1)

# TEST 1: Initialize
try:
    assert generator is not None
    assert generator.model == "gpt-3.5-turbo"
    assert generator.temperature == 0.7
    print("Test 1 (Initialization): PASSED ✓")
    passed += 1
except AssertionError:
    print("Test 1 (Initialization): FAILED ✗")
    failed += 1

# TEST 2: Format Documents
try:
    docs = [
        {"doc_id": "doc_1", "content": "Campus is in Coimbatore", "similarity": 0.85},
        {"doc_id": "doc_2", "content": "Phone: 123-456", "similarity": 0.72}
    ]
    formatted = generator.format_documents(docs)
    assert "doc_1" in formatted
    assert "doc_2" in formatted
    assert "85%" in formatted or "0.85" in formatted
    print("Test 2 (Format Documents): PASSED ✓")
    passed += 1
except AssertionError:
    print("Test 2 (Format Documents): FAILED ✗")
    failed += 1

# TEST 3: Empty Documents
try:
    formatted = generator.format_documents([])
    assert "No documents" in formatted
    print("Test 3 (Empty Documents): PASSED ✓")
    passed += 1
except AssertionError:
    print("Test 3 (Empty Documents): FAILED ✗")
    failed += 1

# TEST 4: High Confidence Generation (MOCKED)
try:
    print("\n[Running API Test with MOCKED response...]")

    mock_response = MagicMock()
    mock_response.choices[0].message.content = (
        "Our campus is located in Coimbatore, Tamil Nadu, India. "
        "It provides world-class facilities for students."
    )
    mock_response.usage.total_tokens = 45

    with patch.object(generator.client.chat.completions, 'create', return_value=mock_response):
        query = "What is the campus location?"
        docs = [
            {
                "doc_id": "doc_1",
                "content": "Our campus is located in Coimbatore, Tamil Nadu, India",
                "similarity": 0.88
            }
        ]
        result = generator.generate_answer(query, docs, 0.75)

    assert result["success"] is True
    assert len(result["answer"]) > 0
    assert result["timestamp"] is not None
    assert len(result["sources"]) > 0
    assert "Coimbatore" in result["answer"]
    print("Test 4 (High Confidence Answer - MOCKED): PASSED ✓")
    passed += 1
except AssertionError as e:
    print(f"Test 4 (High Confidence Answer): FAILED ✗ - {e}")
    failed += 1
except Exception as e:
    print(f"Test 4 (High Confidence Answer): FAILED ✗ - {e}")
    failed += 1

# TEST 5: Low Confidence Escalation
try:
    query = "Unknown obscure question"
    result = generator.generate_answer(query, [], 0.30)

    assert result["success"] is True
    assert result.get("status") == "escalated"
    assert "human" in result["answer"].lower()
    print("Test 5 (Low Confidence Escalation): PASSED ✓")
    passed += 1
except AssertionError:
    print("Test 5 (Low Confidence Escalation): FAILED ✗")
    failed += 1

# TEST 6: Source Citation Format (MOCKED)
try:
    mock_response = MagicMock()
    mock_response.choices[0].message.content = "Test answer"
    mock_response.usage.total_tokens = 25

    with patch.object(generator.client.chat.completions, 'create', return_value=mock_response):
        query = "Test question"
        docs = [
            {"doc_id": "doc_5", "content": "Content here", "similarity": 0.82},
            {"doc_id": "doc_7", "content": "More content", "similarity": 0.65}
        ]
        result = generator.generate_answer(query, docs, 0.70)

    sources = result.get("sources", [])
    assert len(sources) >= 1
    assert sources[0]["doc_id"] in ["doc_5", "doc_7"]
    print("Test 6 (Source Citations - MOCKED): PASSED ✓")
    passed += 1
except AssertionError:
    print("Test 6 (Source Citations): FAILED ✗")
    failed += 1

# TEST 7: Timestamp Format (MOCKED)
try:
    mock_response = MagicMock()
    mock_response.choices[0].message.content = "Answer"
    mock_response.usage.total_tokens = 15

    with patch.object(generator.client.chat.completions, 'create', return_value=mock_response):
        result = generator.generate_answer(
            "Test?",
            [{"doc_id": "d1", "content": "test", "similarity": 0.8}],
            0.75
        )

    assert result["timestamp"] is not None
    assert "T" in result["timestamp"]  # ISO format check
    print("Test 7 (Timestamp Format): PASSED ✓")
    passed += 1
except AssertionError:
    print("Test 7 (Timestamp Format): FAILED ✗")
    failed += 1

# TEST 8: Batch Generation (MOCKED)
try:
    mock_response = MagicMock()
    mock_response.choices[0].message.content = "Batch answer"
    mock_response.usage.total_tokens = 30

    with patch.object(generator.client.chat.completions, 'create', return_value=mock_response):
        queries = ["Q1?", "Q2?", "Q3?"]
        docs_list = [
            [{"doc_id": "d1", "content": "A1", "similarity": 0.85}],
            [{"doc_id": "d2", "content": "A2", "similarity": 0.90}],
            [{"doc_id": "d3", "content": "A3", "similarity": 0.80}]
        ]
        confidences = [0.75, 0.80, 0.70]

        results = generator.batch_generate(queries, docs_list, confidences)

    assert len(results) == 3
    assert all(r["success"] for r in results)
    print("Test 8 (Batch Generation - MOCKED): PASSED ✓")
    passed += 1
except AssertionError:
    print("Test 8 (Batch Generation): FAILED ✗")
    failed += 1

# SUMMARY
print("\n" + "=" * 60)
print(f"RESULTS: {passed} PASSED ✓ | {failed} FAILED ✗")
print("=" * 60)

if passed == 8:
    print("\n✅ ALL 8/8 TESTS PASSED - MODULE 4 COMPLETE!")
    print("   (Using MOCKED API - no credits used)")
    print("=" * 60 + "\n")
    sys.exit(0)
else:
    print(f"\n❌ {failed} test(s) failed")
    print("=" * 60 + "\n")
    sys.exit(1)
