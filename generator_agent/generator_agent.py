import os
from typing import Dict, List
from openai import OpenAI
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

# Import prompts
from .prompt_templates import SYSTEM_PROMPT, USER_PROMPT_TEMPLATE, ESCALATION_PROMPT


class GeneratorAgent:
    """
    Generator Agent - Creates answers using OpenAI ChatGPT

    Receives:
    - User query
    - Retrieved documents (from Module 2 Retriever)
    - Confidence score (from Module 3 Verifier)

    Outputs:
    - Natural language answer
    - Source citations
    - Success status
    """

    def __init__(self, model: str = "gpt-3.5-turbo", temperature: float = 0.7):
        """Initialize Generator Agent"""
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not found in .env file")

        self.client = OpenAI(api_key=self.api_key)
        self.model = model
        self.temperature = temperature
        self.max_tokens = 500
        print(f"✓ Generator Agent initialized with {model}")

    def format_documents(self, documents: List[Dict]) -> str:
        """Convert documents to readable text for LLM"""
        if not documents:
            return "No documents available."

        formatted = ""
        for doc in documents:
            doc_id = doc.get("doc_id", "unknown")
            content = doc.get("content", "No content")
            similarity = doc.get("similarity", 0)

            formatted += f"\n[{doc_id}] (Match: {similarity:.0%})\n{content}\n"

        return formatted

    def generate_answer(
        self,
        query: str,
        documents: List[Dict],
        confidence_score: float
    ) -> Dict:
        """
        Generate answer using ChatGPT

        Inputs:
        - query: User's question
        - documents: Retrieved documents from Module 2
        - confidence_score: Confidence from Module 3 (0.0-1.0)

        Outputs:
        - Dictionary with answer, sources, status
        """
        # If confidence is too low, escalate
        if confidence_score < 0.50:
            return {
                "answer": ESCALATION_PROMPT.format(query=query),
                "sources": [],
                "timestamp": datetime.now().isoformat(),
                "success": True,
                "status": "escalated",
                "confidence": confidence_score
            }

        # Format documents for ChatGPT
        formatted_docs = self.format_documents(documents)

        # Create the prompt
        user_message = USER_PROMPT_TEMPLATE.format(
            query=query,
            retrieved_docs=formatted_docs
        )

        try:
            # Call ChatGPT API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_message}
                ],
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )

            # Get the answer
            answer = response.choices[0].message.content.strip()

            # Get sources
            sources = [
                {
                    "doc_id": doc.get("doc_id", ""),
                    "similarity": doc.get("similarity", 0)
                }
                for doc in documents
            ]

            return {
                "answer": answer,
                "sources": sources,
                "timestamp": datetime.now().isoformat(),
                "model_used": self.model,
                "tokens_used": response.usage.total_tokens,
                "success": True,
                "confidence": confidence_score
            }

        except Exception as e:
            print(f"❌ Error: {str(e)}")
            return {
                "answer": f"Error generating answer: {str(e)}",
                "sources": [],
                "timestamp": datetime.now().isoformat(),
                "success": False,
                "error": str(e)
            }

    def batch_generate(
        self,
        queries: List[str],
        documents_list: List[List[Dict]],
        confidence_scores: List[float]
    ) -> List[Dict]:
        """Generate answers for multiple queries"""
        results = []
        for query, docs, confidence in zip(queries, documents_list, confidence_scores):
            result = self.generate_answer(query, docs, confidence)
            results.append(result)
        return results
