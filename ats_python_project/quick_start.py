"""
Quick Start Demo for ATS Python Project
This script demonstrates basic functionality without requiring full setup
"""
import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

from services.document_processor import DocumentProcessor
from utils.matching_algorithms import MatchingAlgorithms
from models.ats_models import Candidate, JobPosting, ContactInfo, JobStatus


async def demo_document_processing():
    """Demonstrate document processing capabilities"""
    print("📄 Document Processing Demo")
    print("-" * 40)
    
    processor = DocumentProcessor()
    
    # Check if sample resume exists
    sample_resume = Path("data/sample_resume.txt")
    if sample_resume.exists():
        print(f"Processing sample resume: {sample_resume}")
        
        # Extract text
        text = processor.extract_text(str(sample_resume))
        print(f"✓ Extracted {len(text)} characters of text")
        
        # Extract contact info
        contact_info = processor.extract_contact_info(text)
        print(f"✓ Found contact info:")
        for key, value in contact_info.items():
            if value:
                print(f"  {key}: {value}")
        
        # Extract experience
        years_exp = processor.extract_experience_years(text)
        print(f"✓ Experience: {years_exp} years" if years_exp else "✓ Experience: Not specified")
        
        # Get text statistics
        stats = processor.get_text_statistics(text)
        print(f"✓ Text statistics:")
        for key, value in stats.items():
            print(f"  {key}: {value}")
    
    else:
        print("❌ Sample resume not found. Run setup.py first or create data/sample_resume.txt")
    
    print()


def demo_matching_algorithms():
    """Demonstrate matching algorithms"""
    print("🎯 Matching Algorithms Demo")
    print("-" * 40)
    
    matcher = MatchingAlgorithms()
    
    # Sample data
    candidate_skills = ["Python", "JavaScript", "React", "SQL", "AWS"]
    job_required_skills = ["Python", "React", "PostgreSQL"]
    job_preferred_skills = ["JavaScript", "AWS", "Docker"]
    
    print(f"Candidate skills: {candidate_skills}")
    print(f"Job required skills: {job_required_skills}")
    print(f"Job preferred skills: {job_preferred_skills}")
    
    # Calculate skill match
    skill_match = matcher.calculate_skill_match_score(
        candidate_skills, job_required_skills, job_preferred_skills
    )
    
    print(f"\n✓ Skill Match Results:")
    print(f"  Overall score: {skill_match['score']:.1f}%")
    print(f"  Required skills score: {skill_match['required_score']:.1f}%")
    print(f"  Preferred skills score: {skill_match['preferred_score']:.1f}%")
    print(f"  Matched required: {skill_match['matched_required']}")
    print(f"  Matched preferred: {skill_match['matched_preferred']}")
    print(f"  Missing required: {skill_match['missing_required']}")
    
    # Test experience matching
    job_description = "We are looking for a developer with 3+ years of experience in Python development"
    exp_match = matcher.calculate_experience_match_score(5, job_description)
    
    print(f"\n✓ Experience Match Results:")
    print(f"  Score: {exp_match['score']:.1f}%")
    print(f"  Required years: {exp_match['required_years']}")
    print(f"  Candidate years: {exp_match['candidate_years']}")
    print(f"  Gap: {exp_match.get('gap', 'N/A')} years")
    
    print()


def demo_models():
    """Demonstrate data models"""
    print("📊 Data Models Demo")
    print("-" * 40)
    
    # Create sample candidate
    contact_info = ContactInfo(
        email="john.smith@email.com",
        phone="(555) 123-4567",
        linkedin="linkedin.com/in/johnsmith"
    )
    
    candidate = Candidate(
        first_name="John",
        last_name="Smith",
        contact_info=contact_info,
        skills=["Python", "JavaScript", "React", "SQL", "AWS"],
        years_of_experience=5
    )
    
    print(f"✓ Created candidate: {candidate.full_name}")
    print(f"  Email: {candidate.contact_info.email}")
    print(f"  Skills: {', '.join(candidate.skills)}")
    print(f"  Experience: {candidate.years_of_experience} years")
    
    # Create sample job
    job = JobPosting(
        title="Senior Python Developer",
        company="TechCorp",
        location="Remote",
        description="We are looking for an experienced Python developer...",
        required_skills=["Python", "Django", "PostgreSQL"],
        preferred_skills=["React", "AWS", "Docker"],
        status=JobStatus.ACTIVE
    )
    
    print(f"\n✓ Created job posting: {job.title}")
    print(f"  Company: {job.company}")
    print(f"  Location: {job.location}")
    print(f"  Required skills: {', '.join(job.required_skills)}")
    print(f"  Preferred skills: {', '.join(job.preferred_skills)}")
    print(f"  Status: {job.status.value}")
    
    # Calculate basic match
    matcher = MatchingAlgorithms()
    match_score = matcher.calculate_basic_match_score(candidate, job)
    
    print(f"\n✓ Match Score: {match_score.overall_score:.1f}%")
    print(f"  Skill match: {match_score.skill_match_score:.1f}%")
    print(f"  Experience match: {match_score.experience_match_score:.1f}%")
    print(f"  Education match: {match_score.education_match_score:.1f}%")
    print(f"  Matched skills: {', '.join(match_score.matched_skills)}")
    
    if match_score.recommendations:
        print(f"  Recommendations:")
        for rec in match_score.recommendations:
            print(f"    - {rec}")
    
    print()


def demo_configuration():
    """Demonstrate configuration"""
    print("⚙️ Configuration Demo")
    print("-" * 40)
    
    try:
        from config.settings import settings
        
        print(f"✓ App Name: {settings.app_name}")
        print(f"✓ Version: {settings.app_version}")
        print(f"✓ LM Studio URL: {settings.lm_studio_base_url}")
        print(f"✓ Database URL: {settings.database_url}")
        print(f"✓ Max file size: {settings.max_file_size_mb}MB")
        print(f"✓ Allowed file types: {', '.join(settings.allowed_file_types)}")
        print(f"✓ Debug mode: {settings.debug}")
        
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        print("   Make sure to run setup.py and configure your .env file")
    
    print()


async def main():
    """Run all demos"""
    print("🚀 ATS Python Project - Quick Start Demo")
    print("=" * 50)
    print("This demo shows basic functionality without requiring LM Studio setup")
    print()
    
    try:
        # Run demos
        await demo_document_processing()
        demo_matching_algorithms()
        demo_models()
        demo_configuration()
        
        print("=" * 50)
        print("✅ Demo completed successfully!")
        print("\nNext steps:")
        print("1. Run 'python setup.py' to complete installation")
        print("2. Configure your .env file with LM Studio settings")
        print("3. Start LM Studio and load a compatible model")
        print("4. Run 'python main.py' for the full application")
        print("\nFor more information, see README.md")
        
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        print("Make sure all dependencies are installed: pip install -r requirements.txt")


if __name__ == "__main__":
    asyncio.run(main())
