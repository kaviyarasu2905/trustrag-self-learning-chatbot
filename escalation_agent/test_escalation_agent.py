import sys
import os
from unittest.mock import Mock, patch, MagicMock

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from escalation_agent import EscalationAgent

import io, sys as _sys
_sys.stdout = io.TextIOWrapper(_sys.stdout.buffer, encoding='utf-8', errors='replace')

print("\n" + "="*60)
print("[TEST] MODULE 5: ESCALATION AGENT - TEST SUITE")
print("[INFO] Using MOCKED Jira API (no tickets created)")
print("="*60 + "\n")

passed = 0
failed = 0

try:
    print("Initializing Escalation Agent...")
    agent = EscalationAgent()
    print("✓ Escalation Agent initialized\n")
except Exception as e:
    print(f"❌ Failed to initialize: {e}")
    sys.exit(1)

# TEST 1: Initialization
try:
    assert agent is not None
    assert agent.escalation_threshold == 0.50
    assert agent.jira is not None
    print("Test 1 (Initialization): PASSED ✓")
    passed += 1
except AssertionError:
    print("Test 1 (Initialization): FAILED ✗")
    failed += 1

# TEST 2: Should Escalate - Low Confidence
try:
    should_escalate = agent.should_escalate(0.30)
    assert should_escalate is True
    print("Test 2 (Should Escalate - Low): PASSED ✓")
    passed += 1
except AssertionError:
    print("Test 2 (Should Escalate - Low): FAILED ✗")
    failed += 1

# TEST 3: Should Not Escalate - High Confidence
try:
    should_escalate = agent.should_escalate(0.75)
    assert should_escalate is False
    print("Test 3 (Should Not Escalate - High): PASSED ✓")
    passed += 1
except AssertionError:
    print("Test 3 (Should Not Escalate - High): FAILED ✗")
    failed += 1

# TEST 4: Create Escalation Ticket (MOCKED)
try:
    print("\n[Running Jira API Test with MOCKED response...]")
    
    mock_result = {
        "success": True,
        "issue_key": "KAN-1",
        "url": "https://test.atlassian.net/browse/KAN-1"
    }
    
    with patch.object(agent.jira, 'create_issue', return_value=mock_result):
        result = agent.create_escalation_ticket(
            query="What is the campus location?",
            confidence_score=0.30
        )
    
    assert result["escalated"] is True
    assert result["issue_key"] == "KAN-1"
    assert result["status"] == "pending_review"
    assert result["success"] is True
    print("Test 4 (Create Escalation Ticket - MOCKED): PASSED ✓")
    passed += 1
except AssertionError as e:
    print(f"Test 4 (Create Escalation Ticket): FAILED ✗ - {e}")
    failed += 1

# TEST 5: Escalation with Documents
try:
    mock_result = {
        "success": True,
        "issue_key": "KAN-2",
        "url": "https://test.atlassian.net/browse/KAN-2"
    }
    
    docs = [
        {"doc_id": "doc_1", "content": "Some content", "similarity": 0.45}
    ]
    
    with patch.object(agent.jira, 'create_issue', return_value=mock_result):
        result = agent.create_escalation_ticket(
            query="Test query",
            confidence_score=0.40,
            retrieved_docs=docs
        )
    
    assert result["success"] is True
    assert "KAN-2" in result["issue_key"]
    print("Test 5 (Escalation with Documents): PASSED ✓")
    passed += 1
except AssertionError:
    print("Test 5 (Escalation with Documents): FAILED ✗")
    failed += 1

# TEST 6: Check Escalation Status (MOCKED)
try:
    mock_issue = {
        "success": True,
        "status": "In Progress",
        "summary": "Test issue"
    }
    
    with patch.object(agent.jira, 'get_issue', return_value=mock_issue):
        result = agent.check_escalation_status("KAN-1")
    
    assert result["success"] is True
    assert result["issue_key"] == "KAN-1"
    assert result["resolved"] is False
    print("Test 6 (Check Escalation Status): PASSED ✓")
    passed += 1
except AssertionError:
    print("Test 6 (Check Escalation Status): FAILED ✗")
    failed += 1

# TEST 7: Batch Escalation (MOCKED)
try:
    mock_result = {
        "success": True,
        "issue_key": "KAN-3",
        "url": "https://test.atlassian.net/browse/KAN-3"
    }
    
    with patch.object(agent.jira, 'create_issue', return_value=mock_result):
        queries = ["Q1?", "Q2?", "Q3?"]
        confidences = [0.30, 0.25, 0.75]  # Last one won't escalate
        
        results = agent.batch_escalate(queries, confidences)
    
    assert len(results) == 2  # Only 2 escalations (first two)
    assert all(r["escalated"] for r in results)
    print("Test 7 (Batch Escalation): PASSED ✓")
    passed += 1
except AssertionError as e:
    print(f"Test 7 (Batch Escalation): FAILED ✗ - {e}")
    failed += 1

# TEST 8: Escalation Statistics
try:
    stats = agent.get_escalation_stats()
    
    assert stats["escalation_threshold"] == 0.50
    assert stats["jira_project"] == "KAN"
    assert stats["status"] == "operational"
    print("Test 8 (Escalation Statistics): PASSED ✓")
    passed += 1
except AssertionError:
    print("Test 8 (Escalation Statistics): FAILED ✗")
    failed += 1

# SUMMARY
print("\n" + "="*60)
print(f"RESULTS: {passed} PASSED ✓ | {failed} FAILED ✗")
print("="*60)

if passed == 8:
    print("\n✅ ALL 8/8 TESTS PASSED - MODULE 5 COMPLETE!")
    print("   (Using MOCKED Jira API - no tickets created)")
    print("="*60 + "\n")
    sys.exit(0)
else:
    print(f"\n❌ {failed} test(s) failed")
    print("="*60 + "\n")
    sys.exit(1)
