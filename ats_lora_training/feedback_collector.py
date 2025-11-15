"""Feedback collection system for model responses"""

import json
import uuid
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional
from sentence_transformers import SentenceTransformer
import numpy as np

class FeedbackCollector:
    def __init__(self, db_path: str = "feedback_db"):
        self.db_path = Path(db_path)
        self.db_path.mkdir(exist_ok=True)
        
        # Create subdirectories
        (self.db_path / "embeddings").mkdir(exist_ok=True)
        (self.db_path / "training_pairs").mkdir(exist_ok=True)
        
        self.interactions_file = self.db_path / "interactions.jsonl"
        self.embedding_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
        
    def collect_feedback(
        self,
        query: str,
        context: List[str],
        response: str,
        interaction_id: Optional[str] = None
    ) -> Dict:
        """
        Interactive feedback collection from user
        """
        print("\n" + "="*60)
        print("RESPONSE FEEDBACK COLLECTION")
        print("="*60)
        print(f"\nQuery: {query}")
        print(f"\nResponse: {response}\n")
        
        rating = int(input("Rate this response (1-5): "))
        correct = input("What was correct? (comma-separated or press Enter): ")
        incorrect = input("What was incorrect? (comma-separated or press Enter): ")
        missing = input("What was missing? (comma-separated or press Enter): ")
        ideal = input("What should the ideal response be? (or press Enter): ")
        
        feedback_data = {
            "id": interaction_id or str(uuid.uuid4()),
            "timestamp": datetime.now().isoformat(),
            "query": query,
            "context": context,
            "response": response,
            "feedback": {
                "rating": rating,
                "correct_points": [p.strip() for p in correct.split(",") if p.strip()],
                "incorrect_points": [p.strip() for p in incorrect.split(",") if p.strip()],
                "missing_points": [p.strip() for p in missing.split(",") if p.strip()],
                "ideal_response": ideal if ideal.strip() else response
            }
        }
        
        # Generate embeddings
        feedback_data["embeddings"] = {
            "query": self.embedding_model.encode(query).tolist(),
            "response": self.embedding_model.encode(response).tolist(),
            "ideal": self.embedding_model.encode(feedback_data["feedback"]["ideal_response"]).tolist()
        }
        
        # Save to JSONL
        self._save_feedback(feedback_data)
        
        print(f"\n✓ Feedback saved with ID: {feedback_data['id']}")
        return feedback_data
    
    def save_feedback(
        self,
        interaction_id: str,
        query: str,
        context: List[str],
        response: str,
        rating: int,
        correct_points: List[str],
        incorrect_points: List[str],
        ideal_response: str
    ) -> Dict:
        """
        Save feedback programmatically (for API integration)
        """
        feedback_data = {
            "id": interaction_id,
            "timestamp": datetime.now().isoformat(),
            "query": query,
            "context": context,
            "response": response,
            "feedback": {
                "rating": rating,
                "correct_points": correct_points,
                "incorrect_points": incorrect_points,
                "ideal_response": ideal_response
            }
        }
        
        # Generate embeddings
        feedback_data["embeddings"] = {
            "query": self.embedding_model.encode(query).tolist(),
            "response": self.embedding_model.encode(response).tolist(),
            "ideal": self.embedding_model.encode(ideal_response).tolist()
        }
        
        self._save_feedback(feedback_data)
        return feedback_data
    
    def _save_feedback(self, feedback_data: Dict):
        """Save feedback to JSONL file"""
        with open(self.interactions_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(feedback_data) + "\n")
    
    def get_feedback_count(self) -> int:
        """Get total number of feedback samples"""
        if not self.interactions_file.exists():
            return 0
        
        with open(self.interactions_file, "r", encoding="utf-8") as f:
            return sum(1 for _ in f)
    
    def get_average_rating(self) -> float:
        """Get average rating across all feedback"""
        if not self.interactions_file.exists():
            return 0.0
        
        ratings = []
        with open(self.interactions_file, "r", encoding="utf-8") as f:
            for line in f:
                data = json.loads(line)
                ratings.append(data["feedback"]["rating"])
        
        return sum(ratings) / len(ratings) if ratings else 0.0

if __name__ == "__main__":
    # Example usage
    collector = FeedbackCollector()
    
    feedback = collector.collect_feedback(
        query="Analyze this resume for Software Engineer position",
        context=["Context chunk 1", "Context chunk 2"],
        response="This candidate has strong Python skills and 5 years of experience."
    )
    
    print(f"\nTotal feedback samples: {collector.get_feedback_count()}")
    print(f"Average rating: {collector.get_average_rating():.2f}")
