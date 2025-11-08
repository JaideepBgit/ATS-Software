"""
Database manager for ATS data persistence
"""
import sqlite3
import json
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
from pathlib import Path
import aiosqlite
from loguru import logger

from models.ats_models import (
    Candidate, JobPosting, Application, SearchFilters,
    ApplicationStatus, JobStatus
)


class DatabaseManager:
    """Manages database operations for the ATS system"""
    
    def __init__(self, db_path: str = "ats_database.db"):
        self.db_path = db_path
        self.db_initialized = False
    
    async def initialize(self):
        """Initialize the database with required tables"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                # Create candidates table
                await db.execute("""
                    CREATE TABLE IF NOT EXISTS candidates (
                        id TEXT PRIMARY KEY,
                        first_name TEXT NOT NULL,
                        last_name TEXT NOT NULL,
                        email TEXT,
                        phone TEXT,
                        linkedin TEXT,
                        github TEXT,
                        website TEXT,
                        resume_text TEXT,
                        resume_file_path TEXT,
                        skills TEXT,  -- JSON array
                        education TEXT,  -- JSON array
                        experience TEXT,  -- JSON array
                        years_of_experience INTEGER,
                        created_at TIMESTAMP,
                        updated_at TIMESTAMP
                    )
                """)
                
                # Create job_postings table
                await db.execute("""
                    CREATE TABLE IF NOT EXISTS job_postings (
                        id TEXT PRIMARY KEY,
                        title TEXT NOT NULL,
                        company TEXT NOT NULL,
                        department TEXT,
                        location TEXT NOT NULL,
                        job_type TEXT DEFAULT 'full-time',
                        salary_min REAL,
                        salary_max REAL,
                        description TEXT NOT NULL,
                        requirements TEXT,  -- JSON array
                        preferred_qualifications TEXT,  -- JSON array
                        required_skills TEXT,  -- JSON array
                        preferred_skills TEXT,  -- JSON array
                        status TEXT DEFAULT 'draft',
                        created_at TIMESTAMP,
                        updated_at TIMESTAMP,
                        posted_date TIMESTAMP,
                        closing_date TIMESTAMP
                    )
                """)
                
                # Create applications table
                await db.execute("""
                    CREATE TABLE IF NOT EXISTS applications (
                        id TEXT PRIMARY KEY,
                        candidate_id TEXT NOT NULL,
                        job_id TEXT NOT NULL,
                        status TEXT DEFAULT 'submitted',
                        match_score_data TEXT,  -- JSON object
                        cover_letter TEXT,
                        interview_notes TEXT,
                        interview_questions TEXT,  -- JSON array
                        applied_at TIMESTAMP,
                        updated_at TIMESTAMP,
                        reviewed_by TEXT,
                        review_notes TEXT,
                        FOREIGN KEY (candidate_id) REFERENCES candidates (id),
                        FOREIGN KEY (job_id) REFERENCES job_postings (id)
                    )
                """)
                
                # Create indexes for better performance
                await db.execute("CREATE INDEX IF NOT EXISTS idx_candidates_email ON candidates (email)")
                await db.execute("CREATE INDEX IF NOT EXISTS idx_applications_candidate ON applications (candidate_id)")
                await db.execute("CREATE INDEX IF NOT EXISTS idx_applications_job ON applications (job_id)")
                await db.execute("CREATE INDEX IF NOT EXISTS idx_applications_status ON applications (status)")
                await db.execute("CREATE INDEX IF NOT EXISTS idx_jobs_status ON job_postings (status)")
                
                await db.commit()
                
            self.db_initialized = True
            logger.info("Database initialized successfully")
            
        except Exception as e:
            logger.error(f"Error initializing database: {str(e)}")
            raise
    
    # Candidate operations
    async def save_candidate(self, candidate: Candidate) -> bool:
        """Save candidate to database"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                await db.execute("""
                    INSERT OR REPLACE INTO candidates (
                        id, first_name, last_name, email, phone, linkedin, github, website,
                        resume_text, resume_file_path, skills, education, experience,
                        years_of_experience, created_at, updated_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    candidate.id,
                    candidate.first_name,
                    candidate.last_name,
                    candidate.contact_info.email,
                    candidate.contact_info.phone,
                    candidate.contact_info.linkedin,
                    candidate.contact_info.github,
                    candidate.contact_info.website,
                    candidate.resume_text,
                    candidate.resume_file_path,
                    json.dumps(candidate.skills),
                    json.dumps([edu.dict() for edu in candidate.education]),
                    json.dumps([exp.dict() for exp in candidate.experience]),
                    candidate.years_of_experience,
                    candidate.created_at.isoformat(),
                    candidate.updated_at.isoformat()
                ))
                await db.commit()
                return True
                
        except Exception as e:
            logger.error(f"Error saving candidate: {str(e)}")
            return False
    
    async def get_candidate(self, candidate_id: str) -> Optional[Candidate]:
        """Get candidate by ID"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                db.row_factory = aiosqlite.Row
                cursor = await db.execute(
                    "SELECT * FROM candidates WHERE id = ?", (candidate_id,)
                )
                row = await cursor.fetchone()
                
                if row:
                    return self._row_to_candidate(row)
                return None
                
        except Exception as e:
            logger.error(f"Error getting candidate: {str(e)}")
            return None
    
    async def search_candidates(self, filters: SearchFilters) -> List[Candidate]:
        """Search candidates with filters"""
        try:
            query = "SELECT * FROM candidates WHERE 1=1"
            params = []
            
            if filters.skills:
                # Search for candidates with any of the specified skills
                skill_conditions = []
                for skill in filters.skills:
                    skill_conditions.append("skills LIKE ?")
                    params.append(f"%{skill}%")
                query += f" AND ({' OR '.join(skill_conditions)})"
            
            if filters.experience_min is not None:
                query += " AND years_of_experience >= ?"
                params.append(filters.experience_min)
            
            if filters.experience_max is not None:
                query += " AND years_of_experience <= ?"
                params.append(filters.experience_max)
            
            query += " ORDER BY updated_at DESC"
            
            async with aiosqlite.connect(self.db_path) as db:
                db.row_factory = aiosqlite.Row
                cursor = await db.execute(query, params)
                rows = await cursor.fetchall()
                
                return [self._row_to_candidate(row) for row in rows]
                
        except Exception as e:
            logger.error(f"Error searching candidates: {str(e)}")
            return []
    
    async def update_candidate(self, candidate: Candidate) -> bool:
        """Update candidate"""
        return await self.save_candidate(candidate)
    
    async def count_candidates(self) -> int:
        """Count total candidates"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                cursor = await db.execute("SELECT COUNT(*) FROM candidates")
                result = await cursor.fetchone()
                return result[0] if result else 0
        except Exception as e:
            logger.error(f"Error counting candidates: {str(e)}")
            return 0
    
    # Job posting operations
    async def save_job_posting(self, job: JobPosting) -> bool:
        """Save job posting to database"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                await db.execute("""
                    INSERT OR REPLACE INTO job_postings (
                        id, title, company, department, location, job_type,
                        salary_min, salary_max, description, requirements,
                        preferred_qualifications, required_skills, preferred_skills,
                        status, created_at, updated_at, posted_date, closing_date
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    job.id,
                    job.title,
                    job.company,
                    job.department,
                    job.location,
                    job.job_type,
                    job.salary_min,
                    job.salary_max,
                    job.description,
                    json.dumps(job.requirements),
                    json.dumps(job.preferred_qualifications),
                    json.dumps(job.required_skills),
                    json.dumps(job.preferred_skills),
                    job.status.value,
                    job.created_at.isoformat(),
                    job.updated_at.isoformat(),
                    job.posted_date.isoformat() if job.posted_date else None,
                    job.closing_date.isoformat() if job.closing_date else None
                ))
                await db.commit()
                return True
                
        except Exception as e:
            logger.error(f"Error saving job posting: {str(e)}")
            return False
    
    async def get_job_posting(self, job_id: str) -> Optional[JobPosting]:
        """Get job posting by ID"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                db.row_factory = aiosqlite.Row
                cursor = await db.execute(
                    "SELECT * FROM job_postings WHERE id = ?", (job_id,)
                )
                row = await cursor.fetchone()
                
                if row:
                    return self._row_to_job_posting(row)
                return None
                
        except Exception as e:
            logger.error(f"Error getting job posting: {str(e)}")
            return None
    
    async def search_job_postings(self, filters: SearchFilters) -> List[JobPosting]:
        """Search job postings with filters"""
        try:
            query = "SELECT * FROM job_postings WHERE 1=1"
            params = []
            
            if filters.status:
                query += " AND status = ?"
                params.append(filters.status)
            
            if filters.location:
                query += " AND location LIKE ?"
                params.append(f"%{filters.location}%")
            
            if filters.job_type:
                query += " AND job_type = ?"
                params.append(filters.job_type)
            
            if filters.salary_min is not None:
                query += " AND salary_max >= ?"
                params.append(filters.salary_min)
            
            if filters.salary_max is not None:
                query += " AND salary_min <= ?"
                params.append(filters.salary_max)
            
            query += " ORDER BY updated_at DESC"
            
            async with aiosqlite.connect(self.db_path) as db:
                db.row_factory = aiosqlite.Row
                cursor = await db.execute(query, params)
                rows = await cursor.fetchall()
                
                return [self._row_to_job_posting(row) for row in rows]
                
        except Exception as e:
            logger.error(f"Error searching job postings: {str(e)}")
            return []
    
    async def update_job_posting(self, job: JobPosting) -> bool:
        """Update job posting"""
        return await self.save_job_posting(job)
    
    async def count_job_postings(self) -> int:
        """Count total job postings"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                cursor = await db.execute("SELECT COUNT(*) FROM job_postings")
                result = await cursor.fetchone()
                return result[0] if result else 0
        except Exception as e:
            logger.error(f"Error counting job postings: {str(e)}")
            return 0
    
    # Application operations
    async def save_application(self, application: Application) -> bool:
        """Save application to database"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                match_score_json = None
                if application.match_score:
                    match_score_json = json.dumps(application.match_score.dict())
                
                await db.execute("""
                    INSERT OR REPLACE INTO applications (
                        id, candidate_id, job_id, status, match_score_data,
                        cover_letter, interview_notes, interview_questions,
                        applied_at, updated_at, reviewed_by, review_notes
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    application.id,
                    application.candidate_id,
                    application.job_id,
                    application.status.value,
                    match_score_json,
                    application.cover_letter,
                    application.interview_notes,
                    json.dumps(application.interview_questions),
                    application.applied_at.isoformat(),
                    application.updated_at.isoformat(),
                    application.reviewed_by,
                    application.review_notes
                ))
                await db.commit()
                return True
                
        except Exception as e:
            logger.error(f"Error saving application: {str(e)}")
            return False
    
    async def get_application(self, application_id: str) -> Optional[Application]:
        """Get application by ID"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                db.row_factory = aiosqlite.Row
                cursor = await db.execute(
                    "SELECT * FROM applications WHERE id = ?", (application_id,)
                )
                row = await cursor.fetchone()
                
                if row:
                    return self._row_to_application(row)
                return None
                
        except Exception as e:
            logger.error(f"Error getting application: {str(e)}")
            return None
    
    async def get_applications_for_job(self, job_id: str) -> List[Application]:
        """Get all applications for a job"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                db.row_factory = aiosqlite.Row
                cursor = await db.execute(
                    "SELECT * FROM applications WHERE job_id = ? ORDER BY applied_at DESC",
                    (job_id,)
                )
                rows = await cursor.fetchall()
                
                return [self._row_to_application(row) for row in rows]
                
        except Exception as e:
            logger.error(f"Error getting applications for job: {str(e)}")
            return []
    
    async def get_applications_for_candidate(self, candidate_id: str) -> List[Application]:
        """Get all applications for a candidate"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                db.row_factory = aiosqlite.Row
                cursor = await db.execute(
                    "SELECT * FROM applications WHERE candidate_id = ? ORDER BY applied_at DESC",
                    (candidate_id,)
                )
                rows = await cursor.fetchall()
                
                return [self._row_to_application(row) for row in rows]
                
        except Exception as e:
            logger.error(f"Error getting applications for candidate: {str(e)}")
            return []
    
    async def update_application(self, application: Application) -> bool:
        """Update application"""
        return await self.save_application(application)
    
    async def count_applications(self) -> int:
        """Count total applications"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                cursor = await db.execute("SELECT COUNT(*) FROM applications")
                result = await cursor.fetchone()
                return result[0] if result else 0
        except Exception as e:
            logger.error(f"Error counting applications: {str(e)}")
            return 0
    
    async def count_applications_this_month(self) -> int:
        """Count applications from this month"""
        try:
            first_day_of_month = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            
            async with aiosqlite.connect(self.db_path) as db:
                cursor = await db.execute(
                    "SELECT COUNT(*) FROM applications WHERE applied_at >= ?",
                    (first_day_of_month.isoformat(),)
                )
                result = await cursor.fetchone()
                return result[0] if result else 0
        except Exception as e:
            logger.error(f"Error counting applications this month: {str(e)}")
            return 0
    
    async def get_average_match_score(self) -> float:
        """Get average match score across all applications"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                cursor = await db.execute(
                    "SELECT match_score_data FROM applications WHERE match_score_data IS NOT NULL"
                )
                rows = await cursor.fetchall()
                
                if not rows:
                    return 0.0
                
                total_score = 0
                count = 0
                
                for row in rows:
                    try:
                        match_data = json.loads(row[0])
                        total_score += match_data.get("overall_score", 0)
                        count += 1
                    except (json.JSONDecodeError, KeyError):
                        continue
                
                return total_score / count if count > 0 else 0.0
                
        except Exception as e:
            logger.error(f"Error getting average match score: {str(e)}")
            return 0.0
    
    async def get_top_skills(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get top skills across all candidates"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                cursor = await db.execute("SELECT skills FROM candidates WHERE skills IS NOT NULL")
                rows = await cursor.fetchall()
                
                skill_counts = {}
                
                for row in rows:
                    try:
                        skills = json.loads(row[0])
                        for skill in skills:
                            skill_lower = skill.lower().strip()
                            skill_counts[skill_lower] = skill_counts.get(skill_lower, 0) + 1
                    except json.JSONDecodeError:
                        continue
                
                # Sort by count and return top skills
                sorted_skills = sorted(skill_counts.items(), key=lambda x: x[1], reverse=True)
                
                return [
                    {"skill": skill, "count": count}
                    for skill, count in sorted_skills[:limit]
                ]
                
        except Exception as e:
            logger.error(f"Error getting top skills: {str(e)}")
            return []
    
    # Helper methods for converting database rows to models
    def _row_to_candidate(self, row) -> Candidate:
        """Convert database row to Candidate model"""
        from models.ats_models import ContactInfo, Education, Experience
        
        contact_info = ContactInfo(
            email=row["email"],
            phone=row["phone"],
            linkedin=row["linkedin"],
            github=row["github"],
            website=row["website"]
        )
        
        skills = json.loads(row["skills"]) if row["skills"] else []
        education = [Education(**edu) for edu in json.loads(row["education"])] if row["education"] else []
        experience = [Experience(**exp) for exp in json.loads(row["experience"])] if row["experience"] else []
        
        return Candidate(
            id=row["id"],
            first_name=row["first_name"],
            last_name=row["last_name"],
            contact_info=contact_info,
            resume_text=row["resume_text"],
            resume_file_path=row["resume_file_path"],
            skills=skills,
            education=education,
            experience=experience,
            years_of_experience=row["years_of_experience"],
            created_at=datetime.fromisoformat(row["created_at"]),
            updated_at=datetime.fromisoformat(row["updated_at"])
        )
    
    def _row_to_job_posting(self, row) -> JobPosting:
        """Convert database row to JobPosting model"""
        return JobPosting(
            id=row["id"],
            title=row["title"],
            company=row["company"],
            department=row["department"],
            location=row["location"],
            job_type=row["job_type"],
            salary_min=row["salary_min"],
            salary_max=row["salary_max"],
            description=row["description"],
            requirements=json.loads(row["requirements"]) if row["requirements"] else [],
            preferred_qualifications=json.loads(row["preferred_qualifications"]) if row["preferred_qualifications"] else [],
            required_skills=json.loads(row["required_skills"]) if row["required_skills"] else [],
            preferred_skills=json.loads(row["preferred_skills"]) if row["preferred_skills"] else [],
            status=JobStatus(row["status"]),
            created_at=datetime.fromisoformat(row["created_at"]),
            updated_at=datetime.fromisoformat(row["updated_at"]),
            posted_date=datetime.fromisoformat(row["posted_date"]) if row["posted_date"] else None,
            closing_date=datetime.fromisoformat(row["closing_date"]) if row["closing_date"] else None
        )
    
    def _row_to_application(self, row) -> Application:
        """Convert database row to Application model"""
        from models.ats_models import MatchScore
        
        match_score = None
        if row["match_score_data"]:
            try:
                match_data = json.loads(row["match_score_data"])
                match_score = MatchScore(**match_data)
            except json.JSONDecodeError:
                pass
        
        return Application(
            id=row["id"],
            candidate_id=row["candidate_id"],
            job_id=row["job_id"],
            status=ApplicationStatus(row["status"]),
            match_score=match_score,
            cover_letter=row["cover_letter"],
            interview_notes=row["interview_notes"],
            interview_questions=json.loads(row["interview_questions"]) if row["interview_questions"] else [],
            applied_at=datetime.fromisoformat(row["applied_at"]),
            updated_at=datetime.fromisoformat(row["updated_at"]),
            reviewed_by=row["reviewed_by"],
            review_notes=row["review_notes"]
        )
    
    async def cleanup(self):
        """Cleanup database resources"""
        # SQLite doesn't require explicit cleanup for async connections
        logger.info("Database cleanup completed")
