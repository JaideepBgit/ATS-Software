"""
Resume Storage System
Manages uploaded resumes with persistent storage
"""
import json
import hashlib
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional


class ResumeStorage:
    """Store and manage uploaded resumes"""
    
    def __init__(self, storage_dir: str = "data/resumes"):
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self.pdfs_dir = self.storage_dir / "pdfs"
        self.pdfs_dir.mkdir(exist_ok=True)
        self.texts_dir = self.storage_dir / "texts"
        self.texts_dir.mkdir(exist_ok=True)
        self.index_file = self.storage_dir / "resumes_index.json"
        self._ensure_files_exist()
    
    def _ensure_files_exist(self):
        """Create storage files if they don't exist"""
        if not self.index_file.exists():
            self._save_index({})
    
    def _load_index(self) -> Dict:
        """Load the resumes index"""
        try:
            with open(self.index_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    
    def _save_index(self, index: Dict):
        """Save the resumes index"""
        with open(self.index_file, 'w', encoding='utf-8') as f:
            json.dump(index, f, indent=2)
    
    def _compute_hash(self, content: bytes) -> str:
        """Compute SHA256 hash of content"""
        return hashlib.sha256(content).hexdigest()[:16]
    
    def save_resume(self, pdf_bytes: bytes, resume_text: str, 
                   filename: str, candidate_name: str = "") -> Dict:
        """Save a resume (PDF and extracted text)
        
        Args:
            pdf_bytes: PDF file bytes
            resume_text: Extracted text from PDF
            filename: Original filename
            candidate_name: Candidate name (optional)
            
        Returns:
            Dict with resume_id and details
        """
        # Generate unique ID based on content hash
        content_hash = self._compute_hash(pdf_bytes)
        resume_id = f"resume_{content_hash}"
        timestamp = datetime.now().isoformat()
        
        # Save PDF
        pdf_path = self.pdfs_dir / f"{resume_id}.pdf"
        with open(pdf_path, 'wb') as f:
            f.write(pdf_bytes)
        
        # Save text
        text_path = self.texts_dir / f"{resume_id}.txt"
        with open(text_path, 'w', encoding='utf-8') as f:
            f.write(resume_text)
        
        # Create resume record
        resume_record = {
            "resume_id": resume_id,
            "candidate_name": candidate_name,
            "original_filename": filename,
            "pdf_path": str(pdf_path),
            "text_path": str(text_path),
            "uploaded_at": timestamp,
            "file_size": len(pdf_bytes),
            "text_length": len(resume_text)
        }
        
        # Update index
        index = self._load_index()
        index[resume_id] = resume_record
        self._save_index(index)
        
        return resume_record
    
    def get_resume(self, resume_id: str) -> Optional[Dict]:
        """Get resume metadata by ID
        
        Args:
            resume_id: The resume ID
            
        Returns:
            Resume record or None if not found
        """
        index = self._load_index()
        return index.get(resume_id)
    
    def get_resume_text(self, resume_id: str) -> Optional[str]:
        """Get resume text by ID
        
        Args:
            resume_id: The resume ID
            
        Returns:
            Resume text or None if not found
        """
        resume = self.get_resume(resume_id)
        if not resume:
            return None
        
        try:
            text_path = Path(resume['text_path'])
            with open(text_path, 'r', encoding='utf-8') as f:
                return f.read()
        except:
            return None
    
    def get_resume_pdf(self, resume_id: str) -> Optional[bytes]:
        """Get resume PDF bytes by ID
        
        Args:
            resume_id: The resume ID
            
        Returns:
            PDF bytes or None if not found
        """
        resume = self.get_resume(resume_id)
        if not resume:
            return None
        
        try:
            pdf_path = Path(resume['pdf_path'])
            with open(pdf_path, 'rb') as f:
                return f.read()
        except:
            return None
    
    def list_resumes(self, limit: int = 50) -> List[Dict]:
        """List all resumes (most recent first)
        
        Args:
            limit: Maximum number of resumes to return
            
        Returns:
            List of resume records
        """
        index = self._load_index()
        resumes = list(index.values())
        
        # Sort by upload date (most recent first)
        resumes.sort(key=lambda x: x['uploaded_at'], reverse=True)
        
        return resumes[:limit]
    
    def delete_resume(self, resume_id: str) -> bool:
        """Delete a resume
        
        Args:
            resume_id: The resume ID
            
        Returns:
            True if deleted, False otherwise
        """
        resume = self.get_resume(resume_id)
        if not resume:
            return False
        
        try:
            # Delete files
            pdf_path = Path(resume['pdf_path'])
            text_path = Path(resume['text_path'])
            
            if pdf_path.exists():
                pdf_path.unlink()
            if text_path.exists():
                text_path.unlink()
            
            # Remove from index
            index = self._load_index()
            del index[resume_id]
            self._save_index(index)
            
            return True
        except:
            return False
