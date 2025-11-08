"""
Pydantic models for ATS data structures
"""
from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, EmailStr
from enum import Enum


class JobStatus(str, Enum):
    """Job posting status"""
    DRAFT = "draft"
    ACTIVE = "active"
    PAUSED = "paused"
    CLOSED = "closed"


class ApplicationStatus(str, Enum):
    """Application status"""
    SUBMITTED = "submitted"
    SCREENING = "screening"
    INTERVIEW = "interview"
    OFFER = "offer"
    HIRED = "hired"
    REJECTED = "rejected"
    WITHDRAWN = "withdrawn"


class ContactInfo(BaseModel):
    """Contact information model"""
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    linkedin: Optional[str] = None
    github: Optional[str] = None
    website: Optional[str] = None


class Education(BaseModel):
    """Education model"""
    degree: str
    field: str
    institution: Optional[str] = None
    graduation_year: Optional[int] = None
    gpa: Optional[float] = None


class Experience(BaseModel):
    """Work experience model"""
    title: str
    company: str
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    description: Optional[str] = None
    is_current: bool = False


class Candidate(BaseModel):
    """Candidate model"""
    id: Optional[str] = None
    first_name: str
    last_name: str
    contact_info: ContactInfo
    resume_text: Optional[str] = None
    resume_file_path: Optional[str] = None
    skills: List[str] = Field(default_factory=list)
    education: List[Education] = Field(default_factory=list)
    experience: List[Experience] = Field(default_factory=list)
    years_of_experience: Optional[int] = None
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    
    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"


class JobPosting(BaseModel):
    """Job posting model"""
    id: Optional[str] = None
    title: str
    company: str
    department: Optional[str] = None
    location: str
    job_type: str = "full-time"  # full-time, part-time, contract, internship
    salary_min: Optional[float] = None
    salary_max: Optional[float] = None
    description: str
    requirements: List[str] = Field(default_factory=list)
    preferred_qualifications: List[str] = Field(default_factory=list)
    required_skills: List[str] = Field(default_factory=list)
    preferred_skills: List[str] = Field(default_factory=list)
    status: JobStatus = JobStatus.DRAFT
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    posted_date: Optional[datetime] = None
    closing_date: Optional[datetime] = None


class MatchScore(BaseModel):
    """Match score between candidate and job"""
    overall_score: float = Field(ge=0, le=100)
    skill_match_score: float = Field(ge=0, le=100)
    experience_match_score: float = Field(ge=0, le=100)
    education_match_score: float = Field(ge=0, le=100)
    matched_skills: List[str] = Field(default_factory=list)
    missing_skills: List[str] = Field(default_factory=list)
    strengths: List[str] = Field(default_factory=list)
    recommendations: List[str] = Field(default_factory=list)


class Application(BaseModel):
    """Job application model"""
    id: Optional[str] = None
    candidate_id: str
    job_id: str
    status: ApplicationStatus = ApplicationStatus.SUBMITTED
    match_score: Optional[MatchScore] = None
    cover_letter: Optional[str] = None
    interview_notes: Optional[str] = None
    interview_questions: List[str] = Field(default_factory=list)
    applied_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    reviewed_by: Optional[str] = None
    review_notes: Optional[str] = None


class InterviewQuestion(BaseModel):
    """Interview question model"""
    id: Optional[str] = None
    question: str
    category: str = "general"  # technical, behavioral, general, etc.
    difficulty: str = "medium"  # easy, medium, hard
    job_id: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)


class ATSStats(BaseModel):
    """ATS statistics model"""
    total_candidates: int = 0
    total_jobs: int = 0
    total_applications: int = 0
    active_jobs: int = 0
    applications_this_month: int = 0
    avg_match_score: float = 0.0
    top_skills: List[Dict[str, Any]] = Field(default_factory=list)


class SearchFilters(BaseModel):
    """Search filters for candidates and jobs"""
    skills: Optional[List[str]] = None
    location: Optional[str] = None
    experience_min: Optional[int] = None
    experience_max: Optional[int] = None
    education_level: Optional[str] = None
    job_type: Optional[str] = None
    salary_min: Optional[float] = None
    salary_max: Optional[float] = None
    status: Optional[str] = None


class BulkProcessRequest(BaseModel):
    """Request model for bulk processing"""
    file_paths: List[str]
    job_id: Optional[str] = None
    auto_apply: bool = False
    notify_on_completion: bool = True


class ATSResponse(BaseModel):
    """Standard ATS API response"""
    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None
    errors: Optional[List[str]] = None
    timestamp: datetime = Field(default_factory=datetime.now)
