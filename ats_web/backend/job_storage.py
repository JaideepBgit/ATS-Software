"""
Job Description Storage System
Manages job descriptions with unique IDs and persistent storage
"""
import json
import uuid
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional


class JobStorage:
    """Store and manage job descriptions with unique IDs"""
    
    def __init__(self, storage_dir: str = "data/jobs"):
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self.jobs_file = self.storage_dir / "jobs.jsonl"
        self.index_file = self.storage_dir / "jobs_index.json"
        self._ensure_files_exist()
    
    def _ensure_files_exist(self):
        """Create storage files if they don't exist"""
        if not self.jobs_file.exists():
            self.jobs_file.touch()
        
        if not self.index_file.exists():
            self._save_index({})
    
    def _load_index(self) -> Dict:
        """Load the jobs index"""
        try:
            with open(self.index_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    
    def _save_index(self, index: Dict):
        """Save the jobs index"""
        with open(self.index_file, 'w', encoding='utf-8') as f:
            json.dump(index, f, indent=2)
    
    def add_job(self, job_description: str, company_name: str = "", 
                role_name: str = "", metadata: Optional[Dict] = None) -> Dict:
        """Add a new job description
        
        Args:
            job_description: The job description text
            company_name: Company name
            role_name: Role/position name
            metadata: Additional metadata
            
        Returns:
            Dict with job_id and job details
        """
        # Generate unique ID
        job_id = str(uuid.uuid4())[:8]  # Short UUID
        timestamp = datetime.now().isoformat()
        
        # Create job record
        job_record = {
            "job_id": job_id,
            "company_name": company_name,
            "role_name": role_name,
            "job_description": job_description,
            "created_at": timestamp,
            "metadata": metadata or {},
            "analysis_count": 0
        }
        
        # Append to JSONL file
        with open(self.jobs_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(job_record) + '\n')
        
        # Update index
        index = self._load_index()
        index[job_id] = {
            "company_name": company_name,
            "role_name": role_name,
            "created_at": timestamp,
            "analysis_count": 0
        }
        self._save_index(index)
        
        return job_record
    
    def get_job(self, job_id: str) -> Optional[Dict]:
        """Get a job by ID
        
        Args:
            job_id: The job ID
            
        Returns:
            Job record or None if not found
        """
        try:
            with open(self.jobs_file, 'r', encoding='utf-8') as f:
                for line in f:
                    job = json.loads(line)
                    if job['job_id'] == job_id:
                        return job
        except:
            pass
        return None
    
    def list_jobs(self, limit: int = 50) -> List[Dict]:
        """List all jobs (most recent first)
        
        Args:
            limit: Maximum number of jobs to return
            
        Returns:
            List of job records (without full description)
        """
        jobs = []
        try:
            with open(self.jobs_file, 'r', encoding='utf-8') as f:
                for line in f:
                    job = json.loads(line)
                    # Return summary without full description
                    jobs.append({
                        "job_id": job['job_id'],
                        "company_name": job['company_name'],
                        "role_name": job['role_name'],
                        "created_at": job['created_at'],
                        "analysis_count": job.get('analysis_count', 0),
                        "description_preview": job['job_description'][:200] + "..."
                    })
        except:
            pass
        
        # Return most recent first
        return list(reversed(jobs))[:limit]
    
    def increment_analysis_count(self, job_id: str):
        """Increment the analysis count for a job"""
        index = self._load_index()
        if job_id in index:
            index[job_id]['analysis_count'] = index[job_id].get('analysis_count', 0) + 1
            self._save_index(index)
    
    def search_jobs(self, query: str) -> List[Dict]:
        """Search jobs by company or role name
        
        Args:
            query: Search query
            
        Returns:
            List of matching jobs
        """
        query_lower = query.lower()
        matching_jobs = []
        
        try:
            with open(self.jobs_file, 'r', encoding='utf-8') as f:
                for line in f:
                    job = json.loads(line)
                    if (query_lower in job['company_name'].lower() or 
                        query_lower in job['role_name'].lower()):
                        matching_jobs.append({
                            "job_id": job['job_id'],
                            "company_name": job['company_name'],
                            "role_name": job['role_name'],
                            "created_at": job['created_at'],
                            "description_preview": job['job_description'][:200] + "..."
                        })
        except:
            pass
        
        return list(reversed(matching_jobs))
    
    def delete_job(self, job_id: str) -> bool:
        """Delete a job (soft delete by marking)
        
        Args:
            job_id: The job ID
            
        Returns:
            True if deleted, False otherwise
        """
        # For now, just remove from index
        index = self._load_index()
        if job_id in index:
            del index[job_id]
            self._save_index(index)
            return True
        return False
