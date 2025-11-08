"""
Basic functionality tests for ATS Python Project
"""
import pytest
import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent.parent / "src"))

from core.ats_engine import ATSEngine
from models.ats_models import JobPosting, Candidate, ContactInfo, JobStatus
from services.document_processor import DocumentProcessor
from utils.matching_algorithms import MatchingAlgorithms


class TestDocumentProcessor:
    """Test document processing functionality"""
    
    def setup_method(self):
        self.processor = DocumentProcessor()
    
    def test_validate_file_nonexistent(self):
        """Test validation of non-existent file"""
        is_valid, message = self.processor.validate_file("nonexistent_file.pdf")
        assert not is_valid
        assert "does not exist" in message
    
    def test_extract_contact_info(self):
        """Test contact information extraction"""
        sample_text = """
        John Doe
        Email: john.doe@example.com
        Phone: (555) 123-4567
        LinkedIn: linkedin.com/in/johndoe
        GitHub: github.com/johndoe
        """
        
        contact_info = self.processor.extract_contact_info(sample_text)
        
        assert contact_info["email"] == "john.doe@example.com"
        assert contact_info["phone"] == "(555) 123-4567"
        assert "linkedin.com/in/johndoe" in contact_info["linkedin"]
        assert "github.com/johndoe" in contact_info["github"]
    
    def test_extract_experience_years(self):
        """Test experience years extraction"""
        text1 = "I have 5 years of experience in software development"
        text2 = "3+ years experience in data science"
        text3 = "No specific experience mentioned"
        
        assert self.processor.extract_experience_years(text1) == 5
        assert self.processor.extract_experience_years(text2) == 3
        assert self.processor.extract_experience_years(text3) is None
    
    def test_clean_text(self):
        """Test text cleaning functionality"""
        dirty_text = "This   has    extra   spaces\n\nand\t\ttabs"
        clean_text = self.processor.clean_text(dirty_text)
        
        assert "  " not in clean_text  # No double spaces
        assert clean_text.strip() == clean_text  # No leading/trailing spaces


class TestMatchingAlgorithms:
    """Test matching algorithms"""
    
    def setup_method(self):
        self.matcher = MatchingAlgorithms()
    
    def test_normalize_skills(self):
        """Test skill normalization"""
        skills = ["Python", "JavaScript", "React.js", "AWS"]
        normalized = self.matcher.normalize_skills(skills)
        
        assert "python" in normalized
        assert "javascript" in normalized
        assert "react" in normalized
        assert "aws" in normalized
    
    def test_calculate_skill_match_score(self):
        """Test skill matching calculation"""
        candidate_skills = ["Python", "JavaScript", "React", "SQL"]
        required_skills = ["Python", "React", "Node.js"]
        preferred_skills = ["JavaScript", "AWS"]
        
        result = self.matcher.calculate_skill_match_score(
            candidate_skills, required_skills, preferred_skills
        )
        
        assert result["score"] > 0
        assert len(result["matched_required"]) > 0
        assert "python" in result["matched_required"]
        assert "react" in result["matched_required"]
    
    def test_calculate_experience_match_score(self):
        """Test experience matching"""
        job_description = "We require 3+ years of experience in software development"
        
        # Test candidate with exact experience
        result1 = self.matcher.calculate_experience_match_score(3, job_description)
        assert result1["score"] >= 75
        
        # Test candidate with more experience
        result2 = self.matcher.calculate_experience_match_score(5, job_description)
        assert result2["score"] > result1["score"]
        
        # Test candidate with less experience
        result3 = self.matcher.calculate_experience_match_score(1, job_description)
        assert result3["score"] < result1["score"]


class TestATSModels:
    """Test ATS data models"""
    
    def test_candidate_creation(self):
        """Test candidate model creation"""
        contact_info = ContactInfo(
            email="test@example.com",
            phone="555-1234"
        )
        
        candidate = Candidate(
            first_name="John",
            last_name="Doe",
            contact_info=contact_info,
            skills=["Python", "JavaScript"],
            years_of_experience=3
        )
        
        assert candidate.full_name == "John Doe"
        assert candidate.contact_info.email == "test@example.com"
        assert len(candidate.skills) == 2
    
    def test_job_posting_creation(self):
        """Test job posting model creation"""
        job = JobPosting(
            title="Software Developer",
            company="Tech Corp",
            location="Remote",
            description="We are looking for a skilled developer",
            required_skills=["Python", "JavaScript"],
            status=JobStatus.ACTIVE
        )
        
        assert job.title == "Software Developer"
        assert job.status == JobStatus.ACTIVE
        assert len(job.required_skills) == 2


@pytest.mark.asyncio
class TestATSEngine:
    """Test ATS Engine functionality"""
    
    async def test_engine_initialization(self):
        """Test ATS engine initialization"""
        engine = ATSEngine()
        
        # Test that engine can be created
        assert engine is not None
        assert engine.document_processor is not None
        assert engine.matching_algorithms is not None
    
    async def test_create_job_posting(self):
        """Test job posting creation"""
        engine = ATSEngine()
        await engine.initialize()
        
        job_data = {
            "title": "Test Developer",
            "company": "Test Company",
            "location": "Test Location",
            "description": "Test job description",
            "required_skills": ["Python", "Testing"]
        }
        
        job = await engine.create_job_posting(job_data)
        
        assert job is not None
        assert job.title == "Test Developer"
        assert job.id is not None
        
        # Cleanup
        await engine.cleanup()


def run_tests():
    """Run all tests"""
    print("🧪 Running ATS Python Project Tests...")
    print("=" * 50)
    
    # Run pytest
    import subprocess
    import sys
    
    try:
        result = subprocess.run([
            sys.executable, "-m", "pytest", 
            str(Path(__file__)), 
            "-v", "--tb=short"
        ], capture_output=True, text=True)
        
        print(result.stdout)
        if result.stderr:
            print("Errors:")
            print(result.stderr)
        
        return result.returncode == 0
    
    except Exception as e:
        print(f"Error running tests: {e}")
        return False


if __name__ == "__main__":
    success = run_tests()
    if success:
        print("\n✅ All tests passed!")
    else:
        print("\n❌ Some tests failed!")
        sys.exit(1)
