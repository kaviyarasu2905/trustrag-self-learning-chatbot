# Day 4: Module 5 - Escalation Agent (Jira Integration)

## Overview
Escalation Agent creates Jira tickets for low-confidence queries.

## Architecture

```
User Query
↓
Retriever (Module 2) → Get documents
↓
Verifier (Module 3) → Get confidence score
↓
Generator (Module 4) → Try to answer
↓
Confidence < 0.50?
├─ NO  → Return answer ✓
└─ YES → Escalation Agent (THIS MODULE)
         ├─ Create Jira ticket
         ├─ Wait for admin response
         ├─ Store answer in KB
         └─ Future query uses stored answer (self-learning!)
```

## Files Created

| File | Purpose |
|------|---------|
| `escalation_agent/__init__.py` | Package exports |
| `escalation_agent/jira_client.py` | Jira REST API client |
| `escalation_agent/escalation_agent.py` | Core escalation logic |
| `escalation_agent/test_escalation_agent.py` | 8-test suite (mocked) |

## Key Methods

### EscalationAgent
- `should_escalate(confidence_score)` — Returns `True` if score < 0.50
- `create_escalation_ticket(query, confidence, docs, user_id)` — Creates Jira task
- `check_escalation_status(issue_key)` — Polls ticket status
- `batch_escalate(queries, scores)` — Bulk escalation
- `get_escalation_stats()` — Returns threshold + project info

### JiraClient
- `create_issue(summary, description, issue_type)` — POST to Jira REST API v3
- `get_issue(issue_key)` — GET issue by key
- `update_issue(issue_key, updates)` — PUT field updates

## Environment Variables Required

```
JIRA_DOMAIN=https://your-domain.atlassian.net
JIRA_EMAIL=your@email.com
JIRA_API_TOKEN=your_token
JIRA_PROJECT_KEY=KAN
```

## Test Results
- 8/8 tests pass using mocked Jira API
- No real tickets created during testing
