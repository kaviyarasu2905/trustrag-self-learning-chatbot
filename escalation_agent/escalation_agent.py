"""
Escalation Agent - Handles low-confidence query escalation to Jira
"""

import os
from typing import Dict, List
from datetime import datetime
from dotenv import load_dotenv
from .jira_client import JiraClient

load_dotenv()

class EscalationAgent:
    """
    Escalation Agent - Creates Jira tickets for low-confidence queries
    
    Receives:
    - User query
    - Confidence score (from Module 3)
    - Previous attempts/context
    
    Actions:
    - Create Jira ticket for human review
    - Track escalation status
    - Store admin response in KB
    """
    
    def __init__(self):
        """Initialize Escalation Agent with Jira client"""
        try:
            self.jira = JiraClient()
            self.escalation_threshold = 0.50
            print("✓ Escalation Agent initialized")
        except Exception as e:
            print(f"❌ Failed to initialize Escalation Agent: {e}")
            raise
    
    def should_escalate(self, confidence_score: float) -> bool:
        """Determine if query should be escalated"""
        return confidence_score < self.escalation_threshold
    
    def create_escalation_ticket(
        self,
        query: str,
        confidence_score: float,
        retrieved_docs: List[Dict] = None,
        user_id: str = "anonymous"
    ) -> Dict:
        """
        Create Jira ticket for escalated query
        
        Args:
            query: The user's question
            confidence_score: System confidence (0.0-1.0)
            retrieved_docs: Documents retrieved (if any)
            user_id: User identifier
        
        Returns:
            Dict with ticket key, status, and URL
        """
        # Format ticket summary and description
        summary = f"[Escalated] {query[:100]}"
        
        doc_info = ""
        if retrieved_docs:
            doc_info = "Retrieved Documents:\n"
            for doc in retrieved_docs:
                doc_id = doc.get("doc_id", "unknown")
                similarity = doc.get("similarity", 0)
                doc_info += f"- {doc_id} (Similarity: {similarity:.2f})\n"
        
        description = f"""
Query: {query}

Confidence Score: {confidence_score:.2f} (Below 0.50 threshold)
User ID: {user_id}
Timestamp: {datetime.now().isoformat()}

{doc_info}

Action Required: 
Please review this query and provide the correct answer. 
The answer will be stored in the knowledge base for future reference.
"""
        
        # Create Jira issue
        result = self.jira.create_issue(
            summary=summary,
            description=description,
            issue_type="Task"
        )
        
        if result["success"]:
            print(f"✓ Escalation ticket created: {result['issue_key']}")
        
        return {
            "escalated": True,
            "issue_key": result.get("issue_key"),
            "issue_url": result.get("url"),
            "status": "pending_review",
            "timestamp": datetime.now().isoformat(),
            "confidence": confidence_score,
            "success": result["success"]
        }
    
    def check_escalation_status(self, issue_key: str) -> Dict:
        """Check status of escalated ticket"""
        issue = self.jira.get_issue(issue_key)
        
        if not issue["success"]:
            return {"success": False, "error": issue["error"]}
        
        return {
            "success": True,
            "issue_key": issue_key,
            "status": issue.get("status"),
            "summary": issue.get("summary"),
            "resolved": issue.get("status") == "Done"
        }
    
    def batch_escalate(
        self,
        queries: List[str],
        confidence_scores: List[float],
        user_ids: List[str] = None
    ) -> List[Dict]:
        """Escalate multiple queries at once"""
        if user_ids is None:
            user_ids = ["anonymous"] * len(queries)
        
        results = []
        for query, confidence, user_id in zip(queries, confidence_scores, user_ids):
            if self.should_escalate(confidence):
                result = self.create_escalation_ticket(query, confidence, user_id=user_id)
                results.append(result)
        
        return results
    
    def get_escalation_stats(self) -> Dict:
        """Get escalation statistics"""
        return {
            "escalation_threshold": self.escalation_threshold,
            "jira_project": self.jira.project_key,
            "jira_domain": self.jira.domain,
            "status": "operational"
        }
