"""RAG service using feedback database + Ollama"""

from feedback_store import feedback_store
from typing import List, Dict

class RAGService:
    def __init__(self):
        self.feedback_store = feedback_store
    
    def get_relevant_examples(self, query: str, min_rating: int = 4, n_results: int = 3) -> List[Dict]:
        """Get relevant high-quality examples from feedback"""
        results = self.feedback_store.search_similar_chromadb(
            query=query,
            n_results=n_results,
            min_rating=min_rating
        )
        
        if 'error' in results or not results.get('documents'):
            return []
        
        examples = []
        for doc, metadata in zip(results['documents'][0], results['metadatas'][0]):
            examples.append({
                'query': metadata['query'],
                'response': metadata['response'],
                'rating': metadata['rating']
            })
        
        return examples
    
    def build_rag_prompt(self, query: str, context: Dict, examples: List[Dict]) -> str:
        """Build enhanced prompt with examples from feedback"""
        
        # Start with examples
        prompt = "Here are some examples of good responses:\n\n"
        
        for i, example in enumerate(examples, 1):
            prompt += f"Example {i}:\n"
            prompt += f"Question: {example['query']}\n"
            prompt += f"Answer: {example['response']}\n\n"
        
        # Add current context
        prompt += "Now answer this question using the same style and accuracy:\n\n"
        prompt += f"Candidate: {context.get('candidate_name', 'Unknown')}\n"
        prompt += f"Overall Score: {context.get('overall_score', 0)}%\n"
        prompt += f"Question: {query}\n\n"
        prompt += "Answer:"
        
        return prompt
    
    def ask_with_rag(self, query: str, context: Dict, llm_service) -> str:
        """Ask question with RAG enhancement"""
        
        # Get relevant examples
        examples = self.get_relevant_examples(query, min_rating=4, n_results=3)
        
        if examples:
            # Use RAG-enhanced prompt
            enhanced_prompt = self.build_rag_prompt(query, context, examples)
            response = llm_service.call_llm(enhanced_prompt, temperature=0.3)
        else:
            # Fallback to normal question
            response = llm_service.ask_question(query, context)
        
        return response


# Global instance
rag_service = RAGService()
