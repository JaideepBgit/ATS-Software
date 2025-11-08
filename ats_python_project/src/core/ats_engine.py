"""
Core ATS Engine for managing candidates, jobs, and applications
"""
import uuid
from datetime import datetime
from typing import List, Optional, Dict, Any, Tuple
from pathlib import Path
import asyncio
from loguru import logger

from models.ats_models import (
    Candidate, JobPosting, Application, MatchScore, 
    ApplicationStatus, JobStatus, SearchFilters, ATSStats
)
from services.lm_studio_service import LMStudioService
from services.document_processor import DocumentProcessor
from utils.matching_algorithms import MatchingAlgorithms
from utils.database_manager import DatabaseManager


class ATSEngine:
    """Core ATS Engine for managing the entire recruitment process"""
    
    def __init__(self):
        self.document_processor = DocumentProcessor()
        self.matching_algorithms = MatchingAlgorithms()
        self.db_manager = DatabaseManager()
        
    async def initialize(self):
        """Initialize the ATS engine"""
        await self.db_manager.initialize()
        logger.info("ATS Engine initialized successfully")
    
    # Candidate Management
    async def add_candidate_from_resume(self, resume_file_path: str) -> Optional[Candidate]:
        """Add a new candidate from resume file"""
        try:
            # Extract text from resume
            resume_text = self.document_processor.extract_text(resume_file_path)
            if not resume_text:
                logger.error(f"Could not extract text from resume: {resume_file_path}")
                return None
            
            # Extract contact information
            contact_info = self.document_processor.extract_contact_info(resume_text)
            
            # Extract education
            education_data = self.document_processor.extract_education(resume_text)
            
            # Extract years of experience
            years_exp = self.document_processor.extract_experience_years(resume_text)
            
            # Use LM Studio to extract skills
            async with LMStudioService() as lm_service:
                skills = await lm_service.extract_resume_skills(resume_text)
            
            # Create candidate (we'll need to get name from user input or extract it)
            candidate = Candidate(
                id=str(uuid.uuid4()),
                first_name="Unknown",  # This should be extracted or provided
                last_name="Candidate",
                contact_info=contact_info,
                resume_text=resume_text,
                resume_file_path=resume_file_path,
                skills=skills,
                years_of_experience=years_exp
            )
            
            # Save to database
            await self.db_manager.save_candidate(candidate)
            logger.info(f"Added new candidate: {candidate.id}")
            
            return candidate
            
        except Exception as e:
            logger.error(f"Error adding candidate from resume: {str(e)}")
            return None
    
    async def get_candidate(self, candidate_id: str) -> Optional[Candidate]:
        """Get candidate by ID"""
        return await self.db_manager.get_candidate(candidate_id)
    
    async def search_candidates(self, filters: SearchFilters) -> List[Candidate]:
        """Search candidates with filters"""
        return await self.db_manager.search_candidates(filters)
    
    async def update_candidate(self, candidate: Candidate) -> bool:
        """Update candidate information"""
        candidate.updated_at = datetime.now()
        return await self.db_manager.update_candidate(candidate)
    
    # Job Management
    async def create_job_posting(self, job_data: Dict[str, Any]) -> JobPosting:
        """Create a new job posting"""
        job = JobPosting(
            id=str(uuid.uuid4()),
            **job_data
        )
        
        await self.db_manager.save_job_posting(job)
        logger.info(f"Created new job posting: {job.id} - {job.title}")
        
        return job
    
    async def get_job_posting(self, job_id: str) -> Optional[JobPosting]:
        """Get job posting by ID"""
        return await self.db_manager.get_job_posting(job_id)
    
    async def search_job_postings(self, filters: SearchFilters) -> List[JobPosting]:
        """Search job postings with filters"""
        return await self.db_manager.search_job_postings(filters)
    
    async def update_job_posting(self, job: JobPosting) -> bool:
        """Update job posting"""
        job.updated_at = datetime.now()
        return await self.db_manager.update_job_posting(job)
    
    # Application Management
    async def create_application(
        self, 
        candidate_id: str, 
        job_id: str, 
        cover_letter: Optional[str] = None
    ) -> Optional[Application]:
        """Create a new job application"""
        try:
            # Get candidate and job
            candidate = await self.get_candidate(candidate_id)
            job = await self.get_job_posting(job_id)
            
            if not candidate or not job:
                logger.error("Candidate or job not found")
                return None
            
            # Calculate match score
            match_score = await self.calculate_match_score(candidate, job)
            
            # Generate interview questions
            async with LMStudioService() as lm_service:
                interview_questions = await lm_service.generate_interview_questions(
                    candidate.resume_text or "",
                    job.description
                )
            
            # Create application
            application = Application(
                id=str(uuid.uuid4()),
                candidate_id=candidate_id,
                job_id=job_id,
                match_score=match_score,
                cover_letter=cover_letter,
                interview_questions=interview_questions
            )
            
            # Save to database
            await self.db_manager.save_application(application)
            logger.info(f"Created application: {application.id}")
            
            return application
            
        except Exception as e:
            logger.error(f"Error creating application: {str(e)}")
            return None
    
    async def get_application(self, application_id: str) -> Optional[Application]:
        """Get application by ID"""
        return await self.db_manager.get_application(application_id)
    
    async def get_applications_for_job(self, job_id: str) -> List[Application]:
        """Get all applications for a specific job"""
        return await self.db_manager.get_applications_for_job(job_id)
    
    async def get_applications_for_candidate(self, candidate_id: str) -> List[Application]:
        """Get all applications for a specific candidate"""
        return await self.db_manager.get_applications_for_candidate(candidate_id)
    
    async def update_application_status(
        self, 
        application_id: str, 
        status: ApplicationStatus,
        notes: Optional[str] = None
    ) -> bool:
        """Update application status"""
        application = await self.get_application(application_id)
        if not application:
            return False
        
        application.status = status
        application.updated_at = datetime.now()
        if notes:
            application.review_notes = notes
        
        return await self.db_manager.update_application(application)
    
    # Matching and Scoring
    async def calculate_match_score(
        self, 
        candidate: Candidate, 
        job: JobPosting
    ) -> MatchScore:
        """Calculate comprehensive match score between candidate and job"""
        try:
            # Use LM Studio for AI-powered matching
            async with LMStudioService() as lm_service:
                ai_analysis = await lm_service.calculate_job_match_score(
                    candidate.resume_text or "",
                    job.description
                )
            
            if ai_analysis:
                return MatchScore(**ai_analysis)
            
            # Fallback to rule-based matching
            return self.matching_algorithms.calculate_basic_match_score(candidate, job)
            
        except Exception as e:
            logger.error(f"Error calculating match score: {str(e)}")
            return MatchScore(overall_score=0)
    
    async def find_best_candidates_for_job(
        self, 
        job_id: str, 
        limit: int = 10
    ) -> List[Tuple[Candidate, MatchScore]]:
        """Find best matching candidates for a job"""
        job = await self.get_job_posting(job_id)
        if not job:
            return []
        
        # Get all candidates
        all_candidates = await self.search_candidates(SearchFilters())
        
        # Calculate match scores
        candidate_scores = []
        for candidate in all_candidates:
            match_score = await self.calculate_match_score(candidate, job)
            candidate_scores.append((candidate, match_score))
        
        # Sort by overall score and return top candidates
        candidate_scores.sort(key=lambda x: x[1].overall_score, reverse=True)
        return candidate_scores[:limit]
    
    async def find_best_jobs_for_candidate(
        self, 
        candidate_id: str, 
        limit: int = 10
    ) -> List[Tuple[JobPosting, MatchScore]]:
        """Find best matching jobs for a candidate"""
        candidate = await self.get_candidate(candidate_id)
        if not candidate:
            return []
        
        # Get active job postings
        active_jobs = await self.search_job_postings(
            SearchFilters(status=JobStatus.ACTIVE.value)
        )
        
        # Calculate match scores
        job_scores = []
        for job in active_jobs:
            match_score = await self.calculate_match_score(candidate, job)
            job_scores.append((job, match_score))
        
        # Sort by overall score and return top jobs
        job_scores.sort(key=lambda x: x[1].overall_score, reverse=True)
        return job_scores[:limit]
    
    # Bulk Operations
    async def bulk_process_resumes(
        self, 
        resume_directory: str, 
        job_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Process multiple resumes from a directory"""
        results = {
            "processed": 0,
            "successful": 0,
            "failed": 0,
            "candidates": [],
            "applications": []
        }
        
        resume_dir = Path(resume_directory)
        if not resume_dir.exists():
            logger.error(f"Directory not found: {resume_directory}")
            return results
        
        # Get all resume files
        resume_files = []
        for ext in self.document_processor.allowed_extensions:
            resume_files.extend(resume_dir.glob(f"*.{ext}"))
        
        logger.info(f"Found {len(resume_files)} resume files to process")
        
        for resume_file in resume_files:
            results["processed"] += 1
            
            try:
                # Add candidate from resume
                candidate = await self.add_candidate_from_resume(str(resume_file))
                
                if candidate:
                    results["successful"] += 1
                    results["candidates"].append(candidate.id)
                    
                    # Create application if job_id provided
                    if job_id:
                        application = await self.create_application(candidate.id, job_id)
                        if application:
                            results["applications"].append(application.id)
                else:
                    results["failed"] += 1
                    
            except Exception as e:
                logger.error(f"Error processing resume {resume_file}: {str(e)}")
                results["failed"] += 1
        
        logger.info(f"Bulk processing completed: {results}")
        return results
    
    # Analytics and Statistics
    async def get_ats_statistics(self) -> ATSStats:
        """Get comprehensive ATS statistics"""
        try:
            stats = ATSStats()
            
            # Get basic counts
            stats.total_candidates = await self.db_manager.count_candidates()
            stats.total_jobs = await self.db_manager.count_job_postings()
            stats.total_applications = await self.db_manager.count_applications()
            
            # Get active jobs count
            active_jobs = await self.search_job_postings(
                SearchFilters(status=JobStatus.ACTIVE.value)
            )
            stats.active_jobs = len(active_jobs)
            
            # Get applications this month
            stats.applications_this_month = await self.db_manager.count_applications_this_month()
            
            # Calculate average match score
            stats.avg_match_score = await self.db_manager.get_average_match_score()
            
            # Get top skills
            stats.top_skills = await self.db_manager.get_top_skills()
            
            return stats
            
        except Exception as e:
            logger.error(f"Error getting ATS statistics: {str(e)}")
            return ATSStats()
    
    async def cleanup(self):
        """Cleanup resources"""
        await self.db_manager.cleanup()
        logger.info("ATS Engine cleanup completed")
