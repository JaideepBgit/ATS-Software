"""
Test script for the new storage system
"""
import requests
import json
from pathlib import Path

BASE_URL = "http://localhost:8000"

def print_section(title):
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)

def test_storage_system():
    """Test the complete storage workflow"""
    
    print_section("1. Create Job Description")
    job_data = {
        "job_description": "Senior Python Developer at TechCorp. Must have 5+ years Python, Django, REST APIs, and cloud experience.",
        "company_name": "TechCorp",
        "role_name": "Senior Python Developer"
    }
    
    response = requests.post(f"{BASE_URL}/api/job-description", json=job_data)
    result = response.json()
    print(f"✓ Job created with ID: {result['job_id']}")
    print(f"  Company: {result['company_name']}")
    print(f"  Role: {result['role_name']}")
    job_id = result['job_id']
    
    print_section("2. List All Jobs")
    response = requests.get(f"{BASE_URL}/api/jobs")
    result = response.json()
    print(f"✓ Total jobs: {result['total']}")
    for job in result['jobs'][:3]:
        print(f"  - {job['job_id']}: {job['company_name']} - {job['role_name']}")
    
    print_section("3. Get Specific Job")
    response = requests.get(f"{BASE_URL}/api/jobs/{job_id}")
    result = response.json()
    job = result['job']
    print(f"✓ Retrieved job: {job['job_id']}")
    print(f"  Company: {job['company_name']}")
    print(f"  Role: {job['role_name']}")
    print(f"  Description length: {len(job['job_description'])} chars")
    print(f"  Created: {job['created_at']}")
    
    print_section("4. Search Jobs")
    response = requests.get(f"{BASE_URL}/api/jobs/search?query=TechCorp")
    result = response.json()
    print(f"✓ Found {result['total']} jobs matching 'TechCorp'")
    
    print_section("5. Check Storage Statistics")
    response = requests.get(f"{BASE_URL}/api/storage/stats")
    stats = response.json()
    print(f"✓ Storage Statistics:")
    print(f"  Jobs: {stats['jobs']['total']}")
    print(f"  Resumes: {stats['resumes']['total']}")
    print(f"  Analyses: {stats['analyses']['total']}")
    print(f"  Feedback: {stats['feedback']['total_feedback']}")
    print(f"  Current Job ID: {stats['current_job_id']}")
    
    print_section("6. List Resumes")
    response = requests.get(f"{BASE_URL}/api/resumes")
    result = response.json()
    print(f"✓ Total resumes: {result['total']}")
    if result['resumes']:
        for resume in result['resumes'][:3]:
            print(f"  - {resume['resume_id']}: {resume['candidate_name']} ({resume['original_filename']})")
    else:
        print("  (No resumes uploaded yet)")
    
    print_section("7. List Analyses")
    response = requests.get(f"{BASE_URL}/api/analyses")
    result = response.json()
    print(f"✓ Total analyses: {result['total']}")
    if result['analyses']:
        for analysis in result['analyses'][:3]:
            print(f"  - {analysis['analysis_id']}: {analysis['candidate_name']} (Score: {analysis['overall_score']}%)")
            print(f"    Job: {analysis['job_id']}, Resume: {analysis['resume_id']}")
    else:
        print("  (No analyses yet)")
    
    print_section("8. Filter Analyses by Job")
    response = requests.get(f"{BASE_URL}/api/analyses?job_id={job_id}")
    result = response.json()
    print(f"✓ Analyses for job {job_id}: {result['total']}")
    
    print_section("Test Complete!")
    print("\nNext steps:")
    print("1. Upload a resume using the web interface")
    print("2. The resume will be analyzed against the current job")
    print("3. You'll receive analysis_id, resume_id, and job_id")
    print("4. When giving feedback, include these IDs for LoRA training")
    print("\nAll data is now persistent and won't be lost on restart!")

def test_job_selection():
    """Test selecting a different job"""
    print_section("Job Selection Test")
    
    # List jobs
    response = requests.get(f"{BASE_URL}/api/jobs")
    jobs = response.json()['jobs']
    
    if len(jobs) < 2:
        print("Need at least 2 jobs to test selection. Creating another...")
        job_data = {
            "job_description": "Data Scientist at DataCorp. ML, Python, TensorFlow required.",
            "company_name": "DataCorp",
            "role_name": "Data Scientist"
        }
        response = requests.post(f"{BASE_URL}/api/job-description", json=job_data)
        jobs = requests.get(f"{BASE_URL}/api/jobs").json()['jobs']
    
    # Select first job
    job_id = jobs[0]['job_id']
    print(f"\n1. Selecting job: {job_id}")
    response = requests.post(f"{BASE_URL}/api/jobs/{job_id}/select")
    result = response.json()
    print(f"✓ Selected: {result['company_name']} - {result['role_name']}")
    
    # Verify it's current
    response = requests.get(f"{BASE_URL}/api/job-description")
    current = response.json()
    print(f"✓ Current job: {current['company_name']} - {current['role_name']}")
    
    print("\n✓ Job selection works! You can now:")
    print("  - Switch between saved jobs")
    print("  - Analyze resumes against different jobs")
    print("  - Track which job each analysis belongs to")

if __name__ == "__main__":
    try:
        print("\n" + "=" * 60)
        print("  ATS STORAGE SYSTEM TEST")
        print("=" * 60)
        print("\nMake sure the backend is running on port 8000")
        print("Starting tests...\n")
        
        test_storage_system()
        print("\n")
        test_job_selection()
        
        print("\n" + "=" * 60)
        print("  ALL TESTS PASSED!")
        print("=" * 60)
        
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Could not connect to backend.")
        print("Please start the backend first:")
        print("  cd ats_web/backend")
        print("  python main.py")
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
