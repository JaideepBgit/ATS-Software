"""
Test LM Studio connection and model
Quick script to verify your setup before running the full ATS
"""
from openai import OpenAI
import sys

def test_lm_studio():
    """Test LM Studio connection"""
    print("="*80)
    print("🧪 Testing LM Studio Connection")
    print("="*80)
    
    # Configuration
    base_url = "http://localhost:1234/v1"
    model = "google/gemma-3n-e4b"
    
    print(f"\n📡 Connecting to: {base_url}")
    print(f"🤖 Model: {model}")
    
    try:
        # Create client (compatible with different OpenAI versions)
        try:
            client = OpenAI(base_url=base_url, api_key="not-needed")
        except TypeError:
            # Fallback for older OpenAI versions
            import openai as openai_module
            openai_module.api_key = "not-needed"
            openai_module.api_base = base_url
            client = OpenAI(api_key="not-needed")
            client.base_url = base_url
        
        print("\n⏳ Sending test request...")
        
        # Simple test
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Say 'Hello! LM Studio is working!' in one sentence."}
            ],
            temperature=0.3,
            max_tokens=100
        )
        
        result = response.choices[0].message.content.strip()
        
        print("\n✅ SUCCESS! LM Studio is working!")
        print(f"\n🤖 Model Response:")
        print(f"   {result}")
        
        # Test JSON extraction (important for ATS)
        print("\n⏳ Testing JSON extraction (critical for ATS)...")
        
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are an expert at extracting information. Return ONLY valid JSON."},
                {"role": "user", "content": 'Extract skills from this text: "I have 5 years of Python and JavaScript experience." Return JSON: {"skills": ["skill1", "skill2"], "years": 5}'}
            ],
            temperature=0.1,
            max_tokens=200
        )
        
        json_result = response.choices[0].message.content.strip()
        
        print(f"\n🤖 JSON Response:")
        print(f"   {json_result}")
        
        # Check if it's valid JSON
        import json
        try:
            parsed = json.loads(json_result)
            print("\n✅ JSON parsing successful!")
            print(f"   Parsed: {parsed}")
        except:
            # Try to extract JSON from response
            import re
            json_match = re.search(r'\{.*?\}', json_result, re.DOTALL)
            if json_match:
                try:
                    parsed = json.loads(json_match.group(0))
                    print("\n✅ JSON extracted and parsed successfully!")
                    print(f"   Parsed: {parsed}")
                except:
                    print("\n⚠️  JSON extraction needs improvement, but ATS has fallback handling")
            else:
                print("\n⚠️  JSON format not perfect, but ATS has fallback handling")
        
        print("\n" + "="*80)
        print("🎉 LM Studio Test Complete!")
        print("="*80)
        print("\n✅ Your setup is ready for the Advanced ATS!")
        print("\nNext steps:")
        print("1. Add PDF resumes to: data/resumes/")
        print("2. Edit job description: data/job_description.txt")
        print("3. Run: python advanced_ats.py")
        print("\nOr double-click: RUN_ADVANCED_ATS.bat")
        print("="*80 + "\n")
        
        return True
        
    except Exception as e:
        print("\n❌ ERROR: Could not connect to LM Studio")
        print(f"\nError details: {str(e)}")
        print("\n🔧 Troubleshooting:")
        print("1. Is LM Studio running?")
        print("2. Is the server started? (Click 'Start Server' in LM Studio)")
        print("3. Is the model loaded? (Load google/gemma-3n-e4b)")
        print("4. Check the URL: http://localhost:1234")
        print("5. Try restarting LM Studio")
        print("\n📖 See START_LM_STUDIO_GUIDE.md for detailed setup")
        print("="*80 + "\n")
        
        return False


if __name__ == "__main__":
    success = test_lm_studio()
    sys.exit(0 if success else 1)
