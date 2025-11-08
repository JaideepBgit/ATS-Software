"""
LM Studio integration service for ATS functionality
"""
import json
import httpx
from typing import Dict, List, Optional, Any
from loguru import logger
from config.settings import settings


class LMStudioService:
    """Service for interacting with LM Studio local models"""
    
    def __init__(self):
        self.base_url = settings.lm_studio_base_url
        self.api_key = settings.lm_studio_api_key
        self.model_name = settings.lm_studio_model_name
        self.client = httpx.AsyncClient(timeout=30.0)
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.aclose()
    
    async def generate_completion(
        self, 
        prompt: str, 
        max_tokens: int = 1000,
        temperature: float = 0.7,
        system_message: Optional[str] = None
    ) -> Optional[str]:
        """Generate completion using LM Studio"""
        try:
            messages = []
            if system_message:
                messages.append({"role": "system", "content": system_message})
            messages.append({"role": "user", "content": prompt})
            
            payload = {
                "model": self.model_name,
                "messages": messages,
                "max_tokens": max_tokens,
                "temperature": temperature,
                "stream": False
            }
            
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            response = await self.client.post(
                f"{self.base_url}/chat/completions",
                json=payload,
                headers=headers
            )
            
            if response.status_code == 200:
                result = response.json()
                return result["choices"][0]["message"]["content"]
            else:
                logger.error(f"LM Studio API error: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            logger.error(f"Error generating completion: {str(e)}")
            return None
    
    async def extract_resume_skills(self, resume_text: str) -> List[str]:
        """Extract skills from resume text using LM Studio"""
        system_message = """You are an expert ATS system. Extract technical skills, soft skills, and competencies from the given resume text. Return only a JSON list of skills, no additional text."""
        
        prompt = f"""
        Extract all skills from this resume text:
        
        {resume_text}
        
        Return format: ["skill1", "skill2", "skill3", ...]
        """
        
        response = await self.generate_completion(
            prompt=prompt,
            system_message=system_message,
            max_tokens=500,
            temperature=0.3
        )
        
        if response:
            try:
                # Try to parse JSON response
                skills = json.loads(response.strip())
                return skills if isinstance(skills, list) else []
            except json.JSONDecodeError:
                # Fallback: extract skills from text response
                lines = response.strip().split('\n')
                skills = []
                for line in lines:
                    if line.strip() and not line.startswith('#'):
                        skills.append(line.strip().strip('-').strip())
                return skills
        
        return []
    
    async def calculate_job_match_score(
        self, 
        resume_text: str, 
        job_description: str
    ) -> Dict[str, Any]:
        """Calculate match score between resume and job description"""
        system_message = """You are an expert ATS system. Analyze the match between a resume and job description. Provide a detailed analysis with a numerical score (0-100) and specific reasons."""
        
        prompt = f"""
        Analyze the match between this resume and job description:
        
        RESUME:
        {resume_text}
        
        JOB DESCRIPTION:
        {job_description}
        
        Provide analysis in this JSON format:
        {{
            "overall_score": 85,
            "skill_match_score": 90,
            "experience_match_score": 80,
            "education_match_score": 85,
            "matched_skills": ["skill1", "skill2"],
            "missing_skills": ["skill3", "skill4"],
            "strengths": ["strength1", "strength2"],
            "recommendations": ["recommendation1", "recommendation2"]
        }}
        """
        
        response = await self.generate_completion(
            prompt=prompt,
            system_message=system_message,
            max_tokens=800,
            temperature=0.3
        )
        
        if response:
            try:
                return json.loads(response.strip())
            except json.JSONDecodeError:
                logger.error("Failed to parse job match response as JSON")
                return {
                    "overall_score": 0,
                    "skill_match_score": 0,
                    "experience_match_score": 0,
                    "education_match_score": 0,
                    "matched_skills": [],
                    "missing_skills": [],
                    "strengths": [],
                    "recommendations": []
                }
        
        return {}
    
    async def generate_interview_questions(
        self, 
        resume_text: str, 
        job_description: str,
        num_questions: int = 5
    ) -> List[str]:
        """Generate interview questions based on resume and job description"""
        system_message = """You are an expert HR interviewer. Generate relevant interview questions based on the candidate's resume and the job requirements."""
        
        prompt = f"""
        Generate {num_questions} interview questions for this candidate:
        
        RESUME:
        {resume_text}
        
        JOB DESCRIPTION:
        {job_description}
        
        Return as a JSON list: ["question1", "question2", ...]
        """
        
        response = await self.generate_completion(
            prompt=prompt,
            system_message=system_message,
            max_tokens=600,
            temperature=0.7
        )
        
        if response:
            try:
                questions = json.loads(response.strip())
                return questions if isinstance(questions, list) else []
            except json.JSONDecodeError:
                # Fallback: extract questions from text
                lines = response.strip().split('\n')
                questions = []
                for line in lines:
                    if line.strip() and ('?' in line or line.startswith(('1.', '2.', '3.', '4.', '5.'))):
                        questions.append(line.strip())
                return questions[:num_questions]
        
        return []
    
    async def health_check(self) -> bool:
        """Check if LM Studio is accessible"""
        try:
            response = await self.client.get(f"{self.base_url}/models")
            return response.status_code == 200
        except Exception as e:
            logger.error(f"LM Studio health check failed: {str(e)}")
            return False
