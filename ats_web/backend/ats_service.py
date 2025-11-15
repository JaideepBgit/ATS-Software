"""
ATS Service - Core logic from advanced_ats.py adapted for web API
"""
import os
import re
import json
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict, field
from datetime import datetime
import PyPDF2
from openai import OpenAI


@dataclass
class ATSResult:
    candidate_name: str
    filename: str
    overall_score: float
    skill_match_score: float
    experience_match_score: float
    education_match_score: float
    matched_skills: List[str]
    missing_critical_skills: List[str]
    strengths: List[str]
    weaknesses: List[str]
    executive_summary: str
    hiring_recommendation: str
    timestamp: str
    company_name: str = ""
    role_name: str = ""
    thinking_process: List[Dict[str, str]] = field(default_factory=list)


class ATSService:
    def __init__(self, llm_url: str = None, model: str = None, api_key: str = None):
        self.llm_url = llm_url or os.getenv("LLM_URL", "http://localhost:11434/v1")
        self.model = model or os.getenv("LLM_MODEL", "qwen2.5:7b")
        self.api_key = api_key or os.getenv("OPENAI_API_KEY", "not-needed")
        
        try:
            self.client = OpenAI(base_url=self.llm_url, api_key=self.api_key)
        except Exception as e:
            print(f"Warning: Could not initialize LLM client: {e}")
            self.client = None
    
    def extract_text_from_pdf(self, pdf_bytes: bytes) -> str:
        """Extract text from PDF bytes"""
        try:
            from io import BytesIO
            pdf_reader = PyPDF2.PdfReader(BytesIO(pdf_bytes))
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            return text
        except Exception as e:
            print(f"Error reading PDF: {e}")
            return ""
    
    def call_llm(self, prompt: str, system_prompt: str = None, temperature: float = 0.3) -> str:
        """Call LLM with prompt"""
        if not self.client:
            return ""
        
        try:
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})
            
            # Check if using Ollama (has extra_body support)
            if "11434" in self.llm_url or "ollama" in self.llm_url.lower():
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    temperature=temperature,
                    max_tokens=2000,
                    extra_body={"num_ctx": 8192}
                )
            else:
                # For OpenAI and other providers
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    temperature=temperature,
                    max_tokens=2000
                )
            
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"LLM Error: {e}")
            return ""
    
    def extract_json_from_response(self, response: str) -> Dict:
        """Extract JSON from LLM response"""
        if not response:
            return {}
        
        json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', response, re.DOTALL)
        if json_match:
            response = json_match.group(1)
        
        start = response.find('{')
        end = response.rfind('}')
        if start != -1 and end != -1:
            response = response[start:end+1]
        
        try:
            return json.loads(response)
        except:
            return {}
    
    def extract_job_info(self, job_desc: str) -> Dict[str, str]:
        """Extract company name and role name from job description"""
        if not self.client or not job_desc:
            return {"company_name": "", "role_name": ""}
        
        system_prompt = "You are an expert at extracting structured information from job descriptions. Return ONLY valid JSON."
        
        prompt = f"""Extract the company name and role/position name from this job description. Return ONLY valid JSON.

JOB DESCRIPTION:
{job_desc[:1500]}

Return this exact JSON structure:
{{
  "company_name": "Company Name Here",
  "role_name": "Job Title/Role Here"
}}

If you cannot find the company name or role name, use empty string ""."""
        
        response = self.call_llm(prompt, system_prompt, temperature=0.2)
        data = self.extract_json_from_response(response)
        
        return {
            "company_name": data.get("company_name", ""),
            "role_name": data.get("role_name", "")
        }
    
    def analyze_resume(self, resume_text: str, job_desc: str, filename: str, company_name: str = "", role_name: str = "") -> ATSResult:
        """Analyze a single resume against job description"""
        
        print(f"[ATS] analyze_resume called with company='{company_name}', role='{role_name}'")
        
        # Extract company and role from job description if not provided
        if not company_name or not role_name:
            print(f"[ATS] Extracting job info from description (company or role missing)")
            job_info = self.extract_job_info(job_desc)
            company_name = company_name or job_info.get("company_name", "")
            role_name = role_name or job_info.get("role_name", "")
            print(f"[ATS] Extracted: company='{company_name}', role='{role_name}'")
        
        # Extract candidate name
        candidate_name = self._extract_name(resume_text)
        
        # Generate thinking process (chain of thought)
        thinking_process = self._generate_thinking_process(resume_text, job_desc, candidate_name, role_name, company_name)
        
        # AI Analysis with enhanced focus on gaps and weaknesses
        system_prompt = """You are an expert ATS system and critical evaluator. 
Your job is to thoroughly analyze candidates, being especially rigorous about identifying gaps, missing skills, and weaknesses.
Be objective, detailed, and don't overlook potential concerns. Return ONLY valid JSON."""
        
        role_context = f" for the {role_name} role at {company_name}" if role_name and company_name else f" for the {role_name} role" if role_name else f" at {company_name}" if company_name else ""
        
        prompt = f"""Analyze this candidate{role_context} with CRITICAL attention to missing skills and weaknesses.

COMPANY: {company_name if company_name else "Not specified"}
ROLE: {role_name if role_name else "Not specified"}

JOB DESCRIPTION:
{job_desc[:2000]}

RESUME:
{resume_text[:4000]}

CRITICAL ANALYSIS REQUIREMENTS:

1. MISSING SKILLS - Be thorough and specific:
   - List EVERY required skill from the job description that is NOT clearly present in the resume
   - Include technical skills, tools, frameworks, methodologies, and soft skills
   - Don't just list obvious ones - dig deep into the job requirements
   - If a skill is mentioned but lacks depth/experience, include it as missing
   - Consider: programming languages, frameworks, cloud platforms, databases, methodologies, certifications, domain knowledge
   - Minimum 3-5 missing skills (be critical!)

2. WEAKNESSES - Be honest and detailed:
   - Identify gaps in experience level (junior vs senior expectations)
   - Note missing leadership/mentoring experience if required
   - Point out lack of specific industry experience
   - Highlight insufficient years of experience in key areas
   - Mention missing certifications or education requirements
   - Note any red flags: job hopping, career gaps, lack of progression
   - Identify missing soft skills: communication, teamwork, leadership
   - Consider scale/complexity gaps (startup vs enterprise, team size, etc.)
   - Minimum 3-5 specific weaknesses (be thorough!)

3. MATCHED SKILLS - Only include skills with clear evidence:
   - Must be explicitly mentioned in resume with context
   - Include proficiency level if evident

4. STRENGTHS - Be specific with evidence:
   - Reference actual achievements and experience
   - Quantify when possible

Return this exact JSON structure (analyze based ONLY on the actual job description above):
{{
  "skill_match_score": <number 0-100>,
  "experience_match_score": <number 0-100>,
  "education_match_score": <number 0-100>,
  "matched_skills": ["<skill with evidence>", "..."],
  "missing_critical_skills": ["<missing skill from actual job description>", "..."],
  "strengths": ["<strength with evidence>", "..."],
  "weaknesses": ["<weakness with specifics>", "..."],
  "executive_summary": "<2-3 sentence summary>",
  "hiring_recommendation": "<YES/NO/MAYBE - reason>"
}}

BE CRITICAL AND THOROUGH. Don't be lenient - identify real gaps and concerns.
Scores should be 0-100 and reflect the gaps you identify."""
        
        response = self.call_llm(prompt, system_prompt, temperature=0.4)
        data = self.extract_json_from_response(response)
        
        if not data:
            data = self._fallback_scoring(resume_text, job_desc)
        
        # Calculate overall score
        overall_score = (
            data.get('skill_match_score', 50) * 0.4 +
            data.get('experience_match_score', 50) * 0.35 +
            data.get('education_match_score', 50) * 0.25
        )
        
        return ATSResult(
            candidate_name=candidate_name,
            filename=filename,
            overall_score=round(overall_score, 2),
            skill_match_score=data.get('skill_match_score', 50),
            experience_match_score=data.get('experience_match_score', 50),
            education_match_score=data.get('education_match_score', 50),
            matched_skills=data.get('matched_skills', []),
            missing_critical_skills=data.get('missing_critical_skills', []),
            strengths=data.get('strengths', []),
            weaknesses=data.get('weaknesses', []),
            executive_summary=data.get('executive_summary', 'Analysis completed'),
            hiring_recommendation=data.get('hiring_recommendation', 'MAYBE - Requires review'),
            timestamp=datetime.now().isoformat(),
            company_name=company_name,
            role_name=role_name,
            thinking_process=thinking_process
        )
    
    def ask_question(self, question: str, context: Dict) -> str:
        """Interactive Q&A about a candidate"""
        if not self.client:
            return "LLM not available"
        
        # Check if user is asking for LaTeX format
        is_latex_request = any(keyword in question.lower() for keyword in ['latex', 'overleaf', 'tex'])
        
        formatting_instructions = """
FORMATTING GUIDELINES:
- Use **bold text** for emphasis and important points
- Use bullet points with - or * for lists
- When providing LaTeX code, wrap it in ```latex code blocks
- Structure your response clearly with proper paragraphs
"""
        
        if is_latex_request:
            formatting_instructions += """
- For LaTeX requests, provide complete, copy-paste ready LaTeX code
- Include all necessary packages and document structure
- Format the code properly with proper indentation
"""
        
        system_prompt = f"""You are an expert HR consultant. Answer questions about this candidate.

CANDIDATE: {context.get('candidate_name')}
SCORE: {context.get('overall_score')}%
RECOMMENDATION: {context.get('hiring_recommendation')}

RESUME:
{context.get('resume_text', '')[:4000]}

JOB DESCRIPTION:
{context.get('job_desc', '')[:2000]}

{formatting_instructions}

Provide specific, actionable insights."""
        
        response = self.call_llm(question, system_prompt, temperature=0.5)
        return response or "Unable to generate response"
    
    def _extract_name(self, text: str) -> str:
        """Extract name from resume text"""
        lines = text.split('\n')[:5]
        for line in lines:
            line = line.strip()
            if len(line) > 3 and len(line) < 50:
                words = line.split()
                if len(words) >= 2 and all(w[0].isupper() for w in words if w):
                    return line
        return "Unknown Candidate"
    
    def _generate_thinking_process(self, resume_text: str, job_desc: str, candidate_name: str, role_name: str, company_name: str = "") -> List[Dict[str, str]]:
        """Generate chain-of-thought reasoning for the analysis"""
        if not self.client:
            return []
        
        system_prompt = """You are an expert ATS system showing your internal reasoning process. 
Think step-by-step and question yourself as you analyze the candidate. 
Be thorough, critical, and honest - especially about gaps and concerns.
Show your thought process like a rigorous human recruiter would."""
        
        role_context = f"the {role_name} role at {company_name}" if role_name and company_name else f"the {role_name} role" if role_name else f"a position at {company_name}" if company_name else "this position"
        
        prompt = f"""Analyze this candidate for {role_context}. Show your thinking process step-by-step.

COMPANY: {company_name if company_name else "Not specified"}
ROLE: {role_name if role_name else "Not specified"}

JOB DESCRIPTION:
{job_desc[:2000]}

RESUME:
{resume_text[:4000]}

Think through this analysis step-by-step, asking yourself critical questions:
1. What are ALL the key requirements for this role? (technical, experience, soft skills, domain knowledge)
2. What technical skills does the candidate have? What's MISSING?
3. How does their experience align? What gaps exist?
4. What are the SPECIFIC concerns and red flags?
5. What makes them stand out? (be honest, not generous)
6. What's my overall assessment? Should we proceed or pass?

BE CRITICAL AND THOROUGH in your thinking. Don't overlook gaps.

Return ONLY valid JSON in this format (analyze based ONLY on the actual job description provided above):
{{
  "thoughts": [
    {{"step": "Understanding Requirements", "thinking": "What does this specific role need? Let me identify requirements from the actual job description..."}},
    {{"step": "Technical Skills Assessment", "thinking": "What technical skills does the candidate have? What's missing from the job requirements?"}},
    {{"step": "Experience Evaluation", "thinking": "How does their experience align with this specific role's requirements?"}},
    {{"step": "Critical Gap Analysis", "thinking": "What's missing based on the actual job description?"}},
    {{"step": "Standout Qualities", "thinking": "What genuinely impresses me about this candidate?"}},
    {{"step": "Final Assessment", "thinking": "Overall evaluation and recommendation..."}}
  ]
}}

Be specific, critical, and reference actual details. Don't be lenient - identify real concerns."""
        
        try:
            response = self.call_llm(prompt, system_prompt, temperature=0.6)
            data = self.extract_json_from_response(response)
            
            if data and 'thoughts' in data:
                return data['thoughts']
            
            # Fallback thinking process
            return [
                {"step": "Initial Review", "thinking": f"Analyzing {candidate_name}'s profile for the {role_name} position."},
                {"step": "Skills Assessment", "thinking": "Evaluating technical skills and their relevance to the role requirements."},
                {"step": "Experience Match", "thinking": "Comparing candidate's work history with the position's experience requirements."},
                {"step": "Final Evaluation", "thinking": "Synthesizing all factors to determine overall fit."}
            ]
        except Exception as e:
            print(f"Error generating thinking process: {e}")
            return []
    
    def _fallback_scoring(self, resume_text: str, job_desc: str) -> Dict:
        """Fallback scoring when LLM fails"""
        resume_lower = resume_text.lower()
        job_lower = job_desc.lower()
        
        job_words = set(job_lower.split())
        resume_words = set(resume_lower.split())
        
        keyword_match = len(job_words.intersection(resume_words))
        keyword_score = min((keyword_match / len(job_words)) * 100, 100) if job_words else 50
        
        return {
            'skill_match_score': keyword_score,
            'experience_match_score': 60.0,
            'education_match_score': 60.0,
            'matched_skills': ['Manual review required'],
            'missing_critical_skills': ['LLM analysis unavailable'],
            'strengths': ['Fallback analysis'],
            'weaknesses': ['Manual review needed'],
            'executive_summary': 'Automated analysis incomplete. Manual review recommended.',
            'hiring_recommendation': 'MAYBE - Requires manual review'
        }
