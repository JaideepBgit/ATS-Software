"""
Test Ollama Connection
Quick script to verify Ollama is running and accessible
"""
import sys
from openai import OpenAI

def test_ollama():
    """Test connection to Ollama"""
    print("\n" + "="*80)
    print("TESTING OLLAMA CONNECTION")
    print("="*80)
    
    # Test 1: Check if Ollama is running
    print("\n1. Checking if Ollama is running...")
    try:
        import requests
        response = requests.get("http://localhost:11434")
        if response.status_code == 200:
            print("   ✓ Ollama is running!")
        else:
            print(f"   ⚠️  Ollama responded with status: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Cannot connect to Ollama: {str(e)}")
        print("\n   Make sure Ollama is installed and running:")
        print("   - Install from: https://ollama.ai")
        print("   - Ollama should start automatically")
        print("   - Or run: ollama serve")
        return False
    
    # Test 2: Check if model is available
    print("\n2. Checking if qwen2.5:7b model is available...")
    try:
        import subprocess
        result = subprocess.run(['ollama', 'list'], capture_output=True, text=True)
        if 'qwen2.5:7b' in result.stdout:
            print("   ✓ Model qwen2.5:7b is available!")
        else:
            print("   ⚠️  Model qwen2.5:7b not found")
            print("\n   Available models:")
            print(result.stdout)
            print("\n   To download the model, run:")
            print("   ollama pull qwen2.5:7b")
            return False
    except Exception as e:
        print(f"   ⚠️  Could not check models: {str(e)}")
        print("   Continuing anyway...")
    
    # Test 3: Test API connection
    print("\n3. Testing Ollama API connection...")
    try:
        client = OpenAI(
            base_url="http://localhost:11434/v1",
            api_key="not-needed"  # Ollama doesn't need an API key
        )
        
        print("   ✓ OpenAI client created successfully!")
        
        # Test 4: Send a simple request
        print("\n4. Sending test request to qwen2.5:7b...")
        response = client.chat.completions.create(
            model="qwen2.5:7b",
            messages=[
                {"role": "user", "content": "Say 'Hello! I am working correctly.' in one sentence."}
            ],
            max_tokens=50,
            temperature=0.7
        )
        
        answer = response.choices[0].message.content.strip()
        print(f"   ✓ Response received: {answer}")
        
        print("\n" + "="*80)
        print("✅ ALL TESTS PASSED!")
        print("="*80)
        print("\nYour Ollama setup is working correctly!")
        print("You can now run: python interactive_ats_ollama.py")
        print("="*80 + "\n")
        return True
        
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
        print("\n" + "="*80)
        print("❌ TEST FAILED")
        print("="*80)
        print("\nTroubleshooting:")
        print("1. Make sure Ollama is running")
        print("2. Check the model is downloaded: ollama list")
        print("3. Try pulling the model: ollama pull qwen2.5:7b")
        print("4. Verify Ollama endpoint: http://localhost:11434")
        print("="*80 + "\n")
        return False


if __name__ == "__main__":
    success = test_ollama()
    sys.exit(0 if success else 1)
