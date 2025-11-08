"""
Advanced ATS Matcher - Enterprise-grade resume analysis with LLM
Uses AI for deep semantic understanding, skill extraction, and matching
Optimized for local LLMs (LM Studio, Ollama) and cloud APIs
"""
import os
import re
import json
import time
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
import PyPDF2
from openai import OpenAI


@dataclass
class SkillAnalysis:
    """Detailed skill analysis"""
    technical_skills: List[str]
    soft_skills: List[str]
    tools_technologies: List[str]
    certifications: List[str]
    domains: List[str]


@dataclass
class ExperienceAnalysis:
    """Detailed experience analysis"""
    total_years: float
    positions: List[Dict]
    companies: List[str]
    career_progression: str
    relevant_experience_years: float


@dataclass
class EducationAnalysis:
    """Education details"""
    degrees: List[str]
    institutions: List[str]
    fields_of_study: List[str]
    graduation_years: List[int]


@dataclass
class ATSMatchResult:
    """Complete ATS matching result"""
    candidate_name: str
    filename: str
    overall_score: float
    
    # Detailed scores
    skill_match_score: float
    experience_match_score: float
    education_match_score: float
    cultural_fit_score: float
    keyword_density_score: float
    
    # Skill analysis
    matched_skills: List[str]
    missing_critical_skills: List[str]
    missing_preferred_skills: List[str]
    additional_skills: List[str]
    
    # Experience
    candidate_experience: ExperienceAnalysis
    experience_gap: str
    
    # Education
    education: EducationAnalysis
    education_match: str
    
    # AI insights
    strengths: List[str]
    weaknesses: List[str]
    red_flags: List[str]
    recommendations: List[str]
    
    # Interview
    suggested_interview_questions: List[str]
    areas_to_probe: List[str]
    
    # Summary
    executive_summary: str
    hiring_recommendation: str
    
    timestamp: str


class AdvancedATS:
    """Advanced ATS with LLM-powered analysis"""
    
    def __init__(self, config_path: str = "ats_config.txt"):
        self.config = self.load_config(config_path)
        self.setup_llm()
        
    def load_config(self, config_path: str) -> Dict[str, str]:
        """Load configuration from file"""
        config = {}
        
        if not Path(config_path).exists():
            print(f"⚠️  Config file not found: {config_path}")
            print("Creating default config file...")
            self.create_default_config(config_path)
        
        with open(config_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    config[key.strip()] = value.strip()
        
        return config
    
    def create_default_config(self, config_path: str):
        """Create a default configuration file"""
        default_config = """# Advanced ATS Configuration File

# Path to folder containing resume PDFs
RESUME_FOLDER=./data/resumes

# Path to job description text file
JOB_DESCRIPTION_FILE=./data/job_description.txt

# Minimum match score to consider (0-100)
MIN_MATCH_SCORE=60

# LLM Configuration
# Options: openai, local, azure
LLM_PROVIDER=openai

# For OpenAI (GPT-4, GPT-3.5-turbo)
OPENAI_API_KEY=your-api-key-here
OPENAI_MODEL=gpt-4o-mini

# For Local LLM (LM Studio, Ollama, etc.)
LOCAL_LLM_URL=http://localhost:1234/v1
LOCAL_LLM_MODEL=llama3

# For Azure OpenAI
AZURE_ENDPOINT=your-endpoint
AZURE_API_KEY=your-key
AZURE_DEPLOYMENT=your-deployment

# Analysis Settings
ENABLE_DEEP_ANALYSIS=true
GENERATE_INTERVIEW_QUESTIONS=true
CHECK_CULTURAL_FIT=true
ANALYZE_CAREER_PROGRESSION=true
DETECT_RED_FLAGS=true

# Output Settings
SAVE_DETAILED_REPORTS=true
OUTPUT_FOLDER=./data/reports
EXPORT_FORMAT=json,txt
"""
        with open(config_path, 'w', encoding='utf-8') as f:
            f.write(default_config)
        
        print(f"✓ Created default config at: {config_path}")
    
    def setup_llm(self):
        """Setup LLM client based on configuration"""
        provider = self.config.get('LLM_PROVIDER', 'openai').lower()
        
        if provider == 'openai':
            api_key = self.config.get('OPENAI_API_KEY', '')
            if not api_key or api_key == 'your-api-key-here':
                print("\n⚠️  WARNING: OpenAI API key not configured!")
                print("Please set OPENAI_API_KEY in ats_config.txt")
                print("Get your API key from: https://platform.openai.com/api-keys")
                self.client = None
                self.model = None
                return
            
            self.client = OpenAI(api_key=api_key)
            self.model = self.config.get('OPENAI_MODEL', 'gpt-4o-mini')
            print(f"✓ Using OpenAI: {self.model}")
            
        elif provider == 'local':
            base_url = self.config.get('LOCAL_LLM_URL', 'http://localhost:1234/v1')
            self.client = OpenAI(base_url=base_url, api_key="not-needed")
            self.model = self.config.get('LOCAL_LLM_MODEL', 'llama3')
            print(f"✓ Using Local LLM: {self.model} at {base_url}")
            
        elif provider == 'azure':
            # Azure OpenAI setup
            from openai import AzureOpenAI
            self.client = AzureOpenAI(
                api_key=self.config.get('AZURE_API_KEY'),
                api_version="2024-02-01",
                azure_endpoint=self.config.get('AZURE_ENDPOINT')
            )
            self.model = self.config.get('AZURE_DEPLOYMENT')
            print(f"✓ Using Azure OpenAI: {self.model}")
        
        else:
            print(f"❌ Unknown LLM provider: {provider}")
            self.client = None
            self.model = None
    
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extract text from PDF file"""
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
                return text
        except Exception as e:
            print(f"❌ Error reading PDF {pdf_path}: {str(e)}")
            return ""
    
    def call_llm(self, prompt: str, system_prompt: str = None, temperature: float = 0.3, max_retries: int = 3) -> str:
        """Call LLM with prompt and retry logic"""
        if not self.client:
            return ""
        
        for attempt in range(max_retries):
            try:
                messages = []
                if system_prompt:
                    messages.append({"role": "system", "content": system_prompt})
                messages.append({"role": "user", "content": prompt})
                
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    temperature=temperature,
                    max_tokens=3000,
                    timeout=120  # 2 minute timeout for local LLMs
                )
                
                return response.choices[0].message.content.strip()
            
            except Exception as e:
                if attempt < max_retries - 1:
                    print(f"   ⚠️  LLM attempt {attempt + 1} failed, retrying... ({str(e)[:50]})")
                    time.sleep(2)  # Wait before retry
                else:
                    print(f"   ❌ LLM Error after {max_retries} attempts: {str(e)}")
                    return ""
        
        return ""
    
    def extract_json_from_response(self, response: str) -> Dict:
        """Extract JSON from LLM response, handling markdown code blocks"""
        if not response:
            return {}
        
        # Try to find JSON in markdown code blocks
        json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', response, re.DOTALL)
        if json_match:
            response = json_match.group(1)
        
        # Remove any text before first { and after last }
        start = response.find('{')
        end = response.rfind('}')
        if start != -1 and end != -1:
            response = response[start:end+1]
        
        try:
            return json.loads(response)
        except json.JSONDecodeError as e:
            print(f"   ⚠️  JSON parsing error: {str(e)[:100]}")
            # Try to fix common issues
            try:
                # Remove trailing commas
                response = re.sub(r',(\s*[}\]])', r'\1', response)
                return json.loads(response)
            except:
                return {}
    
    def extract_candidate_info(self, resume_text: str) -> Dict:
        """Extract candidate information using LLM"""
        system_prompt = """You are an expert ATS system. Extract information accurately and return ONLY valid JSON."""
        
        prompt = f"""Extract candidate information from this resume. Return ONLY a JSON object with these fields:

name: Full name of candidate
email: Email address
phone: Phone number
location: City/Location
linkedin: LinkedIn URL if found
summary: 2-3 sentence professional summary

Resume text:
{resume_text[:3000]}

Return format:
{{"name": "...", "email": "...", "phone": "...", "location": "...", "linkedin": "...", "summary": "..."}}"""
        
        response = self.call_llm(prompt, system_prompt, temperature=0.1)
        data = self.extract_json_from_response(response)
        
        if not data or 'name' not in data:
            # Fallback to basic extraction
            return {
                "name": self._extract_name(resume_text),
                "email": self._extract_email(resume_text),
                "phone": self._extract_phone(resume_text),
                "location": "Unknown",
                "linkedin": self._extract_linkedin(resume_text),
                "summary": ""
            }
        
        return data
    
    def analyze_skills(self, resume_text: str, job_desc: str) -> SkillAnalysis:
        """Deep skill analysis using LLM"""
        system_prompt = """You are an expert technical recruiter. Extract ALL skills from resumes accurately. Return ONLY valid JSON."""
        
        prompt = f"""Extract ALL skills from this resume in these categories:

1. technical_skills: Programming languages, frameworks, technical abilities
2. soft_skills: Communication, leadership, teamwork, etc.
3. tools_technologies: Specific tools, platforms, software used
4. certifications: Any certifications or credentials
5. domains: Industry knowledge, business domains

Resume:
{resume_text[:4000]}

Return ONLY this JSON format:
{{"technical_skills": ["skill1", "skill2"], "soft_skills": ["skill1"], "tools_technologies": ["tool1"], "certifications": ["cert1"], "domains": ["domain1"]}}"""
        
        response = self.call_llm(prompt, system_prompt, temperature=0.2)
        data = self.extract_json_from_response(response)
        
        if not data:
            return SkillAnalysis([], [], [], [], [])
        
        try:
            return SkillAnalysis(
                technical_skills=data.get('technical_skills', []),
                soft_skills=data.get('soft_skills', []),
                tools_technologies=data.get('tools_technologies', []),
                certifications=data.get('certifications', []),
                domains=data.get('domains', [])
            )
        except:
            return SkillAnalysis([], [], [], [], [])
    
    def analyze_experience(self, resume_text: str, job_desc: str) -> ExperienceAnalysis:
        """Analyze work experience using LLM"""
        system_prompt = """You are an expert at analyzing work experience. Return ONLY valid JSON."""
        
        prompt = f"""Analyze work experience from this resume.

Job requirements:
{job_desc[:800]}

Resume:
{resume_text[:4000]}

Return ONLY this JSON:
{{
  "total_years": 5.5,
  "positions": [{{"title": "Job Title", "company": "Company", "duration": "2 years"}}],
  "companies": ["Company1", "Company2"],
  "career_progression": "Brief career growth analysis",
  "relevant_experience_years": 4.0
}}"""
        
        response = self.call_llm(prompt, system_prompt, temperature=0.2)
        data = self.extract_json_from_response(response)
        
        if not data:
            return ExperienceAnalysis(0, [], [], "Unable to analyze", 0)
        
        try:
            return ExperienceAnalysis(
                total_years=float(data.get('total_years', 0)),
                positions=data.get('positions', []),
                companies=data.get('companies', []),
                career_progression=data.get('career_progression', 'Unknown'),
                relevant_experience_years=float(data.get('relevant_experience_years', 0))
            )
        except:
            return ExperienceAnalysis(0, [], [], "Unable to analyze", 0)
    
    def analyze_education(self, resume_text: str) -> EducationAnalysis:
        """Analyze education using LLM"""
        system_prompt = """Extract education information. Return ONLY valid JSON."""
        
        prompt = f"""Extract education from this resume.

Resume:
{resume_text[:3000]}

Return ONLY this JSON:
{{"degrees": ["Degree name"], "institutions": ["University"], "fields_of_study": ["Field"], "graduation_years": [2020]}}"""
        
        response = self.call_llm(prompt, system_prompt, temperature=0.1)
        data = self.extract_json_from_response(response)
        
        if not data:
            return EducationAnalysis([], [], [], [])
        
        try:
            return EducationAnalysis(
                degrees=data.get('degrees', []),
                institutions=data.get('institutions', []),
                fields_of_study=data.get('fields_of_study', []),
                graduation_years=data.get('graduation_years', [])
            )
        except:
            return EducationAnalysis([], [], [], [])
    
    def calculate_match_score(self, resume_text: str, job_desc: str, 
                            candidate_info: Dict, skills: SkillAnalysis,
                            experience: ExperienceAnalysis, education: EducationAnalysis) -> ATSMatchResult:
        """Calculate comprehensive ATS match score using LLM"""
        
        system_prompt = """You are an expert ATS system. Analyze candidates objectively and return ONLY valid JSON."""
        
        # Prepare skill summary
        all_skills = skills.technical_skills + skills.tools_technologies
        skill_summary = ', '.join(all_skills[:30]) if all_skills else 'No skills extracted'
        
        prompt = f"""Analyze this candidate for the job. Return ONLY valid JSON.

JOB DESCRIPTION:
{job_desc[:2000]}

CANDIDATE INFO:
Name: {candidate_info.get('name', 'Unknown')}
Experience: {experience.total_years} years total, {experience.relevant_experience_years} relevant
Skills: {skill_summary}
Education: {', '.join(education.degrees) if education.degrees else 'Not specified'}

RESUME EXCERPT:
{resume_text[:3000]}

Return this exact JSON structure:
{{
  "skill_match_score": 75.0,
  "experience_match_score": 80.0,
  "education_match_score": 70.0,
  "cultural_fit_score": 65.0,
  "keyword_density_score": 60.0,
  "matched_skills": ["skill1", "skill2"],
  "missing_critical_skills": ["skill1"],
  "missing_preferred_skills": ["skill1"],
  "additional_skills": ["skill1"],
  "experience_gap": "Brief analysis",
  "education_match": "Brief analysis",
  "strengths": ["strength1", "strength2", "strength3"],
  "weaknesses": ["weakness1", "weakness2"],
  "red_flags": ["flag1"],
  "recommendations": ["rec1", "rec2"],
  "suggested_interview_questions": ["q1", "q2", "q3"],
  "areas_to_probe": ["area1", "area2"],
  "executive_summary": "2-3 sentence summary",
  "hiring_recommendation": "YES - reason"
}}

Scores should be 0-100. Be specific and actionable."""
        
        response = self.call_llm(prompt, system_prompt, temperature=0.4)
        data = self.extract_json_from_response(response)
        
        # Fallback to basic scoring if LLM fails
        if not data or 'skill_match_score' not in data:
            print("   ⚠️  Using fallback scoring method")
            data = self._fallback_scoring(resume_text, job_desc, skills, experience, education)
        
        # Ensure all required fields exist with defaults
        analysis = {
            'skill_match_score': data.get('skill_match_score', 50.0),
            'experience_match_score': data.get('experience_match_score', 50.0),
            'education_match_score': data.get('education_match_score', 50.0),
            'cultural_fit_score': data.get('cultural_fit_score', 50.0),
            'keyword_density_score': data.get('keyword_density_score', 50.0),
            'matched_skills': data.get('matched_skills', []),
            'missing_critical_skills': data.get('missing_critical_skills', []),
            'missing_preferred_skills': data.get('missing_preferred_skills', []),
            'additional_skills': data.get('additional_skills', []),
            'experience_gap': data.get('experience_gap', 'Unable to analyze'),
            'education_match': data.get('education_match', 'Unable to analyze'),
            'strengths': data.get('strengths', []),
            'weaknesses': data.get('weaknesses', []),
            'red_flags': data.get('red_flags', []),
            'recommendations': data.get('recommendations', []),
            'suggested_interview_questions': data.get('suggested_interview_questions', []),
            'areas_to_probe': data.get('areas_to_probe', []),
            'executive_summary': data.get('executive_summary', 'Analysis completed'),
            'hiring_recommendation': data.get('hiring_recommendation', 'MAYBE - Requires review')
        }
        
        # Calculate overall score
        overall_score = (
            analysis['skill_match_score'] * 0.35 +
            analysis['experience_match_score'] * 0.25 +
            analysis['education_match_score'] * 0.15 +
            analysis['cultural_fit_score'] * 0.15 +
            analysis['keyword_density_score'] * 0.10
        )
        
        return ATSMatchResult(
            candidate_name=candidate_info.get('name', 'Unknown'),
            filename="",
            overall_score=round(overall_score, 2),
            skill_match_score=analysis['skill_match_score'],
            experience_match_score=analysis['experience_match_score'],
            education_match_score=analysis['education_match_score'],
            cultural_fit_score=analysis['cultural_fit_score'],
            keyword_density_score=analysis['keyword_density_score'],
            matched_skills=analysis['matched_skills'],
            missing_critical_skills=analysis['missing_critical_skills'],
            missing_preferred_skills=analysis['missing_preferred_skills'],
            additional_skills=analysis['additional_skills'],
            candidate_experience=experience,
            experience_gap=analysis['experience_gap'],
            education=education,
            education_match=analysis['education_match'],
            strengths=analysis['strengths'],
            weaknesses=analysis['weaknesses'],
            red_flags=analysis['red_flags'],
            recommendations=analysis['recommendations'],
            suggested_interview_questions=analysis['suggested_interview_questions'],
            areas_to_probe=analysis['areas_to_probe'],
            executive_summary=analysis['executive_summary'],
            hiring_recommendation=analysis['hiring_recommendation'],
            timestamp=datetime.now().isoformat()
        )
    
    def print_detailed_report(self, result: ATSMatchResult):
        """Print comprehensive ATS report"""
        print("\n" + "="*100)
        print(f"📄 CANDIDATE: {result.candidate_name}")
        print(f"📁 FILE: {result.filename}")
        print("="*100)
        
        # Overall Score
        score = result.overall_score
        if score >= 85:
            emoji, rating = "🟢", "EXCELLENT MATCH - STRONG HIRE"
        elif score >= 70:
            emoji, rating = "🟢", "STRONG MATCH - RECOMMEND INTERVIEW"
        elif score >= 60:
            emoji, rating = "🟡", "GOOD MATCH - CONSIDER FOR INTERVIEW"
        elif score >= 45:
            emoji, rating = "🟠", "MODERATE MATCH - REVIEW CAREFULLY"
        else:
            emoji, rating = "🔴", "POOR MATCH - LIKELY NOT SUITABLE"
        
        print(f"\n{emoji} OVERALL ATS SCORE: {score}% - {rating}")
        print(f"🎯 HIRING RECOMMENDATION: {result.hiring_recommendation}")
        
        # Executive Summary
        print(f"\n📋 EXECUTIVE SUMMARY:")
        print(f"   {result.executive_summary}")
        
        # Detailed Scores
        print(f"\n📊 DETAILED SCORE BREAKDOWN:")
        print(f"   • Skills Match:       {result.skill_match_score:>6.1f}%  {'█' * int(result.skill_match_score/5)}")
        print(f"   • Experience Match:   {result.experience_match_score:>6.1f}%  {'█' * int(result.experience_match_score/5)}")
        print(f"   • Education Match:    {result.education_match_score:>6.1f}%  {'█' * int(result.education_match_score/5)}")
        print(f"   • Cultural Fit:       {result.cultural_fit_score:>6.1f}%  {'█' * int(result.cultural_fit_score/5)}")
        print(f"   • Keyword Density:    {result.keyword_density_score:>6.1f}%  {'█' * int(result.keyword_density_score/5)}")
        
        # Experience Analysis
        print(f"\n💼 EXPERIENCE ANALYSIS:")
        print(f"   • Total Experience: {result.candidate_experience.total_years} years")
        print(f"   • Relevant Experience: {result.candidate_experience.relevant_experience_years} years")
        print(f"   • Companies: {', '.join(result.candidate_experience.companies[:3])}")
        if result.candidate_experience.companies and len(result.candidate_experience.companies) > 3:
            print(f"     ... and {len(result.candidate_experience.companies) - 3} more")
        print(f"   • Career Progression: {result.candidate_experience.career_progression}")
        print(f"   • Gap Analysis: {result.experience_gap}")
        
        # Education
        if result.education.degrees:
            print(f"\n🎓 EDUCATION:")
            for degree in result.education.degrees:
                print(f"   • {degree}")
            print(f"   • Match Analysis: {result.education_match}")
        
        # Skills Analysis
        if result.matched_skills:
            print(f"\n✅ MATCHING SKILLS ({len(result.matched_skills)}):")
            for i, skill in enumerate(result.matched_skills[:20], 1):
                print(f"   {i:2d}. {skill}")
            if len(result.matched_skills) > 20:
                print(f"   ... and {len(result.matched_skills) - 20} more")
        
        if result.missing_critical_skills:
            print(f"\n❌ MISSING CRITICAL SKILLS ({len(result.missing_critical_skills)}):")
            for skill in result.missing_critical_skills:
                print(f"   • {skill}")
        
        if result.missing_preferred_skills:
            print(f"\n⚠️  MISSING PREFERRED SKILLS ({len(result.missing_preferred_skills)}):")
            for skill in result.missing_preferred_skills[:10]:
                print(f"   • {skill}")
        
        # Strengths & Weaknesses
        if result.strengths:
            print(f"\n💪 KEY STRENGTHS:")
            for i, strength in enumerate(result.strengths, 1):
                print(f"   {i}. {strength}")
        
        if result.weaknesses:
            print(f"\n⚠️  AREAS OF CONCERN:")
            for i, weakness in enumerate(result.weaknesses, 1):
                print(f"   {i}. {weakness}")
        
        if result.red_flags:
            print(f"\n🚩 RED FLAGS:")
            for flag in result.red_flags:
                print(f"   • {flag}")
        
        # Recommendations
        if result.recommendations:
            print(f"\n💡 RECOMMENDATIONS:")
            for i, rec in enumerate(result.recommendations, 1):
                print(f"   {i}. {rec}")
        
        # Interview Questions
        if result.suggested_interview_questions:
            print(f"\n❓ SUGGESTED INTERVIEW QUESTIONS:")
            for i, question in enumerate(result.suggested_interview_questions, 1):
                print(f"   {i}. {question}")
        
        if result.areas_to_probe:
            print(f"\n🔍 AREAS TO PROBE IN INTERVIEW:")
            for area in result.areas_to_probe:
                print(f"   • {area}")
        
        print("\n" + "="*100)
    
    def _fallback_scoring(self, resume_text: str, job_desc: str, skills: SkillAnalysis,
                         experience: ExperienceAnalysis, education: EducationAnalysis) -> Dict:
        """Fallback scoring when LLM fails"""
        resume_lower = resume_text.lower()
        job_lower = job_desc.lower()
        
        # Extract job requirements
        job_words = set(job_lower.split())
        resume_words = set(resume_lower.split())
        
        # Keyword match
        keyword_match = len(job_words.intersection(resume_words))
        keyword_score = min((keyword_match / len(job_words)) * 100, 100) if job_words else 50
        
        # Skill match
        all_skills = skills.technical_skills + skills.tools_technologies
        matched_skills = [s for s in all_skills if s.lower() in job_lower]
        skill_score = min((len(matched_skills) / max(len(all_skills), 1)) * 100, 100) if all_skills else 50
        
        # Experience match
        exp_score = min((experience.relevant_experience_years / max(experience.total_years, 1)) * 100, 100) if experience.total_years > 0 else 50
        
        return {
            'skill_match_score': skill_score,
            'experience_match_score': exp_score,
            'education_match_score': 70.0 if education.degrees else 50.0,
            'cultural_fit_score': 60.0,
            'keyword_density_score': keyword_score,
            'matched_skills': matched_skills[:20],
            'missing_critical_skills': ['Unable to determine - LLM analysis failed'],
            'missing_preferred_skills': [],
            'additional_skills': all_skills[:10],
            'experience_gap': f'{experience.total_years} years total experience',
            'education_match': ', '.join(education.degrees) if education.degrees else 'Not specified',
            'strengths': ['Fallback analysis - manual review recommended'],
            'weaknesses': ['LLM analysis unavailable'],
            'red_flags': [],
            'recommendations': ['Manual review required - automated analysis incomplete'],
            'suggested_interview_questions': [
                'Tell me about your relevant experience',
                'What are your key technical skills?',
                'Why are you interested in this role?'
            ],
            'areas_to_probe': ['Technical depth', 'Experience relevance'],
            'executive_summary': 'Automated analysis incomplete. Manual review recommended.',
            'hiring_recommendation': 'MAYBE - Requires manual review'
        }
    
    def save_report(self, result: ATSMatchResult, output_folder: str):
        """Save detailed report to file"""
        Path(output_folder).mkdir(parents=True, exist_ok=True)
        
        # Save JSON
        safe_name = re.sub(r'[^\w\s-]', '', result.candidate_name).strip().replace(' ', '_')
        json_path = Path(output_folder) / f"{safe_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(asdict(result), f, indent=2, ensure_ascii=False)
        
        print(f"   💾 Saved detailed report: {json_path}")
    
    def _extract_name(self, text: str) -> str:
        """Extract name from resume text"""
        # Usually name is in first few lines
        lines = text.split('\n')[:5]
        for line in lines:
            line = line.strip()
            # Look for capitalized words (likely a name)
            if len(line) > 3 and len(line) < 50:
                words = line.split()
                if len(words) >= 2 and all(w[0].isupper() for w in words if w):
                    return line
        return "Unknown Candidate"
    
    def _extract_email(self, text: str) -> str:
        """Extract email from text"""
        pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        matches = re.findall(pattern, text)
        return matches[0] if matches else ""
    
    def _extract_phone(self, text: str) -> str:
        """Extract phone from text"""
        pattern = r'[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]'
        matches = re.findall(pattern, text)
        return matches[0] if matches else ""
    
    def _extract_linkedin(self, text: str) -> str:
        """Extract LinkedIn URL from text"""
        pattern = r'(?:https?://)?(?:www\.)?linkedin\.com/in/[A-Za-z0-9_-]+'
        matches = re.findall(pattern, text, re.IGNORECASE)
        return matches[0] if matches else ""
    
    def run(self):
        """Run the advanced ATS analysis"""
        print("\n" + "="*100)
        print("🚀 ADVANCED ATS MATCHER - Enterprise-Grade Resume Analysis with AI")
        print("="*100)
        
        if not self.client:
            print("\n❌ LLM not configured. Please set up your API key in ats_config.txt")
            print("   The advanced ATS requires an LLM for deep analysis.")
            return
        
        # Get paths from config
        resume_folder = self.config.get('RESUME_FOLDER', './data/resumes')
        job_desc_file = self.config.get('JOB_DESCRIPTION_FILE', './data/job_description.txt')
        min_score = float(self.config.get('MIN_MATCH_SCORE', '60'))
        output_folder = self.config.get('OUTPUT_FOLDER', './data/reports')
        
        # Check paths
        if not Path(resume_folder).exists():
            print(f"\n❌ Resume folder not found: {resume_folder}")
            return
        
        if not Path(job_desc_file).exists():
            print(f"\n❌ Job description file not found: {job_desc_file}")
            return
        
        # Load job description
        print(f"\n📋 Loading job description from: {job_desc_file}")
        with open(job_desc_file, 'r', encoding='utf-8') as f:
            job_desc = f.read()
        print(f"✓ Job description loaded ({len(job_desc)} characters)")
        
        # Find PDFs
        pdf_files = list(Path(resume_folder).glob('*.pdf'))
        if not pdf_files:
            print(f"\n❌ No PDF files found in: {resume_folder}")
            return
        
        print(f"\n📁 Found {len(pdf_files)} resume(s) to analyze")
        print("🤖 Using AI for deep semantic analysis...\n")
        
        # Process each resume
        results = []
        for i, pdf_file in enumerate(pdf_files, 1):
            print(f"\n{'='*100}")
            print(f"⏳ [{i}/{len(pdf_files)}] Processing: {pdf_file.name}")
            print(f"{'='*100}")
            
            # Extract text
            resume_text = self.extract_text_from_pdf(str(pdf_file))
            if not resume_text:
                print(f"   ⚠️  Could not extract text from {pdf_file.name}")
                continue
            
            print(f"✓ Extracted {len(resume_text)} characters from resume")
            
            # AI Analysis
            print("🤖 Analyzing candidate information...")
            candidate_info = self.extract_candidate_info(resume_text)
            
            print("🤖 Performing deep skill analysis...")
            skills = self.analyze_skills(resume_text, job_desc)
            
            print("🤖 Analyzing work experience...")
            experience = self.analyze_experience(resume_text, job_desc)
            
            print("🤖 Analyzing education...")
            education = self.analyze_education(resume_text)
            
            print("🤖 Calculating comprehensive match score...")
            result = self.calculate_match_score(
                resume_text, job_desc, candidate_info, 
                skills, experience, education
            )
            result.filename = pdf_file.name
            
            # Print report
            self.print_detailed_report(result)
            
            # Save report
            if self.config.get('SAVE_DETAILED_REPORTS', 'true').lower() == 'true':
                self.save_report(result, output_folder)
            
            results.append(result)
        
        # Summary
        if results:
            print("\n" + "="*100)
            print("📈 FINAL SUMMARY - All Candidates Ranked")
            print("="*100)
            
            # Sort by score
            results.sort(key=lambda x: x.overall_score, reverse=True)
            
            print(f"\n{'Rank':<6} {'Score':<8} {'Name':<30} {'Recommendation':<25} {'Status'}")
            print("-" * 100)
            
            for i, result in enumerate(results, 1):
                score = result.overall_score
                status = "✓ PASS" if score >= min_score else "✗ FAIL"
                rec = result.hiring_recommendation[:24]
                name = result.candidate_name[:29]
                print(f"{i:<6} {score:<8.1f} {name:<30} {rec:<25} {status}")
            
            # Statistics
            passed = sum(1 for r in results if r.overall_score >= min_score)
            strong_yes = sum(1 for r in results if 'STRONG_YES' in r.hiring_recommendation)
            yes_count = sum(1 for r in results if r.hiring_recommendation.startswith('YES'))
            
            print(f"\n📊 HIRING STATISTICS:")
            print(f"   • Total Candidates Analyzed:  {len(results)}")
            print(f"   • Strong Hire Recommendations: {strong_yes}")
            print(f"   • Hire Recommendations:        {yes_count}")
            print(f"   • Passed Threshold (≥{min_score}%):   {passed}")
            print(f"   • Failed Threshold (<{min_score}%):   {len(results) - passed}")
            print(f"   • Average Score:               {sum(r.overall_score for r in results) / len(results):.1f}%")
            print(f"   • Highest Score:               {results[0].overall_score}% ({results[0].candidate_name})")
            print(f"   • Lowest Score:                {results[-1].overall_score}% ({results[-1].candidate_name})")
            
            if self.config.get('SAVE_DETAILED_REPORTS', 'true').lower() == 'true':
                print(f"\n💾 Detailed reports saved to: {output_folder}")
        
        print("\n" + "="*100)
        print("✅ ADVANCED ATS ANALYSIS COMPLETE!")
        print("="*100 + "\n")


def main():
    """Main entry point"""
    ats = AdvancedATS()
    ats.run()


if __name__ == "__main__":
    main()
