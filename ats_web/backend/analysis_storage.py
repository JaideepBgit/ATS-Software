"""
Analysis Storage System
Manages resume analysis results linked to job IDs
"""
import json
import uuid
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional


class AnalysisStorage:
    """Store and manage analysis results"""
    
    def __init__(self, storage_dir: str = "data/analyses"):
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self.analyses_file = self.storage_dir / "analyses.jsonl"
        self.index_file = self.storage_dir / "analyses_index.json"
        self._ensure_files_exist()
    
    def _ensure_files_exist(self):
        """Create storage files if they don't exist"""
        if not self.analyses_file.exists():
            self.analyses_file.touch()
        
        if not self.index_file.exists():
            self._save_index({})
    
    def _load_index(self) -> Dict:
        """Load the analyses index"""
        try:
            with open(self.index_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    
    def _save_index(self, index: Dict):
        """Save the analyses index"""
        with open(self.index_file, 'w', encoding='utf-8') as f:
            json.dump(index, f, indent=2)
    
    def save_analysis(self, job_id: str, resume_id: str, 
                     analysis_result: Dict, candidate_name: str = "") -> Dict:
        """Save an analysis result
        
        Args:
            job_id: The job ID this analysis is for
            resume_id: The resume ID being analyzed
            analysis_result: The analysis result from ATS service
            candidate_name: Candidate name
            
        Returns:
            Dict with analysis_id and details
        """
        # Generate unique ID
        analysis_id = str(uuid.uuid4())[:12]
        timestamp = datetime.now().isoformat()
        
        # Create analysis record
        analysis_record = {
            "analysis_id": analysis_id,
            "job_id": job_id,
            "resume_id": resume_id,
            "candidate_name": candidate_name,
            "created_at": timestamp,
            "overall_score": analysis_result.get('overall_score', 0),
            "hiring_recommendation": analysis_result.get('hiring_recommendation', ''),
            "analysis_result": analysis_result,
            "feedback_count": 0
        }
        
        # Append to JSONL file
        with open(self.analyses_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(analysis_record) + '\n')
        
        # Update index
        index = self._load_index()
        index[analysis_id] = {
            "job_id": job_id,
            "resume_id": resume_id,
            "candidate_name": candidate_name,
            "created_at": timestamp,
            "overall_score": analysis_result.get('overall_score', 0),
            "feedback_count": 0
        }
        self._save_index(index)
        
        return analysis_record
    
    def get_analysis(self, analysis_id: str) -> Optional[Dict]:
        """Get an analysis by ID
        
        Args:
            analysis_id: The analysis ID
            
        Returns:
            Analysis record or None if not found
        """
        try:
            with open(self.analyses_file, 'r', encoding='utf-8') as f:
                for line in f:
                    analysis = json.loads(line)
                    if analysis['analysis_id'] == analysis_id:
                        return analysis
        except:
            pass
        return None
    
    def list_analyses(self, job_id: Optional[str] = None, 
                     limit: int = 50) -> List[Dict]:
        """List analyses (optionally filtered by job_id)
        
        Args:
            job_id: Optional job ID to filter by
            limit: Maximum number of analyses to return
            
        Returns:
            List of analysis records (summary only)
        """
        analyses = []
        try:
            with open(self.analyses_file, 'r', encoding='utf-8') as f:
                for line in f:
                    analysis = json.loads(line)
                    
                    # Filter by job_id if provided
                    if job_id and analysis['job_id'] != job_id:
                        continue
                    
                    # Return summary without full analysis
                    analyses.append({
                        "analysis_id": analysis['analysis_id'],
                        "job_id": analysis['job_id'],
                        "resume_id": analysis['resume_id'],
                        "candidate_name": analysis['candidate_name'],
                        "created_at": analysis['created_at'],
                        "overall_score": analysis['overall_score'],
                        "hiring_recommendation": analysis['hiring_recommendation'],
                        "feedback_count": analysis.get('feedback_count', 0)
                    })
        except:
            pass
        
        # Return most recent first
        analyses.sort(key=lambda x: x['created_at'], reverse=True)
        return analyses[:limit]
    
    def increment_feedback_count(self, analysis_id: str):
        """Increment the feedback count for an analysis"""
        index = self._load_index()
        if analysis_id in index:
            index[analysis_id]['feedback_count'] = index[analysis_id].get('feedback_count', 0) + 1
            self._save_index(index)
    
    def get_analyses_by_job(self, job_id: str) -> List[Dict]:
        """Get all analyses for a specific job
        
        Args:
            job_id: The job ID
            
        Returns:
            List of analysis records
        """
        return self.list_analyses(job_id=job_id, limit=1000)
    
    def delete_analysis(self, analysis_id: str) -> bool:
        """Delete an analysis (soft delete by removing from index)
        
        Args:
            analysis_id: The analysis ID
            
        Returns:
            True if deleted, False otherwise
        """
        index = self._load_index()
        if analysis_id in index:
            del index[analysis_id]
            self._save_index(index)
            return True
        return False
