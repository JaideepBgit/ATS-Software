#!/usr/bin/env python3
"""
Script to modify Resume-Matcher backend to use LM Studio instead of Ollama
Run this script from the Resume-Matcher root directory
"""

import os
import re
from pathlib import Path

def find_python_files(directory):
    """Find all Python files in the backend directory"""
    backend_dir = Path(directory) / "apps" / "backend"
    if not backend_dir.exists():
        print(f"Backend directory not found: {backend_dir}")
        return []
    
    python_files = []
    for file_path in backend_dir.rglob("*.py"):
        python_files.append(file_path)
    return python_files

def modify_ollama_imports(file_path):
    """Replace Ollama imports with OpenAI imports"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Replace ollama imports
        content = re.sub(r'import ollama', 'from openai import OpenAI', content)
        content = re.sub(r'from ollama import.*', 'from openai import OpenAI', content)
        
        # Replace ollama client usage
        content = re.sub(
            r'ollama\.chat\(',
            'client.chat.completions.create(',
            content
        )
        
        content = re.sub(
            r'ollama\.generate\(',
            'client.chat.completions.create(',
            content
        )
        
        # Add OpenAI client initialization if ollama was used
        if 'ollama' in original_content.lower() and 'client = OpenAI' not in content:
            # Find a good place to add the client initialization
            lines = content.split('\n')
            insert_index = 0
            
            # Find imports section
            for i, line in enumerate(lines):
                if line.strip().startswith('from ') or line.strip().startswith('import '):
                    insert_index = i + 1
            
            # Add client initialization after imports
            client_init = '''
# LM Studio OpenAI-compatible client
import os
client = OpenAI(
    base_url=os.getenv("LLM_URL", "http://127.0.0.1:1234/v1"),
    api_key=os.getenv("API_KEY", "lm-studio")
)
'''
            lines.insert(insert_index, client_init)
            content = '\n'.join(lines)
        
        # Only write if content changed
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Modified: {file_path}")
            return True
        
    except Exception as e:
        print(f"Error modifying {file_path}: {e}")
        return False
    
    return False

def create_requirements_addition():
    """Create additional requirements for OpenAI"""
    return """
# Additional requirement for LM Studio integration
openai>=1.0.0
python-dotenv>=1.0.0
"""

def main():
    """Main function to modify the backend"""
    print("🔧 Modifying Resume-Matcher backend for LM Studio...")
    
    # Get current directory
    current_dir = Path.cwd()
    resume_matcher_dir = current_dir / "Resume-Matcher"
    
    if not resume_matcher_dir.exists():
        print("❌ Resume-Matcher directory not found!")
        print("Please run this script from the directory containing Resume-Matcher folder")
        return
    
    # Find Python files
    python_files = find_python_files(resume_matcher_dir)
    print(f"Found {len(python_files)} Python files in backend")
    
    # Modify files
    modified_count = 0
    for file_path in python_files:
        if modify_ollama_imports(file_path):
            modified_count += 1
    
    print(f"✅ Modified {modified_count} files")
    
    # Create additional requirements file
    req_file = resume_matcher_dir / "apps" / "backend" / "requirements_lmstudio.txt"
    with open(req_file, 'w') as f:
        f.write(create_requirements_addition())
    print(f"✅ Created additional requirements: {req_file}")
    
    print("\n🎯 Next steps:")
    print("1. Copy backend_env_config.txt content to Resume-Matcher/apps/backend/.env")
    print("2. Copy frontend_env_config.txt content to Resume-Matcher/.env.local")
    print("3. Install additional requirements: pip install -r apps/backend/requirements_lmstudio.txt")
    print("4. Start the applications as instructed")

if __name__ == "__main__":
    main()
