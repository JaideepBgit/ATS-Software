"""
Simple ATS Matcher - Works like real company ATS systems
Reads resume PDFs and job descriptions, shows matching analysis
"""
import os
import re
from pathlib import Path
from typing import Dict, List, Set, Tuple
import PyPDF2
from collections import Counter


class SimpleATS:
    """Simple ATS that matches resumes against job descriptions"""
    
    def __init__(self, config_path: str = "ats_config.txt"):
        self.config = self.load_config(config_path)
        self.skill_synonyms = {
            'python': ['python', 'py', 'python3'],
            'javascript': ['javascript', 'js', 'node.js', 'nodejs', 'node'],
            'react': ['react', 'reactjs', 'react.js'],
            'angular': ['angular', 'angularjs'],
            'vue': ['vue', 'vuejs', 'vue.js'],
            'java': ['java', 'jdk', 'jre'],
            'c++': ['c++', 'cpp', 'cplusplus'],
            'c#': ['c#', 'csharp', 'c sharp'],
            'sql': ['sql', 'mysql', 'postgresql', 'postgres', 'sqlite'],
            'aws': ['aws', 'amazon web services'],
            'docker': ['docker', 'containerization'],
            'kubernetes': ['kubernetes', 'k8s'],
            'git': ['git', 'github', 'gitlab', 'version control'],
            'machine learning': ['machine learning', 'ml', 'deep learning', 'ai'],
            'data science': ['data science', 'data analysis', 'analytics'],
        }
    
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
        default_config = """# ATS Configuration File
# Specify paths to your resume folder and job description file

# Path to folder containing resume PDFs
RESUME_FOLDER=./data/resumes

# Path to job description text file
JOB_DESCRIPTION_FILE=./data/job_description.txt

# Minimum match score to consider (0-100)
MIN_MATCH_SCORE=60
"""
        with open(config_path, 'w', encoding='utf-8') as f:
            f.write(default_config)
        
        print(f"✓ Created default config at: {config_path}")
        print("Please update the paths in the config file and run again.")
    
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extract text from PDF file"""
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text()
                return text
        except Exception as e:
            print(f"❌ Error reading PDF {pdf_path}: {str(e)}")
            return ""
    
    def extract_skills(self, text: str) -> Set[str]:
        """Extract skills from text"""
        text_lower = text.lower()
        found_skills = set()
        
        # Check for each skill and its synonyms
        for main_skill, synonyms in self.skill_synonyms.items():
            for synonym in synonyms:
                # Use word boundaries to avoid partial matches
                pattern = r'\b' + re.escape(synonym) + r'\b'
                if re.search(pattern, text_lower):
                    found_skills.add(main_skill)
                    break
        
        # Also extract common technical terms
        tech_patterns = [
            r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b',  # Capitalized words
            r'\b[A-Z]{2,}\b',  # Acronyms
        ]
        
        for pattern in tech_patterns:
            matches = re.findall(pattern, text)
            for match in matches:
                match_lower = match.lower()
                # Add if it looks like a skill (not common words)
                if len(match) > 2 and match_lower not in ['the', 'and', 'for', 'with']:
                    found_skills.add(match_lower)
        
        return found_skills
    
    def extract_experience_years(self, text: str) -> int:
        """Extract years of experience from text"""
        patterns = [
            r'(\d+)\+?\s*(?:years?|yrs?)\s*(?:of)?\s*experience',
            r'experience\s*(?:of)?\s*(\d+)\+?\s*(?:years?|yrs?)',
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text.lower())
            if matches:
                return max([int(m) for m in matches])
        
        return 0
    
    def calculate_match_score(self, resume_text: str, job_desc_text: str) -> Dict:
        """Calculate ATS match score between resume and job description"""
        
        # Extract skills
        resume_skills = self.extract_skills(resume_text)
        job_skills = self.extract_skills(job_desc_text)
        
        # Find matches and missing
        matched_skills = resume_skills.intersection(job_skills)
        missing_skills = job_skills - resume_skills
        extra_skills = resume_skills - job_skills
        
        # Calculate skill match percentage
        if len(job_skills) > 0:
            skill_match_pct = (len(matched_skills) / len(job_skills)) * 100
        else:
            skill_match_pct = 0
        
        # Extract experience
        resume_exp = self.extract_experience_years(resume_text)
        job_exp = self.extract_experience_years(job_desc_text)
        
        # Calculate experience match
        if job_exp > 0:
            exp_match_pct = min((resume_exp / job_exp) * 100, 100)
        else:
            exp_match_pct = 100
        
        # Calculate keyword density
        job_keywords = set(job_desc_text.lower().split())
        resume_keywords = set(resume_text.lower().split())
        keyword_match = len(job_keywords.intersection(resume_keywords))
        keyword_density = (keyword_match / len(job_keywords)) * 100 if job_keywords else 0
        
        # Overall ATS score (weighted average)
        overall_score = (
            skill_match_pct * 0.5 +  # Skills are 50% of score
            exp_match_pct * 0.2 +     # Experience is 20%
            keyword_density * 0.3      # Keyword density is 30%
        )
        
        return {
            'overall_score': round(overall_score, 2),
            'skill_match_score': round(skill_match_pct, 2),
            'experience_match_score': round(exp_match_pct, 2),
            'keyword_density_score': round(keyword_density, 2),
            'matched_skills': sorted(list(matched_skills)),
            'missing_skills': sorted(list(missing_skills)),
            'extra_skills': sorted(list(extra_skills)),
            'resume_experience': resume_exp,
            'required_experience': job_exp,
        }
    
    def print_match_report(self, filename: str, match_data: Dict):
        """Print a formatted match report"""
        print("\n" + "="*80)
        print(f"📄 RESUME: {filename}")
        print("="*80)
        
        # Overall Score
        score = match_data['overall_score']
        if score >= 80:
            score_emoji = "🟢"
            rating = "EXCELLENT MATCH"
        elif score >= 60:
            score_emoji = "🟡"
            rating = "GOOD MATCH"
        elif score >= 40:
            score_emoji = "🟠"
            rating = "MODERATE MATCH"
        else:
            score_emoji = "🔴"
            rating = "POOR MATCH"
        
        print(f"\n{score_emoji} ATS MATCH SCORE: {score}% - {rating}")
        
        # Detailed Scores
        print(f"\n📊 DETAILED BREAKDOWN:")
        print(f"   • Skills Match:      {match_data['skill_match_score']}%")
        print(f"   • Experience Match:  {match_data['experience_match_score']}%")
        print(f"   • Keyword Density:   {match_data['keyword_density_score']}%")
        
        # Experience
        print(f"\n💼 EXPERIENCE:")
        print(f"   • Resume:   {match_data['resume_experience']} years")
        print(f"   • Required: {match_data['required_experience']} years")
        
        # Matched Skills
        if match_data['matched_skills']:
            print(f"\n✅ MATCHING SKILLS ({len(match_data['matched_skills'])}):")
            for skill in match_data['matched_skills'][:15]:  # Show top 15
                print(f"   • {skill}")
            if len(match_data['matched_skills']) > 15:
                print(f"   ... and {len(match_data['matched_skills']) - 15} more")
        
        # Missing Skills
        if match_data['missing_skills']:
            print(f"\n❌ MISSING REQUIRED SKILLS ({len(match_data['missing_skills'])}):")
            for skill in match_data['missing_skills'][:15]:  # Show top 15
                print(f"   • {skill}")
            if len(match_data['missing_skills']) > 15:
                print(f"   ... and {len(match_data['missing_skills']) - 15} more")
        
        # Extra Skills
        if match_data['extra_skills'] and len(match_data['extra_skills']) <= 10:
            print(f"\n➕ ADDITIONAL SKILLS (Not in job description):")
            for skill in sorted(match_data['extra_skills'])[:10]:
                print(f"   • {skill}")
        
        print("\n" + "="*80)
    
    def run(self):
        """Run the ATS matching process"""
        print("\n" + "="*80)
        print("🎯 SIMPLE ATS MATCHER - Resume Analysis System")
        print("="*80)
        
        # Get paths from config
        resume_folder = self.config.get('RESUME_FOLDER', './data/resumes')
        job_desc_file = self.config.get('JOB_DESCRIPTION_FILE', './data/job_description.txt')
        min_score = float(self.config.get('MIN_MATCH_SCORE', '60'))
        
        # Check if paths exist
        if not Path(resume_folder).exists():
            print(f"\n❌ Resume folder not found: {resume_folder}")
            print("Please create the folder and add PDF resumes, or update the config file.")
            return
        
        if not Path(job_desc_file).exists():
            print(f"\n❌ Job description file not found: {job_desc_file}")
            print("Please create the file with the job description, or update the config file.")
            return
        
        # Load job description
        print(f"\n📋 Loading job description from: {job_desc_file}")
        with open(job_desc_file, 'r', encoding='utf-8') as f:
            job_desc_text = f.read()
        
        print(f"✓ Job description loaded ({len(job_desc_text)} characters)")
        
        # Find all PDF files
        pdf_files = list(Path(resume_folder).glob('*.pdf'))
        
        if not pdf_files:
            print(f"\n❌ No PDF files found in: {resume_folder}")
            return
        
        print(f"\n📁 Found {len(pdf_files)} resume(s) to analyze")
        
        # Process each resume
        results = []
        for pdf_file in pdf_files:
            print(f"\n⏳ Processing: {pdf_file.name}...")
            
            resume_text = self.extract_text_from_pdf(str(pdf_file))
            
            if not resume_text:
                print(f"   ⚠️  Could not extract text from {pdf_file.name}")
                continue
            
            match_data = self.calculate_match_score(resume_text, job_desc_text)
            match_data['filename'] = pdf_file.name
            results.append(match_data)
            
            self.print_match_report(pdf_file.name, match_data)
        
        # Summary
        if results:
            print("\n" + "="*80)
            print("📈 SUMMARY - All Candidates")
            print("="*80)
            
            # Sort by score
            results.sort(key=lambda x: x['overall_score'], reverse=True)
            
            print(f"\n{'Rank':<6} {'Score':<8} {'Resume':<40} {'Status'}")
            print("-" * 80)
            
            for i, result in enumerate(results, 1):
                score = result['overall_score']
                status = "✓ PASS" if score >= min_score else "✗ FAIL"
                print(f"{i:<6} {score:<8.1f} {result['filename']:<40} {status}")
            
            # Statistics
            passed = sum(1 for r in results if r['overall_score'] >= min_score)
            print(f"\n📊 Statistics:")
            print(f"   • Total Resumes:  {len(results)}")
            print(f"   • Passed (≥{min_score}%): {passed}")
            print(f"   • Failed (<{min_score}%): {len(results) - passed}")
            print(f"   • Average Score:  {sum(r['overall_score'] for r in results) / len(results):.1f}%")
            print(f"   • Highest Score:  {results[0]['overall_score']}%")
            print(f"   • Lowest Score:   {results[-1]['overall_score']}%")
        
        print("\n" + "="*80)
        print("✓ Analysis Complete!")
        print("="*80 + "\n")


def main():
    """Main entry point"""
    ats = SimpleATS()
    ats.run()


if __name__ == "__main__":
    main()
