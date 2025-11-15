"""Build training database from collected feedback"""

import json
import argparse
from pathlib import Path
from typing import List, Dict
import numpy as np
from sklearn.model_selection import train_test_split
from config import MIN_FEEDBACK_SAMPLES, SEMANTIC_SIMILARITY_THRESHOLD

class DatabaseBuilder:
    def __init__(self, input_file: str, output_dir: str):
        self.input_file = Path(input_file)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def load_feedback(self) -> List[Dict]:
        """Load all feedback from JSONL file"""
        feedback_list = []
        with open(self.input_file, "r", encoding="utf-8") as f:
            for line in f:
                feedback_list.append(json.loads(line))
        return feedback_list
    
    def calculate_semantic_similarity(self, emb1: List[float], emb2: List[float]) -> float:
        """Calculate cosine similarity between two embeddings"""
        emb1 = np.array(emb1)
        emb2 = np.array(emb2)
        return np.dot(emb1, emb2) / (np.linalg.norm(emb1) * np.linalg.norm(emb2))
    
    def create_training_pairs(self, feedback_list: List[Dict]) -> List[Dict]:
        """Create training pairs from feedback"""
        training_pairs = []
        
        for feedback in feedback_list:
            rating = feedback["feedback"]["rating"]
            query = feedback["query"]
            context = "\n".join(feedback["context"])
            response = feedback["response"]
            ideal_response = feedback["feedback"]["ideal_response"]
            
            # Calculate semantic similarity
            semantic_sim = self.calculate_semantic_similarity(
                feedback["embeddings"]["response"],
                feedback["embeddings"]["ideal"]
            )
            
            # High-quality responses (rating >= 4 and high semantic similarity)
            if rating >= 4 and semantic_sim >= SEMANTIC_SIMILARITY_THRESHOLD:
                training_pairs.append({
                    "instruction": query,
                    "context": context,
                    "response": response,
                    "quality": "high",
                    "rating": rating,
                    "semantic_similarity": semantic_sim
                })
            
            # Use corrected version for low-quality responses
            elif rating < 4 and ideal_response != response:
                training_pairs.append({
                    "instruction": query,
                    "context": context,
                    "response": ideal_response,
                    "quality": "corrected",
                    "rating": rating,
                    "semantic_similarity": semantic_sim
                })
        
        return training_pairs
    
    def format_for_training(self, pair: Dict) -> str:
        """Format training pair into prompt template"""
        prompt = f"""### Instruction:
{pair['instruction']}

### Context:
{pair['context']}

### Response:
{pair['response']}"""
        return prompt
    
    def build_database(self):
        """Main database building process"""
        print("Loading feedback...")
        feedback_list = self.load_feedback()
        print(f"Loaded {len(feedback_list)} feedback samples")
        
        if len(feedback_list) < MIN_FEEDBACK_SAMPLES:
            print(f"Warning: Only {len(feedback_list)} samples. Recommended minimum: {MIN_FEEDBACK_SAMPLES}")
        
        print("\nCreating training pairs...")
        training_pairs = self.create_training_pairs(feedback_list)
        print(f"Created {len(training_pairs)} training pairs")
        
        # Split into train/validation
        train_pairs, val_pairs = train_test_split(
            training_pairs,
            test_size=0.1,
            random_state=42
        )
        
        print(f"Train: {len(train_pairs)}, Validation: {len(val_pairs)}")
        
        # Save training data
        train_file = self.output_dir / "train.jsonl"
        val_file = self.output_dir / "val.jsonl"
        
        with open(train_file, "w", encoding="utf-8") as f:
            for pair in train_pairs:
                f.write(json.dumps(pair) + "\n")
        
        with open(val_file, "w", encoding="utf-8") as f:
            for pair in val_pairs:
                f.write(json.dumps(pair) + "\n")
        
        # Save formatted prompts
        train_prompts_file = self.output_dir / "train_prompts.txt"
        with open(train_prompts_file, "w", encoding="utf-8") as f:
            for pair in train_pairs:
                f.write(self.format_for_training(pair) + "\n\n" + "="*80 + "\n\n")
        
        print(f"\n✓ Training data saved to {self.output_dir}")
        print(f"  - {train_file}")
        print(f"  - {val_file}")
        print(f"  - {train_prompts_file}")
        
        # Statistics
        high_quality = sum(1 for p in training_pairs if p["quality"] == "high")
        corrected = sum(1 for p in training_pairs if p["quality"] == "corrected")
        avg_rating = sum(p["rating"] for p in training_pairs) / len(training_pairs)
        
        print(f"\nStatistics:")
        print(f"  High quality: {high_quality}")
        print(f"  Corrected: {corrected}")
        print(f"  Average rating: {avg_rating:.2f}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build training database from feedback")
    parser.add_argument("--input", default="feedback_db/interactions.jsonl", help="Input feedback file")
    parser.add_argument("--output", default="feedback_db/training_pairs", help="Output directory")
    
    args = parser.parse_args()
    
    builder = DatabaseBuilder(args.input, args.output)
    builder.build_database()
