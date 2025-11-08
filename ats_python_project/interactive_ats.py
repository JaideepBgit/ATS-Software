"""
Interactive ATS - Chat with AI about candidates
Extends the advanced ATS with interactive Q&A capabilities
Maintains full context for multi-turn conversations
"""
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime

# Import from advanced_ats
from advanced_ats import AdvancedATS, ATSMatchResult


class InteractiveATS(AdvancedATS):
    """Interactive ATS with conversational capabilities"""
    
    def __init__(self, config_path: str = "ats_config.txt"):
        super().__init__(config_path)
        self.conversation_history = []
        self.current_candidate = None
        self.current_resume_text = None
        self.current_job_desc = None
        self.all_results = []
    
    def start_conversation(self, candidate_result: ATSMatchResult, resume_text: str, job_desc: str):
        """Start a new conversation about a candidate"""
        self.current_candidate = candidate_result
        self.current_resume_text = resume_text
        self.current_job_desc = job_desc
        
        # Initialize conversation with context
        self.conversation_history = [
            {
                "role": "system",
                "content": f"""You are an expert HR consultant and technical recruiter. You have just analyzed a candidate's resume for a job position.

JOB DESCRIPTION:
{job_desc[:2000]}

CANDIDATE: {candidate_result.candidate_name}
OVERALL SCORE: {candidate_result.overall_score}%
HIRING RECOMMENDATION: {candidate_result.hiring_recommendation}

CANDIDATE SUMMARY:
- Experience: {candidate_result.candidate_experience.total_years} years total, {candidate_result.candidate_experience.relevant_experience_years} relevant
- Education: {', '.join(candidate_result.education.degrees) if candidate_result.education.degrees else 'Not specified'}
- Matched Skills: {', '.join(candidate_result.matched_skills[:15])}
- Missing Skills: {', '.join(candidate_result.missing_critical_skills[:10])}
- Strengths: {'; '.join(candidate_result.strengths[:3])}
- Concerns: {'; '.join(candidate_result.weaknesses[:3])}

FULL RESUME TEXT:
{resume_text[:6000]}

You can answer detailed questions about this candidate, provide insights, suggest interview strategies, compare with job requirements, and give hiring advice. Be specific, actionable, and reference actual details from the resume."""
            }
        ]
    
    def ask_question(self, question: str) -> str:
        """Ask a question about the current candidate"""
        if not self.current_candidate:
            return "No candidate selected. Please run analysis first."
        
        # Add user question to history
        self.conversation_history.append({
            "role": "user",
            "content": question
        })
        
        # Get AI response
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=self.conversation_history,
                temperature=0.5,
                max_tokens=2000
            )
            
            answer = response.choices[0].message.content.strip()
            
            # Add AI response to history
            self.conversation_history.append({
                "role": "assistant",
                "content": answer
            })
            
            return answer
            
        except Exception as e:
            return f"Error getting response: {str(e)}"
    
    def resume_improvement_mode(self, candidate_result: ATSMatchResult, resume_text: str, job_desc: str):
        """Interactive mode for candidates to improve their resume"""
        self.start_conversation(candidate_result, resume_text, job_desc)
        
        # Add resume improvement context
        improvement_context = f"""
ADDITIONAL CONTEXT: The person asking questions IS the candidate whose resume was analyzed. They want to understand:
1. WHY certain aspects of their resume were flagged as concerns
2. HOW to improve specific resume points to better match the job
3. WHAT changes would increase their match score
4. WHICH skills or experiences to emphasize more

When answering:
- Be constructive and encouraging
- Provide SPECIFIC before/after examples for resume bullet points
- Explain the reasoning behind each suggestion
- Show how changes align with job requirements
- Give actionable, concrete advice they can implement immediately
- Reference specific parts of their resume and suggest improvements
"""
        
        self.conversation_history.append({
            "role": "system",
            "content": improvement_context
        })
        
        print("\n" + "="*100)
        print(f"📝 RESUME IMPROVEMENT MODE - {candidate_result.candidate_name}")
        print("="*100)
        print(f"\nYour Resume Score: {candidate_result.overall_score}% | {candidate_result.hiring_recommendation}")
        print("\n🎯 Get personalized advice to improve your resume for this job!")
        print("\nExample questions you can ask:")
        print("  • Why was my experience flagged as a concern?")
        print("  • How can I better highlight my Python skills?")
        print("  • What's wrong with my current resume bullet points?")
        print("  • Which missing skills should I add to my resume?")
        print("  • How can I rewrite my experience to match this job better?")
        print("  • What keywords am I missing?")
        print("  • Show me before/after examples for my work experience")
        print("  • How can I emphasize my leadership experience?")
        print("  • What should I remove from my resume?")
        print("  • How can I increase my score to 90%+?")
        print("\nType 'next' to move to next candidate, 'summary' for quick recap, 'quit' to exit")
        print("="*100 + "\n")
        
        return self._run_qa_loop(candidate_result)
    
    def interactive_session(self, candidate_result: ATSMatchResult, resume_text: str, job_desc: str):
        """Start an interactive Q&A session about a candidate (Recruiter perspective)"""
        self.start_conversation(candidate_result, resume_text, job_desc)
        
        print("\n" + "="*100)
        print(f"💬 INTERACTIVE SESSION - {candidate_result.candidate_name}")
        print("="*100)
        print(f"\nYou can now ask questions about this candidate!")
        print(f"Score: {candidate_result.overall_score}% | Recommendation: {candidate_result.hiring_recommendation}")
        print("\nExample questions:")
        print("  • What are the biggest concerns about this candidate?")
        print("  • How does their experience compare to the job requirements?")
        print("  • What specific questions should I ask about their Python skills?")
        print("  • Can they handle the team leadership responsibilities?")
        print("  • What's the risk of hiring this person?")
        print("  • How quickly could they ramp up on our tech stack?")
        print("  • Compare their skills to a senior developer role")
        print("\nType 'next' to move to next candidate, 'summary' for quick recap, 'quit' to exit")
        print("="*100 + "\n")
        
        return self._run_qa_loop(candidate_result)
    
    def _run_qa_loop(self, candidate_result: ATSMatchResult):
        """Common Q&A loop for both modes"""
        while True:
            try:
                question = input("❓ Your question: ").strip()
                
                if not question:
                    continue
                
                if question.lower() in ['quit', 'exit', 'q']:
                    print("\n👋 Ending interactive session...")
                    return 'quit'
                
                if question.lower() in ['next', 'skip', 'n']:
                    print("\n➡️  Moving to next candidate...")
                    return 'next'
                
                if question.lower() in ['summary', 'recap', 's']:
                    self.print_quick_summary(candidate_result)
                    continue
                
                if question.lower() in ['help', 'h', '?']:
                    # Determine mode from conversation history
                    mode = 'candidate' if any('resume improvement' in msg.get('content', '').lower() 
                                             for msg in self.conversation_history) else 'recruiter'
                    self.print_help(mode)
                    continue
                
                # Get AI response
                print("\n🤖 AI Response:")
                print("-" * 100)
                answer = self.ask_question(question)
                print(answer)
                print("-" * 100 + "\n")
                
            except KeyboardInterrupt:
                print("\n\n👋 Ending interactive session...")
                return 'quit'
            except EOFError:
                return 'quit'
    
    def print_quick_summary(self, result: ATSMatchResult):
        """Print a quick summary of the candidate"""
        print("\n" + "="*100)
        print(f"📊 QUICK SUMMARY - {result.candidate_name}")
        print("="*100)
        print(f"\n🎯 Score: {result.overall_score}% | {result.hiring_recommendation}")
        print(f"\n💼 Experience: {result.candidate_experience.total_years} years")
        print(f"🎓 Education: {', '.join(result.education.degrees[:2]) if result.education.degrees else 'Not specified'}")
        
        if result.matched_skills:
            print(f"\n✅ Top Skills: {', '.join(result.matched_skills[:8])}")
        
        if result.missing_critical_skills:
            print(f"❌ Missing: {', '.join(result.missing_critical_skills[:5])}")
        
        if result.strengths:
            print(f"\n💪 Key Strength: {result.strengths[0]}")
        
        if result.weaknesses:
            print(f"⚠️  Main Concern: {result.weaknesses[0]}")
        
        print("="*100 + "\n")
    
    def print_help(self, mode='recruiter'):
        """Print help information"""
        print("\n" + "="*100)
        if mode == 'candidate':
            print("📖 RESUME IMPROVEMENT HELP")
            print("="*100)
            print("\nYou can ask ANY question about improving your resume. Examples:")
            
            print("\n🎯 UNDERSTANDING YOUR SCORE:")
            print("  • Why did I get this score?")
            print("  • What are my biggest weaknesses?")
            print("  • Which areas hurt my score the most?")
            print("  • Am I qualified for this job?")
            
            print("\n✍️  REWRITING RESUME POINTS:")
            print("  • How can I rewrite my experience at [Company]?")
            print("  • Show me before/after for my bullet points")
            print("  • What's wrong with how I described my Python work?")
            print("  • How should I phrase my leadership experience?")
            print("  • Give me better action verbs for my achievements")
            
            print("\n🔧 TECHNICAL SKILLS:")
            print("  • Which technical skills should I add?")
            print("  • How can I better showcase my Python expertise?")
            print("  • What keywords am I missing?")
            print("  • Should I list more technologies?")
            
            print("\n📊 QUANTIFYING ACHIEVEMENTS:")
            print("  • How can I add metrics to my experience?")
            print("  • What numbers should I include?")
            print("  • How do I quantify my impact?")
            
            print("\n🎓 EDUCATION & CERTIFICATIONS:")
            print("  • Do I need additional certifications?")
            print("  • How should I present my education?")
            print("  • What courses would help my application?")
            
            print("\n🚀 OPTIMIZATION:")
            print("  • What should I remove from my resume?")
            print("  • How can I get to 90%+ match?")
            print("  • What's the fastest way to improve my score?")
            print("  • Which section needs the most work?")
            
            print("\n🎮 COMMANDS:")
            print("  • 'next' or 'n' - Move to next resume")
            print("  • 'summary' or 's' - Show quick summary")
            print("  • 'help' or 'h' - Show this help")
            print("  • 'quit' or 'q' - Exit interactive mode")
        else:
            print("📖 INTERACTIVE ATS HELP")
            print("="*100)
            print("\nYou can ask ANY question about the candidate. Examples:")
            print("\n🎯 ASSESSMENT QUESTIONS:")
            print("  • What are the biggest red flags?")
            print("  • Is this candidate worth interviewing?")
            print("  • What's the risk level of hiring them?")
            print("  • How confident are you in this recommendation?")
            
            print("\n💼 EXPERIENCE QUESTIONS:")
            print("  • Do they have enough experience for this role?")
            print("  • What's their career trajectory?")
            print("  • Have they worked on similar projects?")
            print("  • Why did they change jobs so frequently?")
            
            print("\n🔧 TECHNICAL QUESTIONS:")
            print("  • How strong are their Python skills?")
            print("  • Can they handle our tech stack?")
            print("  • What technical gaps should we address?")
            print("  • Do they have cloud experience?")
            
            print("\n👥 TEAM FIT QUESTIONS:")
            print("  • Will they fit our team culture?")
            print("  • Can they mentor junior developers?")
            print("  • Do they have leadership experience?")
            print("  • How are their communication skills?")
            
            print("\n📋 INTERVIEW PREP:")
            print("  • What should I ask in the interview?")
            print("  • What areas need deeper probing?")
            print("  • How can I verify their claims?")
            print("  • What's the best interview strategy?")
            
            print("\n⚖️  COMPARISON QUESTIONS:")
            print("  • How do they compare to other candidates?")
            print("  • Are they overqualified or underqualified?")
            print("  • What's their salary expectation likely to be?")
            
            print("\n🎮 COMMANDS:")
            print("  • 'next' or 'n' - Move to next candidate")
            print("  • 'summary' or 's' - Show quick summary")
            print("  • 'help' or 'h' - Show this help")
            print("  • 'quit' or 'q' - Exit interactive mode")
        print("="*100 + "\n")
    
    def compare_candidates(self):
        """Interactive comparison of all candidates"""
        if len(self.all_results) < 2:
            print("\n⚠️  Need at least 2 candidates to compare")
            return
        
        print("\n" + "="*100)
        print("⚖️  CANDIDATE COMPARISON MODE")
        print("="*100)
        
        # Show all candidates
        print("\nCandidates analyzed:")
        for i, result in enumerate(self.all_results, 1):
            print(f"{i}. {result.candidate_name} - {result.overall_score}% - {result.hiring_recommendation}")
        
        print("\nYou can now ask comparison questions!")
        print("Examples:")
        print("  • Who is the best candidate overall?")
        print("  • Compare candidate 1 and candidate 2")
        print("  • Who has the strongest technical skills?")
        print("  • Which candidate is the safest hire?")
        print("  • Rank all candidates by experience")
        print("  • Who would ramp up fastest?")
        print("\nType 'quit' to exit comparison mode")
        print("="*100 + "\n")
        
        # Build comparison context
        comparison_context = "You are comparing multiple candidates for the same position.\n\n"
        comparison_context += f"JOB DESCRIPTION:\n{self.current_job_desc[:2000]}\n\n"
        comparison_context += "CANDIDATES:\n\n"
        
        for i, result in enumerate(self.all_results, 1):
            comparison_context += f"CANDIDATE {i}: {result.candidate_name}\n"
            comparison_context += f"Score: {result.overall_score}%\n"
            comparison_context += f"Recommendation: {result.hiring_recommendation}\n"
            comparison_context += f"Experience: {result.candidate_experience.total_years} years\n"
            comparison_context += f"Skills: {', '.join(result.matched_skills[:10])}\n"
            comparison_context += f"Missing: {', '.join(result.missing_critical_skills[:5])}\n"
            comparison_context += f"Strengths: {'; '.join(result.strengths[:2])}\n"
            comparison_context += f"Concerns: {'; '.join(result.weaknesses[:2])}\n\n"
        
        # Initialize comparison conversation
        comparison_history = [
            {
                "role": "system",
                "content": f"{comparison_context}\nProvide detailed comparisons, rankings, and recommendations. Be specific and reference actual candidate details."
            }
        ]
        
        while True:
            try:
                question = input("❓ Comparison question: ").strip()
                
                if not question:
                    continue
                
                if question.lower() in ['quit', 'exit', 'q', 'done']:
                    print("\n👋 Exiting comparison mode...")
                    break
                
                # Add question to history
                comparison_history.append({
                    "role": "user",
                    "content": question
                })
                
                # Get AI response
                try:
                    response = self.client.chat.completions.create(
                        model=self.model,
                        messages=comparison_history,
                        temperature=0.5,
                        max_tokens=2000
                    )
                    
                    answer = response.choices[0].message.content.strip()
                    
                    # Add to history
                    comparison_history.append({
                        "role": "assistant",
                        "content": answer
                    })
                    
                    print("\n🤖 AI Response:")
                    print("-" * 100)
                    print(answer)
                    print("-" * 100 + "\n")
                    
                except Exception as e:
                    print(f"\n❌ Error: {str(e)}\n")
                
            except KeyboardInterrupt:
                print("\n\n👋 Exiting comparison mode...")
                break
            except EOFError:
                break
    
    def run_interactive(self, mode='recruiter'):
        """Run the ATS in interactive mode
        
        Args:
            mode: 'recruiter' for hiring perspective, 'candidate' for resume improvement
        """
        if mode == 'candidate':
            print("\n" + "="*100)
            print("📝 RESUME IMPROVEMENT MODE - Get AI Advice to Improve Your Resume")
            print("="*100)
            print("\nAnalyze your own resume and get specific suggestions to improve it!")
            print("Learn what to change, how to rewrite bullet points, and boost your score.")
        else:
            print("\n" + "="*100)
            print("🚀 INTERACTIVE ATS - Chat with AI about Candidates")
            print("="*100)
        
        if not self.client:
            print("\n❌ LLM not configured. Please set up your API key in ats_config.txt")
            return
        
        # Store mode for later use
        self.current_mode = mode
        
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
        self.current_job_desc = job_desc
        print(f"✓ Job description loaded ({len(job_desc)} characters)")
        
        # Find PDFs
        pdf_files = list(Path(resume_folder).glob('*.pdf'))
        if not pdf_files:
            print(f"\n❌ No PDF files found in: {resume_folder}")
            return
        
        print(f"\n📁 Found {len(pdf_files)} resume(s) to analyze")
        print("🤖 Analyzing all candidates first, then starting interactive sessions...\n")
        
        # Process all resumes first
        resume_data = []
        for i, pdf_file in enumerate(pdf_files, 1):
            print(f"⏳ [{i}/{len(pdf_files)}] Analyzing: {pdf_file.name}...")
            
            # Extract text
            resume_text = self.extract_text_from_pdf(str(pdf_file))
            if not resume_text:
                print(f"   ⚠️  Could not extract text from {pdf_file.name}")
                continue
            
            # AI Analysis
            candidate_info = self.extract_candidate_info(resume_text)
            skills = self.analyze_skills(resume_text, job_desc)
            experience = self.analyze_experience(resume_text, job_desc)
            education = self.analyze_education(resume_text)
            
            result = self.calculate_match_score(
                resume_text, job_desc, candidate_info,
                skills, experience, education
            )
            result.filename = pdf_file.name
            
            # Save for interactive session
            resume_data.append({
                'result': result,
                'resume_text': resume_text,
                'pdf_file': pdf_file
            })
            
            self.all_results.append(result)
            
            # Save report
            if self.config.get('SAVE_DETAILED_REPORTS', 'true').lower() == 'true':
                self.save_report(result, output_folder)
            
            print(f"   ✓ {candidate_info.get('name', 'Unknown')} - Score: {result.overall_score}%")
        
        if not resume_data:
            print("\n❌ No resumes could be processed")
            return
        
        # Sort by score
        resume_data.sort(key=lambda x: x['result'].overall_score, reverse=True)
        self.all_results.sort(key=lambda x: x.overall_score, reverse=True)
        
        # Show summary
        print("\n" + "="*100)
        print("📊 ANALYSIS COMPLETE - Starting Interactive Sessions")
        print("="*100)
        print(f"\n{'Rank':<6} {'Score':<8} {'Name':<35} {'Recommendation'}")
        print("-" * 100)
        for i, data in enumerate(resume_data, 1):
            result = data['result']
            print(f"{i:<6} {result.overall_score:<8.1f} {result.candidate_name:<35} {result.hiring_recommendation[:40]}")
        print("="*100)
        
        # Interactive sessions for each candidate
        for i, data in enumerate(resume_data, 1):
            result = data['result']
            resume_text = data['resume_text']
            
            # Print detailed report first
            self.print_detailed_report(result)
            
            # Start interactive session based on mode
            if mode == 'candidate':
                action = self.resume_improvement_mode(result, resume_text, job_desc)
            else:
                action = self.interactive_session(result, resume_text, job_desc)
            
            if action == 'quit':
                break
        
        # Offer comparison mode
        if len(self.all_results) > 1:
            print("\n" + "="*100)
            compare = input(f"\n🤔 Would you like to compare all {len(self.all_results)} candidates? (yes/no): ").strip().lower()
            if compare in ['yes', 'y']:
                self.compare_candidates()
        
        print("\n" + "="*100)
        print("✅ INTERACTIVE ATS SESSION COMPLETE!")
        print("="*100)
        print(f"\n📊 Summary:")
        print(f"   • Candidates analyzed: {len(self.all_results)}")
        print(f"   • Top candidate: {self.all_results[0].candidate_name} ({self.all_results[0].overall_score}%)")
        print(f"   • Reports saved to: {output_folder}")
        print("\n" + "="*100 + "\n")


def main():
    """Main entry point"""
    print("\n" + "="*100)
    print("💬 INTERACTIVE ATS - Choose Your Mode")
    print("="*100)
    print("\n1. 🎯 RECRUITER MODE - Evaluate candidates and get hiring insights")
    print("2. 📝 CANDIDATE MODE - Improve YOUR resume with AI feedback")
    print("="*100 + "\n")
    
    while True:
        choice = input("Select mode (1 for Recruiter, 2 for Candidate): ").strip()
        if choice == '1':
            mode = 'recruiter'
            print("\n✓ Recruiter Mode selected - Analyzing candidates for hiring decisions\n")
            break
        elif choice == '2':
            mode = 'candidate'
            print("\n✓ Candidate Mode selected - Get personalized resume improvement advice\n")
            break
        else:
            print("❌ Invalid choice. Please enter 1 or 2.")
    
    ats = InteractiveATS()
    ats.run_interactive(mode=mode)


if __name__ == "__main__":
    main()
