"""
Matching algorithms for ATS candidate-job matching
"""
import re
from typing import List, Set, Dict, Any
from fuzzywuzzy import fuzz, process
from models.ats_models import Candidate, JobPosting, MatchScore
from loguru import logger


class MatchingAlgorithms:
    """Collection of algorithms for matching candidates to jobs"""
    
    def __init__(self):
        self.skill_synonyms = self._load_skill_synonyms()
        self.education_levels = {
            "high school": 1,
            "associate": 2,
            "bachelor": 3,
            "master": 4,
            "phd": 5,
            "doctorate": 5
        }
    
    def _load_skill_synonyms(self) -> Dict[str, List[str]]:
        """Load skill synonyms for better matching"""
        return {
            "python": ["python", "py", "python3"],
            "javascript": ["javascript", "js", "node.js", "nodejs", "ecmascript"],
            "java": ["java", "openjdk", "oracle java"],
            "react": ["react", "reactjs", "react.js"],
            "angular": ["angular", "angularjs", "angular.js"],
            "vue": ["vue", "vuejs", "vue.js"],
            "sql": ["sql", "mysql", "postgresql", "sqlite", "mssql"],
            "aws": ["aws", "amazon web services", "amazon aws"],
            "docker": ["docker", "containerization", "containers"],
            "kubernetes": ["kubernetes", "k8s", "container orchestration"],
            "machine learning": ["machine learning", "ml", "artificial intelligence", "ai"],
            "data science": ["data science", "data analysis", "analytics"],
            "project management": ["project management", "pm", "pmp", "agile", "scrum"]
        }
    
    def normalize_skills(self, skills: List[str]) -> Set[str]:
        """Normalize skills using synonyms and standardization"""
        normalized = set()
        
        for skill in skills:
            skill_lower = skill.lower().strip()
            
            # Check if skill matches any synonym group
            found_match = False
            for standard_skill, synonyms in self.skill_synonyms.items():
                if skill_lower in [s.lower() for s in synonyms]:
                    normalized.add(standard_skill)
                    found_match = True
                    break
            
            # If no synonym found, add the original skill
            if not found_match:
                normalized.add(skill_lower)
        
        return normalized
    
    def calculate_skill_match_score(
        self, 
        candidate_skills: List[str], 
        required_skills: List[str],
        preferred_skills: List[str] = None
    ) -> Dict[str, Any]:
        """Calculate skill match score between candidate and job requirements"""
        if preferred_skills is None:
            preferred_skills = []
        
        # Normalize skills
        candidate_skills_norm = self.normalize_skills(candidate_skills)
        required_skills_norm = self.normalize_skills(required_skills)
        preferred_skills_norm = self.normalize_skills(preferred_skills)
        
        # Calculate matches
        required_matches = candidate_skills_norm.intersection(required_skills_norm)
        preferred_matches = candidate_skills_norm.intersection(preferred_skills_norm)
        
        # Calculate scores
        required_score = 0
        if required_skills_norm:
            required_score = (len(required_matches) / len(required_skills_norm)) * 100
        
        preferred_score = 0
        if preferred_skills_norm:
            preferred_score = (len(preferred_matches) / len(preferred_skills_norm)) * 100
        
        # Overall skill score (weighted: 70% required, 30% preferred)
        overall_skill_score = (required_score * 0.7) + (preferred_score * 0.3)
        
        # Find missing skills
        missing_required = required_skills_norm - candidate_skills_norm
        missing_preferred = preferred_skills_norm - candidate_skills_norm
        
        return {
            "score": overall_skill_score,
            "required_score": required_score,
            "preferred_score": preferred_score,
            "matched_required": list(required_matches),
            "matched_preferred": list(preferred_matches),
            "missing_required": list(missing_required),
            "missing_preferred": list(missing_preferred)
        }
    
    def calculate_experience_match_score(
        self, 
        candidate_years: int, 
        job_description: str
    ) -> Dict[str, Any]:
        """Calculate experience match score"""
        # Extract required years from job description
        required_years = self._extract_required_experience(job_description)
        
        if required_years is None:
            return {"score": 50, "required_years": None, "candidate_years": candidate_years}
        
        if candidate_years is None:
            return {"score": 25, "required_years": required_years, "candidate_years": None}
        
        # Calculate score based on experience gap
        if candidate_years >= required_years:
            # Bonus for more experience, but diminishing returns
            excess = candidate_years - required_years
            bonus = min(excess * 5, 25)  # Max 25 bonus points
            score = min(100, 75 + bonus)
        else:
            # Penalty for less experience
            gap = required_years - candidate_years
            penalty = gap * 15  # 15 points per year short
            score = max(0, 75 - penalty)
        
        return {
            "score": score,
            "required_years": required_years,
            "candidate_years": candidate_years,
            "gap": candidate_years - required_years if candidate_years else None
        }
    
    def _extract_required_experience(self, job_description: str) -> int:
        """Extract required years of experience from job description"""
        patterns = [
            r'(\d+)\+?\s*years?\s+(?:of\s+)?experience',
            r'(\d+)\+?\s*yrs?\s+(?:of\s+)?experience',
            r'minimum\s+(?:of\s+)?(\d+)\s+years?',
            r'at\s+least\s+(\d+)\s+years?',
            r'(\d+)\+?\s*years?\s+in'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, job_description.lower())
            if match:
                return int(match.group(1))
        
        return None
    
    def calculate_education_match_score(
        self, 
        candidate_education: List[Dict[str, str]], 
        job_description: str
    ) -> Dict[str, Any]:
        """Calculate education match score"""
        required_education = self._extract_required_education(job_description)
        
        if not required_education:
            return {"score": 50, "required_education": None}
        
        if not candidate_education:
            return {"score": 25, "required_education": required_education}
        
        # Get highest education level of candidate
        candidate_level = 0
        for edu in candidate_education:
            degree = edu.get("degree", "").lower()
            for level_name, level_value in self.education_levels.items():
                if level_name in degree:
                    candidate_level = max(candidate_level, level_value)
                    break
        
        # Get required education level
        required_level = 0
        for level_name, level_value in self.education_levels.items():
            if level_name in required_education.lower():
                required_level = level_value
                break
        
        # Calculate score
        if candidate_level >= required_level:
            score = 85 + min((candidate_level - required_level) * 5, 15)
        else:
            gap = required_level - candidate_level
            score = max(0, 85 - (gap * 20))
        
        return {
            "score": min(100, score),
            "candidate_level": candidate_level,
            "required_level": required_level,
            "required_education": required_education
        }
    
    def _extract_required_education(self, job_description: str) -> str:
        """Extract required education from job description"""
        education_patterns = [
            r'(bachelor[\'s]*|ba|bs|b\.s|b\.a)\s+(?:degree|in)',
            r'(master[\'s]*|ma|ms|m\.s|m\.a|mba)\s+(?:degree|in)',
            r'(phd|ph\.d|doctorate|doctoral)\s+(?:degree|in)',
            r'(associate[\'s]*|aa|as)\s+(?:degree|in)',
            r'(high\s+school|diploma|ged)'
        ]
        
        text = job_description.lower()
        for pattern in education_patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(1)
        
        return ""
    
    def calculate_text_similarity(self, text1: str, text2: str) -> float:
        """Calculate similarity between two texts using fuzzy matching"""
        if not text1 or not text2:
            return 0.0
        
        # Clean texts
        text1_clean = re.sub(r'[^\w\s]', ' ', text1.lower())
        text2_clean = re.sub(r'[^\w\s]', ' ', text2.lower())
        
        # Calculate different similarity metrics
        ratio = fuzz.ratio(text1_clean, text2_clean)
        partial_ratio = fuzz.partial_ratio(text1_clean, text2_clean)
        token_sort_ratio = fuzz.token_sort_ratio(text1_clean, text2_clean)
        token_set_ratio = fuzz.token_set_ratio(text1_clean, text2_clean)
        
        # Weighted average
        similarity = (ratio * 0.2 + partial_ratio * 0.2 + 
                     token_sort_ratio * 0.3 + token_set_ratio * 0.3)
        
        return similarity
    
    def calculate_basic_match_score(
        self, 
        candidate: Candidate, 
        job: JobPosting
    ) -> MatchScore:
        """Calculate basic match score using rule-based algorithms"""
        try:
            # Calculate skill match
            skill_match = self.calculate_skill_match_score(
                candidate.skills,
                job.required_skills,
                job.preferred_skills
            )
            
            # Calculate experience match
            experience_match = self.calculate_experience_match_score(
                candidate.years_of_experience or 0,
                job.description
            )
            
            # Calculate education match
            education_data = [{"degree": edu.degree} for edu in candidate.education]
            education_match = self.calculate_education_match_score(
                education_data,
                job.description
            )
            
            # Calculate overall score (weighted average)
            overall_score = (
                skill_match["score"] * 0.5 +
                experience_match["score"] * 0.3 +
                education_match["score"] * 0.2
            )
            
            # Generate recommendations
            recommendations = []
            if skill_match["missing_required"]:
                recommendations.append(
                    f"Consider developing skills in: {', '.join(skill_match['missing_required'][:3])}"
                )
            
            if experience_match.get("gap", 0) < 0:
                recommendations.append(
                    f"Gain {abs(experience_match['gap'])} more years of relevant experience"
                )
            
            # Generate strengths
            strengths = []
            if skill_match["matched_required"]:
                strengths.append(f"Strong match in required skills: {', '.join(skill_match['matched_required'][:3])}")
            
            if experience_match.get("gap", 0) > 0:
                strengths.append(f"Exceeds experience requirements by {experience_match['gap']} years")
            
            return MatchScore(
                overall_score=round(overall_score, 1),
                skill_match_score=round(skill_match["score"], 1),
                experience_match_score=round(experience_match["score"], 1),
                education_match_score=round(education_match["score"], 1),
                matched_skills=skill_match["matched_required"] + skill_match["matched_preferred"],
                missing_skills=skill_match["missing_required"] + skill_match["missing_preferred"],
                strengths=strengths,
                recommendations=recommendations
            )
            
        except Exception as e:
            logger.error(f"Error calculating basic match score: {str(e)}")
            return MatchScore(overall_score=0)
    
    def rank_candidates(
        self, 
        candidates: List[Candidate], 
        job: JobPosting
    ) -> List[tuple]:
        """Rank candidates for a job posting"""
        candidate_scores = []
        
        for candidate in candidates:
            match_score = self.calculate_basic_match_score(candidate, job)
            candidate_scores.append((candidate, match_score))
        
        # Sort by overall score (descending)
        candidate_scores.sort(key=lambda x: x[1].overall_score, reverse=True)
        
        return candidate_scores
    
    def find_similar_candidates(
        self, 
        target_candidate: Candidate, 
        candidate_pool: List[Candidate],
        similarity_threshold: float = 0.7
    ) -> List[tuple]:
        """Find candidates similar to the target candidate"""
        similar_candidates = []
        
        target_skills = set(self.normalize_skills(target_candidate.skills))
        
        for candidate in candidate_pool:
            if candidate.id == target_candidate.id:
                continue
            
            candidate_skills = set(self.normalize_skills(candidate.skills))
            
            # Calculate Jaccard similarity for skills
            intersection = len(target_skills.intersection(candidate_skills))
            union = len(target_skills.union(candidate_skills))
            
            if union > 0:
                similarity = intersection / union
                
                if similarity >= similarity_threshold:
                    similar_candidates.append((candidate, similarity))
        
        # Sort by similarity (descending)
        similar_candidates.sort(key=lambda x: x[1], reverse=True)
        
        return similar_candidates
