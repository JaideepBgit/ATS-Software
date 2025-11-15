"""
Test script to verify job description and analysis flow
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_job_flow():
    print("=" * 60)
    print("Testing Job Description and Analysis Flow")
    print("=" * 60)
    
    # Step 1: Save job description
    print("\n1. Saving job description...")
    job_data = {
        "job_description": "Data Scientist at Manhattan Associates. Looking for Python, ML, and data analysis skills.",
        "company_name": "Manhattan Associates",
        "role_name": "Data Scientist"
    }
    
    response = requests.post(f"{BASE_URL}/api/job-description", json=job_data)
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}")
    
    # Step 2: Get job description back
    print("\n2. Retrieving job description...")
    response = requests.get(f"{BASE_URL}/api/job-description")
    data = response.json()
    print(f"   Company: {data.get('company_name')}")
    print(f"   Role: {data.get('role_name')}")
    print(f"   Job Desc Length: {len(data.get('job_description', ''))}")
    
    # Step 3: Check debug endpoint
    print("\n3. Checking debug storage...")
    response = requests.get(f"{BASE_URL}/api/debug/storage")
    data = response.json()
    print(f"   Company in storage: {data.get('company_name')}")
    print(f"   Role in storage: {data.get('role_name')}")
    print(f"   Total results: {data.get('total_results')}")
    
    if data.get('sample_result'):
        sample = data['sample_result']
        print(f"   Sample result company: {sample.get('company_name')}")
        print(f"   Sample result role: {sample.get('role_name')}")
    
    print("\n" + "=" * 60)
    print("Test complete! Check backend logs for detailed output.")
    print("=" * 60)

if __name__ == "__main__":
    try:
        test_job_flow()
    except requests.exceptions.ConnectionError:
        print("ERROR: Could not connect to backend. Is it running on port 8000?")
    except Exception as e:
        print(f"ERROR: {e}")
