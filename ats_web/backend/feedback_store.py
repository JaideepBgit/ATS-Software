"""Feedback storage using ChromaDB and FAISS"""

import json
import os
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional
import numpy as np

# ChromaDB
try:
    import chromadb
    from chromadb.config import Settings
    CHROMADB_AVAILABLE = True
except ImportError:
    CHROMADB_AVAILABLE = False
    print("Warning: ChromaDB not installed. Install with: pip install chromadb")

# FAISS
try:
    import faiss
    FAISS_AVAILABLE = True
except ImportError:
    FAISS_AVAILABLE = False
    print("Warning: FAISS not installed. Install with: pip install faiss-cpu")

# Sentence Transformers for embeddings
try:
    from sentence_transformers import SentenceTransformer
    EMBEDDINGS_AVAILABLE = True
except ImportError:
    EMBEDDINGS_AVAILABLE = False
    print("Warning: sentence-transformers not installed. Install with: pip install sentence-transformers")


class FeedbackStore:
    def __init__(self, db_path: str = "feedback_db"):
        self.db_path = Path(db_path)
        self.db_path.mkdir(exist_ok=True)
        
        # Initialize embedding model
        if EMBEDDINGS_AVAILABLE:
            self.embedding_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
            self.embedding_dim = 384
        else:
            self.embedding_model = None
            self.embedding_dim = None
        
        # Initialize ChromaDB
        self.chroma_client = None
        self.chroma_collection = None
        if CHROMADB_AVAILABLE and EMBEDDINGS_AVAILABLE:
            try:
                self.chroma_client = chromadb.PersistentClient(
                    path=str(self.db_path / "chroma")
                )
                self.chroma_collection = self.chroma_client.get_or_create_collection(
                    name="ats_feedback",
                    metadata={"hnsw:space": "cosine"}
                )
                print("✓ ChromaDB initialized")
            except Exception as e:
                print(f"Warning: ChromaDB initialization failed: {e}")
        
        # Initialize FAISS
        self.faiss_index = None
        self.faiss_id_map = []
        if FAISS_AVAILABLE and EMBEDDINGS_AVAILABLE:
            try:
                self._init_faiss()
                print("✓ FAISS initialized")
            except Exception as e:
                print(f"Warning: FAISS initialization failed: {e}")
        
        # JSONL backup
        self.jsonl_file = self.db_path / "interactions.jsonl"
    
    def _init_faiss(self):
        """Initialize or load FAISS index"""
        faiss_index_file = self.db_path / "faiss_index.bin"
        faiss_map_file = self.db_path / "faiss_id_map.json"
        
        if faiss_index_file.exists() and faiss_map_file.exists():
            # Load existing index
            self.faiss_index = faiss.read_index(str(faiss_index_file))
            with open(faiss_map_file, 'r') as f:
                self.faiss_id_map = json.load(f)
        else:
            # Create new index
            self.faiss_index = faiss.IndexFlatL2(self.embedding_dim)
            self.faiss_id_map = []
    
    def _save_faiss(self):
        """Save FAISS index to disk"""
        if self.faiss_index is not None:
            faiss_index_file = self.db_path / "faiss_index.bin"
            faiss_map_file = self.db_path / "faiss_id_map.json"
            
            faiss.write_index(self.faiss_index, str(faiss_index_file))
            with open(faiss_map_file, 'w') as f:
                json.dump(self.faiss_id_map, f)
    
    def add_feedback(
        self,
        interaction_id: str,
        query: str,
        context: List[str],
        response: str,
        rating: int,
        correct_points: List[str],
        incorrect_points: List[str],
        missing_points: List[str],
        ideal_response: str,
        analysis_id: Optional[str] = None,
        job_id: Optional[str] = None
    ) -> Dict:
        """Add feedback to all storage systems"""
        
        feedback_data = {
            "id": interaction_id,
            "timestamp": datetime.now().isoformat(),
            "query": query,
            "context": context,
            "response": response,
            "analysis_id": analysis_id,
            "job_id": job_id,
            "feedback": {
                "rating": rating,
                "correct_points": correct_points,
                "incorrect_points": incorrect_points,
                "missing_points": missing_points,
                "ideal_response": ideal_response
            }
        }
        
        # Generate embeddings
        if self.embedding_model:
            text_for_embedding = f"Query: {query}\nResponse: {response}"
            embedding = self.embedding_model.encode(text_for_embedding)
            feedback_data["embedding"] = embedding.tolist()
        else:
            embedding = None
        
        # Save to JSONL (always works)
        with open(self.jsonl_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(feedback_data) + '\n')
        
        # Save to ChromaDB
        if self.chroma_collection and embedding is not None:
            try:
                metadata = {
                    "rating": rating,
                    "query": query,
                    "response": response,
                    "timestamp": feedback_data["timestamp"],
                    "num_correct": len(correct_points),
                    "num_incorrect": len(incorrect_points)
                }
                if analysis_id:
                    metadata["analysis_id"] = analysis_id
                if job_id:
                    metadata["job_id"] = job_id
                
                self.chroma_collection.add(
                    ids=[interaction_id],
                    embeddings=[embedding.tolist()],
                    documents=[text_for_embedding],
                    metadatas=[metadata]
                )
            except Exception as e:
                print(f"ChromaDB save error: {e}")
        
        # Save to FAISS
        if self.faiss_index is not None and embedding is not None:
            try:
                self.faiss_index.add(np.array([embedding], dtype=np.float32))
                self.faiss_id_map.append(interaction_id)
                self._save_faiss()
            except Exception as e:
                print(f"FAISS save error: {e}")
        
        return feedback_data
    
    def search_similar_chromadb(
        self,
        query: str,
        n_results: int = 5,
        min_rating: Optional[int] = None
    ) -> Dict:
        """Search for similar feedback using ChromaDB"""
        if not self.chroma_collection or not self.embedding_model:
            return {"error": "ChromaDB not available"}
        
        try:
            query_embedding = self.embedding_model.encode(query).tolist()
            
            where_filter = None
            if min_rating is not None:
                where_filter = {"rating": {"$gte": min_rating}}
            
            results = self.chroma_collection.query(
                query_embeddings=[query_embedding],
                n_results=n_results,
                where=where_filter
            )
            
            return results
        except Exception as e:
            return {"error": str(e)}
    
    def search_similar_faiss(
        self,
        query: str,
        k: int = 5
    ) -> List[Dict]:
        """Search for similar feedback using FAISS"""
        if not self.faiss_index or not self.embedding_model:
            return []
        
        try:
            query_embedding = self.embedding_model.encode(query)
            query_embedding = np.array([query_embedding], dtype=np.float32)
            
            distances, indices = self.faiss_index.search(query_embedding, k)
            
            results = []
            for dist, idx in zip(distances[0], indices[0]):
                if idx < len(self.faiss_id_map):
                    results.append({
                        "id": self.faiss_id_map[idx],
                        "distance": float(dist)
                    })
            
            return results
        except Exception as e:
            print(f"FAISS search error: {e}")
            return []
    
    def get_statistics(self) -> Dict:
        """Get feedback statistics"""
        stats = {
            "total_feedback": 0,
            "average_rating": 0.0,
            "chromadb_count": 0,
            "faiss_count": 0
        }
        
        # Count from JSONL
        if self.jsonl_file.exists():
            ratings = []
            with open(self.jsonl_file, 'r', encoding='utf-8') as f:
                for line in f:
                    data = json.loads(line)
                    ratings.append(data["feedback"]["rating"])
            
            stats["total_feedback"] = len(ratings)
            stats["average_rating"] = sum(ratings) / len(ratings) if ratings else 0.0
        
        # ChromaDB count
        if self.chroma_collection:
            try:
                stats["chromadb_count"] = self.chroma_collection.count()
            except:
                pass
        
        # FAISS count
        if self.faiss_index:
            stats["faiss_count"] = self.faiss_index.ntotal
        
        return stats
    
    def get_high_quality_samples(
        self,
        min_rating: int = 4,
        limit: int = 100
    ) -> List[Dict]:
        """Get high-quality feedback samples for training"""
        if not self.chroma_collection:
            return []
        
        try:
            results = self.chroma_collection.get(
                where={"rating": {"$gte": min_rating}},
                limit=limit
            )
            return results
        except Exception as e:
            print(f"Error getting high-quality samples: {e}")
            return []


# Global instance
feedback_store = FeedbackStore()
