"""
Quick test to verify company_name and role_name are stored correctly
Run this while backend is running: python test_company_role.py
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_company_role_storage():
    print("=" * 60)
    print("Testing Company Name & Role Name Storage")
    print("=" * 60)
    
    # Step 1: Set job description with company and role
    print("\n1. Setting job description with company and role...")
    job_data = {
        "job_description": "We are looking for a Machine Learning Engineer...",
        "company_name": "Google",
        "role_name": "Machine Learning Engineer"
    }
    
    response = requests.post(f"{BASE_URL}/api/job-description", json=job_data)
    print(f"   Response: {response.json()}")
    
    # Step 2: Verify it was saved
    print("\n2. Verifying saved data...")
    response = requests.get(f"{BASE_URL}/api/job-description")
    saved_data = response.json()
    print(f"   Company: '{saved_data.get('company_name')}'")
    print(f"   Role: '{saved_data.get('role_name')}'")
    
    # Step 3: Check debug endpoint
    print("\n3. Checking debug storage...")
    response = requests.get(f"{BASE_URL}/api/debug/storage")
    debug_data = response.json()
    print(f"   Company in storage: '{debug_data.get('company_name')}'")
    print(f"   Role in storage: '{debug_data.get('role_name')}'")
    print(f"   Total results: {debug_data.get('total_results')}")
    
    # Step 4: Check existing results
    print("\n4. Checking existing results...")
    response = requests.get(f"{BASE_URL}/api/results")
    results = response.json().get('results', [])
    print(f"   Found {len(results)} results")
    
    if results:
        print("\n   Sample result:")
        sample = results[0]
        print(f"   - Candidate: {sample.get('candidate_name')}")
        print(f"   - Company: '{sample.get('company_name')}'")
        print(f"   - Role: '{sample.get('role_name')}'")
    
    print("\n" + "=" * 60)
    print("Test Complete!")
    print("=" * 60)
    
    # Verification
    if saved_data.get('company_name') == 'Google' and saved_data.get('role_name') == 'Machine Learning Engineer':
        print("✓ SUCCESS: Company and Role are stored correctly!")
    else:
        print("✗ FAILED: Company and Role not stored correctly")
        print(f"  Expected: Google / Machine Learning Engineer")
        print(f"  Got: {saved_data.get('company_name')} / {saved_data.get('role_name')}")

if __name__ == "__main__":
    try:
        test_company_role_storage()
    except requests.exceptions.ConnectionError:
        print("ERROR: Cannot connect to backend. Make sure it's running on http://localhost:8000")
    except Exception as e:
        print(f"ERROR: {e}")
