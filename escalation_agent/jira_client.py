"""
Jira REST API Client for TrustRAG Escalation
"""

import os
import requests
from typing import Dict, Optional
from dotenv import load_dotenv
import base64

load_dotenv()

class JiraClient:
    """Client for Jira REST API integration"""
    
    def __init__(self):
        """Initialize Jira client with credentials from .env"""
        self.domain = os.getenv("JIRA_DOMAIN")
        self.email = os.getenv("JIRA_EMAIL")
        self.api_token = os.getenv("JIRA_API_TOKEN")
        self.project_key = os.getenv("JIRA_PROJECT_KEY")
        
        if not all([self.domain, self.email, self.api_token, self.project_key]):
            raise ValueError("Missing Jira configuration in .env file")
        
        # Create base auth
        auth_str = f"{self.email}:{self.api_token}"
        self.auth_header = base64.b64encode(auth_str.encode()).decode()
        
        self.base_url = f"{self.domain}/rest/api/3"
        self.headers = {
            "Authorization": f"Basic {self.auth_header}",
            "Content-Type": "application/json"
        }
        
        print(f"✓ Jira client initialized for project: {self.project_key}")
    
    def create_issue(
        self, 
        summary: str, 
        description: str,
        issue_type: str = "Task"
    ) -> Dict:
        """
        Create Jira issue (ticket)
        
        Args:
            summary: Ticket title
            description: Ticket description
            issue_type: Type of issue (Task, Bug, Story, etc.)
        
        Returns:
            Dict with issue key and ID
        """
        url = f"{self.base_url}/issue"
        
        payload = {
            "fields": {
                "project": {
                    "key": self.project_key
                },
                "summary": summary,
                "description": {
                    "type": "doc",
                    "version": 1,
                    "content": [
                        {
                            "type": "paragraph",
                            "content": [
                                {
                                    "type": "text",
                                    "text": description
                                }
                            ]
                        }
                    ]
                },
                "issuetype": {
                    "name": issue_type
                }
            }
        }
        
        try:
            response = requests.post(url, json=payload, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            return {
                "success": True,
                "issue_key": data.get("key"),
                "issue_id": data.get("id"),
                "url": f"{self.domain}/browse/{data.get('key')}"
            }
        except Exception as e:
            print(f"❌ Error creating Jira issue: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def get_issue(self, issue_key: str) -> Dict:
        """Get issue details by key"""
        url = f"{self.base_url}/issue/{issue_key}"
        
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            return {
                "success": True,
                "key": data.get("key"),
                "status": data.get("fields", {}).get("status", {}).get("name"),
                "summary": data.get("fields", {}).get("summary"),
                "description": data.get("fields", {}).get("description")
            }
        except Exception as e:
            print(f"❌ Error getting issue: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def update_issue(self, issue_key: str, updates: Dict) -> Dict:
        """Update issue fields"""
        url = f"{self.base_url}/issue/{issue_key}"
        
        payload = {"fields": updates}
        
        try:
            response = requests.put(url, json=payload, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            return {"success": True, "message": "Issue updated"}
        except Exception as e:
            print(f"❌ Error updating issue: {str(e)}")
            return {"success": False, "error": str(e)}
