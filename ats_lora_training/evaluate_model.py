"""Evaluate trained LoRA model"""

import json
import argparse
import torch
from pathlib import Path
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel
from sentence_transformers import SentenceTransformer, util
from tqdm import tqdm

class ModelEvaluator:
    def __init__(self, model_path: str, test_data_path: str):
        self.model_path = Path(model_path)
        self.test_data_path = Path(test_data_path)
        self.semantic_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
        
    def load_model(self):
        """Load fine-tuned model"""
        print(f"Loading model from {self.model_path}")
        
        # Load base model
        base_model_name = "mistralai/Mistral-7B-v0.1"  # Should match training
        model = AutoModelForCausalLM.from_pretrained(
            base_model_name,
            device_map="auto",
            torch_dtype=torch.float16
        )
        
        # Load LoRA weights
        model = PeftModel.from_pretrained(model, str(self.model_path / "final"))
        
        tokenizer = AutoTokenizer.from_pretrained(str(self.model_path / "final"))
        
        return model, tokenizer
    
    def load_test_data(self):
        """Load test data"""
        test_data = []
        with open(self.test_data_path, "r", encoding="utf-8") as f:
            for line in f:
                test_data.append(json.loads(line))
        return test_data
    
    def generate_response(self, model, tokenizer, instruction: str, context: str):
        """Generate response from model"""
        prompt = f"""### Instruction:
{instruction}

### Context:
{context}

### Response:
"""
        
        inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
        
        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=512,
                temperature=0.7,
                do_sample=True,
                top_p=0.9
            )
        
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        # Extract only the response part
        response = response.split("### Response:")[-1].strip()
        
        return response
    
    def calculate_semantic_similarity(self, text1: str, text2: str) -> float:
        """Calculate semantic similarity"""
        emb1 = self.semantic_model.encode(text1, convert_to_tensor=True)
        emb2 = self.semantic_model.encode(text2, convert_to_tensor=True)
        similarity = util.cos_sim(emb1, emb2)
        return similarity.item()
    
    def evaluate(self):
        """Run evaluation"""
        print("Loading model...")
        model, tokenizer = self.load_model()
        
        print("Loading test data...")
        test_data = self.load_test_data()
        print(f"Test samples: {len(test_data)}")
        
        results = []
        semantic_scores = []
        
        print("\nEvaluating...")
        for example in tqdm(test_data):
            instruction = example["instruction"]
            context = example["context"]
            reference = example["response"]
            
            # Generate response
            generated = self.generate_response(model, tokenizer, instruction, context)
            
            # Calculate semantic similarity
            semantic_score = self.calculate_semantic_similarity(generated, reference)
            semantic_scores.append(semantic_score)
            
            results.append({
                "instruction": instruction,
                "reference": reference,
                "generated": generated,
                "semantic_similarity": semantic_score
            })
        
        # Calculate metrics
        avg_semantic_score = sum(semantic_scores) / len(semantic_scores)
        
        print("\n" + "="*60)
        print("EVALUATION RESULTS")
        print("="*60)
        print(f"Average Semantic Similarity: {avg_semantic_score:.4f}")
        print(f"Samples evaluated: {len(test_data)}")
        
        # Save results
        output_file = self.model_path / "evaluation_results.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump({
                "metrics": {
                    "avg_semantic_similarity": avg_semantic_score,
                    "num_samples": len(test_data)
                },
                "examples": results[:10]  # Save first 10 examples
            }, f, indent=2)
        
        print(f"\n✓ Results saved to {output_file}")
        
        # Show some examples
        print("\nExample outputs:")
        for i, result in enumerate(results[:3], 1):
            print(f"\n--- Example {i} ---")
            print(f"Instruction: {result['instruction'][:100]}...")
            print(f"Generated: {result['generated'][:200]}...")
            print(f"Semantic Score: {result['semantic_similarity']:.4f}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Evaluate trained model")
    parser.add_argument("--model", default="models/ats_lora_v1", help="Model directory")
    parser.add_argument("--test_data", default="feedback_db/training_pairs/val.jsonl", help="Test data file")
    
    args = parser.parse_args()
    
    evaluator = ModelEvaluator(args.model, args.test_data)
    evaluator.evaluate()
