"""
Quick script to clear all analysis results
Useful when testing with new job descriptions
"""
import requests

BASE_URL = "http://localhost:8000"

def clear_results():
    print("Clearing all analysis results...")
    try:
        response = requests.delete(f"{BASE_URL}/api/results")
        if response.status_code == 200:
            print("✅ Results cleared successfully!")
            print(f"   Response: {response.json()}")
        else:
            print(f"❌ Error: Status {response.status_code}")
            print(f"   Response: {response.text}")
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to backend. Is it running on port 8000?")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    clear_results()
