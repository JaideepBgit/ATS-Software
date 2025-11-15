"""
Quick test to verify the thinking process feature works
"""
import sys
sys.path.append('backend')

from ats_service import ATSService

# Sample data
job_desc = """
Principal Data Scientist at Tendo
Requirements:
- 8+ years of experience in ML/AI
- Expert in Python, PyTorch/TensorFlow
- Experience with LLMs and RAG systems
- Strong background in retrieval and ranking
- AWS/Azure deployment experience
"""

resume_text = """
Jaideep Bommidi
Senior ML Engineer

Experience:
- 10 years in machine learning and AI
- Expert in Python, PyTorch, TensorFlow
- Built LLM fine-tuning pipelines
- Developed retrieval systems for search
- Deployed models on AWS

Skills: Python, PyTorch, TensorFlow, LLMs, RAG, AWS, Docker
"""

# Initialize service
print("Initializing ATS Service...")
ats = ATSService()

# Test thinking process generation
print("\nGenerating thinking process...")
thinking = ats._generate_thinking_process(
    resume_text=resume_text,
    job_desc=job_desc,
    candidate_name="Jaideep Bommidi",
    role_name="Principal Data Scientist"
)

print(f"\nGenerated {len(thinking)} thinking steps:")
print("-" * 80)

for i, thought in enumerate(thinking, 1):
    print(f"\n{i}. {thought['step']}")
    print(f"   {thought['thinking']}")

print("\n" + "=" * 80)
print("✓ Thinking process feature is working!")
print("=" * 80)
