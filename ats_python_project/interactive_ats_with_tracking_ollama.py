"""
Interactive ATS with Job Application Tracking (Ollama Version)
- Keeps resume in session
- Allows resume replacement
- Tracks job applications in Excel
- Works with Ollama local models
"""
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime

# Import from advanced_ats and job_tracker
from advanced_ats import AdvancedATS, ATSMatchResult
from job_tracker import JobTracker


class InteractiveATSWithTrackingOllama(AdvancedATS):
    """Interactive ATS with job application tracking - Ollama version"""
    
    def __init__(self, config_path: str = "ats_config_ollama.txt"):
        super().__init__(config_path)
        self.conversation_history = []
        self.current_resume_text = None
        self.current_resume_filename = None
        self.current_job_desc = None
        self.current_analysis = None
        self.job_tracker = JobTracker()
    
    def load_resume(self, resume_path: str) -> bool:
        """Load resume into session"""
        try:
            resume_text = self.extract_text_from_pdf(resume_path)
            if not resume_text:
                print(f"❌ Could not extract text from: {resume_path}")
                return False
            
            self.current_resume_text = resume_text
            self.current_resume_filename = Path(resume_path).name
            
            print(f"✅ Resume loaded: {self.current_resume_filename}")
            print(f"   Text length: {len(resume_text)} characters")
            
            return True
            
        except Exception as e:
            print(f"❌ Error loading resume: {str(e)}")
            return False
    
    def replace_resume(self) -> bool:
        """Allow user to replace current resume"""
        print("\n" + "="*100)
        print("📄 REPLACE RESUME")
        print("="*100)
        
        if self.current_resume_filename:
            print(f"\nCurrent resume: {self.current_resume_filename}")
        
        resume_path = input("\nEnter path to new resume PDF: ").strip()
        
        if not resume_path:
            print("❌ No path provided")
            return False
        
        resume_path = resume_path.strip('"').strip("'")
        
        if not Path(resume_path).exists():
            print(f"❌ File not found: {resume_path}")
            return False
        
        return self.load_resume(resume_path)
    
    def analyze_job(self, job_desc: str) -> Optional[ATSMatchResult]:
        """Analyze current resume against job description"""
        if not self.current_resume_text:
            print("❌ No resume loaded. Please load a resume first.")
            return None
        
        print("\n⏳ Analyzing resume against job description...")
        
        self.current_job_desc = job_desc
        
        # AI Analysis
        candidate_info = self.extract_candidate_info(self.current_resume_text)
        skills = self.analyze_skills(self.current_resume_text, job_desc)
        experience = self.analyze_experience(self.current_resume_text, job_desc)
        education = self.analyze_education(self.current_resume_text)
        
        result = self.calculate_match_score(
            self.current_resume_text, job_desc, candidate_info,
            skills, experience, education
        )
        result.filename = self.current_resume_filename
        
        self.current_analysis = result
        
        print(f"✅ Analysis complete!")
        
        return result
    
    def start_conversation(self, result: ATSMatchResult):
        """Start conversation about the analysis"""
        self.conversation_history = [
            {
                "role": "system",
                "content": f"""You are an expert HR consultant and technical recruiter. You have just analyzed a candidate's resume for a job position.

JOB DESCRIPTION:
{self.current_job_desc[:2000]}

CANDIDATE: {result.candidate_name}
OVERALL SCORE: {result.overall_score}%
HIRING RECOMMENDATION: {result.hiring_recommendation}

CANDIDATE SUMMARY:
- Experience: {result.candidate_experience.total_years} years total, {result.candidate_experience.relevant_experience_years} relevant
- Education: {', '.join(result.education.degrees) if result.education.degrees else 'Not specified'}
- Matched Skills: {', '.join(result.matched_skills[:15])}
- Missing Skills: {', '.join(result.missing_critical_skills[:10])}
- Strengths: {'; '.join(result.strengths[:3])}
- Concerns: {'; '.join(result.weaknesses[:3])}

FULL RESUME TEXT:
{self.current_resume_text[:6000]}

You can answer detailed questions about this candidate, provide insights, suggest interview strategies, compare with job requirements, and give hiring advice. Be specific, actionable, and reference actual details from the resume."""
            }
        ]
    
    def ask_question(self, question: str) -> str:
        """Ask a question about the current analysis"""
        if not self.current_analysis:
            return "No analysis available. Please analyze a job first."
        
        self.conversation_history.append({
            "role": "user",
            "content": question
        })
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=self.conversation_history,
                temperature=0.5,
                max_tokens=2000,
                extra_body={
                    "num_ctx": 8192
                }
            )
            
            answer = response.choices[0].message.content.strip()
            
            self.conversation_history.append({
                "role": "assistant",
                "content": answer
            })
            
            return answer
            
        except Exception as e:
            return f"Error getting response: {str(e)}"
    
    def ask_about_application(self) -> bool:
        """Ask user if they applied to the job and log it"""
        if not self.current_analysis:
            return False
        
        print("\n" + "="*100)
        print("📝 JOB APPLICATION TRACKING")
        print("="*100)
        
        company, job_title = self._extract_job_info()
        
        if self.job_tracker.check_if_applied(company, job_title):
            print(f"\n⚠️  You've already logged an application for:")
            print(f"   {job_title} at {company}")
            update = input("\nDo you want to log this again? (yes/no): ").strip().lower()
            if update not in ['yes', 'y']:
                return False
        
        applied = input(f"\n❓ Did you apply for this job? (yes/no): ").strip().lower()
        
        if applied in ['yes', 'y']:
            print(f"\n📋 Logging job application...")
            print(f"   Company: {company}")
            print(f"   Job Title: {job_title}")
            
            edit = input("\nEdit details? (yes/no): ").strip().lower()
            if edit in ['yes', 'y']:
                company = input(f"Company [{company}]: ").strip() or company
                job_title = input(f"Job Title [{job_title}]: ").strip() or job_title
            
            portal = input("Portal [LinkedIn]: ").strip() or "LinkedIn"
            emp_type = input("Employment Type [Full Time]: ").strip() or "Full Time"
            
            success = self.job_tracker.add_job_application(
                company=company,
                job_title=job_title,
                portal=portal,
                employment_type=emp_type
            )
            
            if success:
                total = self.job_tracker.get_application_count()
                print(f"\n🎯 Total applications tracked: {total}")
            
            return True
        
        return False
    
    def _extract_job_info(self) -> tuple:
        """Extract company and job title from job description"""
        if not self.current_job_desc:
            return ("Unknown Company", "Unknown Position")
        
        try:
            prompt = f"""Extract the company name and job title from this job description. 
Return ONLY in this format:
Company: [company name]
Job Title: [job title]

Job Description:
{self.current_job_desc[:1000]}"""
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=100,
                extra_body={"num_ctx": 4096}
            )
            
            result = response.choices[0].message.content.strip()
            
            company = "Unknown Company"
            job_title = "Unknown Position"
            
            for line in result.split('\n'):
                if line.startswith('Company:'):
                    company = line.replace('Company:', '').strip()
                elif line.startswith('Job Title:'):
                    job_title = line.replace('Job Title:', '').strip()
            
            return (company, job_title)
            
        except Exception as e:
            print(f"⚠️  Could not auto-extract job info: {str(e)}")
            return ("Unknown Company", "Unknown Position")
    
    def show_recent_applications(self):
        """Show recent job applications"""
        print("\n" + "="*100)
        print("📊 RECENT JOB APPLICATIONS")
        print("="*100)
        
        applications = self.job_tracker.get_recent_applications(limit=10)
        
        if not applications:
            print("\nNo applications tracked yet.")
            return
        
        print(f"\nTotal applications: {self.job_tracker.get_application_count()}")
        print("\nRecent applications:")
        print("-" * 100)
        
        for i, app in enumerate(applications, 1):
            print(f"\n{i}. {app['job']} at {app['company']}")
            print(f"   Portal: {app['portal']} | Type: {app['type']} | Date: {app['date']}")
        
        print("="*100)
    
    def run_interactive_session(self):
        """Run interactive session with job tracking"""
        print("\n" + "="*100)
        print("🚀 INTERACTIVE ATS WITH JOB TRACKING (OLLAMA)")
        print("="*100)
        print("\nFeatures:")
        print("  • Keep your resume in session")
        print("  • Analyze multiple jobs with the same resume")
        print("  • Track job applications in Excel")
        print("  • Get AI-powered insights")
        print("="*100)
        
        if not self.client:
            print("\n❌ LLM not configured. Please set up Ollama")
            return
        
        print("\n📄 STEP 1: Load Your Resume")
        print("-" * 100)
        
        resume_path = input("Enter path to your resume PDF: ").strip()
        resume_path = resume_path.strip('"').strip("'")
        
        if not self.load_resume(resume_path):
            return
        
        while True:
            print("\n" + "="*100)
            print("📋 MAIN MENU")
            print("="*100)
            print(f"\nCurrent resume: {self.current_resume_filename}")
            print(f"Applications tracked: {self.job_tracker.get_application_count()}")
            print("\nOptions:")
            print("  1. Analyze a new job")
            print("  2. Replace resume")
            print("  3. View recent applications")
            print("  4. Ask questions about last analysis")
            print("  5. Quit")
            print("="*100)
            
            choice = input("\nSelect option (1-5): ").strip()
            
            if choice == '1':
                self._analyze_new_job()
            elif choice == '2':
                self.replace_resume()
            elif choice == '3':
                self.show_recent_applications()
            elif choice == '4':
                self._qa_session()
            elif choice == '5':
                print("\n👋 Goodbye!")
                break
            else:
                print("❌ Invalid option")
    
    def _analyze_new_job(self):
        """Analyze a new job"""
        print("\n" + "="*100)
        print("🔍 ANALYZE NEW JOB")
        print("="*100)
        
        print("\nEnter job description (paste and press Enter twice when done):")
        print("-" * 100)
        
        lines = []
        empty_count = 0
        
        while True:
            try:
                line = input()
                if not line:
                    empty_count += 1
                    if empty_count >= 2:
                        break
                else:
                    empty_count = 0
                    lines.append(line)
            except EOFError:
                break
        
        job_desc = '\n'.join(lines)
        
        if not job_desc.strip():
            print("❌ No job description provided")
            return
        
        result = self.analyze_job(job_desc)
        
        if result:
            self.print_detailed_report(result)
            self.start_conversation(result)
            self.ask_about_application()
    
    def _qa_session(self):
        """Q&A session about last analysis"""
        if not self.current_analysis:
            print("\n❌ No analysis available. Please analyze a job first.")
            return
        
        print("\n" + "="*100)
        print(f"💬 Q&A SESSION - {self.current_analysis.candidate_name}")
        print("="*100)
        print(f"\nScore: {self.current_analysis.overall_score}%")
        print(f"Recommendation: {self.current_analysis.hiring_recommendation}")
        print("\nAsk questions about the analysis. Type 'back' to return to menu.")
        print("="*100 + "\n")
        
        while True:
            try:
                question = input("❓ Your question: ").strip()
                
                if not question:
                    continue
                
                if question.lower() in ['back', 'exit', 'quit', 'menu']:
                    break
                
                print("\n🤖 AI Response:")
                print("-" * 100)
                answer = self.ask_question(question)
                print(answer)
                print("-" * 100 + "\n")
                
            except KeyboardInterrupt:
                break
            except EOFError:
                break


def main():
    """Main entry point"""
    ats = InteractiveATSWithTrackingOllama()
    ats.run_interactive_session()


if __name__ == "__main__":
    main()
