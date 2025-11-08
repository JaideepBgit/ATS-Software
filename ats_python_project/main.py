"""
Main entry point for the ATS Python Project
"""
import asyncio
import sys
from pathlib import Path
from typing import Optional
import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from loguru import logger

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

from core.ats_engine import ATSEngine
from models.ats_models import JobPosting, SearchFilters, JobStatus
from config.settings import settings

console = Console()


class ATSCLIApp:
    """Command Line Interface for the ATS system"""
    
    def __init__(self):
        self.ats_engine = ATSEngine()
        self.initialized = False
    
    async def initialize(self):
        """Initialize the ATS engine"""
        if not self.initialized:
            await self.ats_engine.initialize()
            self.initialized = True
            console.print("[green]✓[/green] ATS Engine initialized successfully")
    
    async def show_main_menu(self):
        """Display the main menu"""
        while True:
            console.clear()
            console.print(Panel.fit(
                f"[bold blue]{settings.app_name}[/bold blue]\n"
                f"Version {settings.app_version}",
                title="ATS Python Project"
            ))
            
            console.print("\n[bold]Main Menu:[/bold]")
            console.print("1. 📄 Candidate Management")
            console.print("2. 💼 Job Management")
            console.print("3. 📋 Application Management")
            console.print("4. 🔍 Matching & Search")
            console.print("5. 📊 Analytics & Reports")
            console.print("6. ⚙️  Settings & Configuration")
            console.print("7. ❌ Exit")
            
            choice = Prompt.ask("\nSelect an option", choices=["1", "2", "3", "4", "5", "6", "7"])
            
            try:
                if choice == "1":
                    await self.candidate_menu()
                elif choice == "2":
                    await self.job_menu()
                elif choice == "3":
                    await self.application_menu()
                elif choice == "4":
                    await self.matching_menu()
                elif choice == "5":
                    await self.analytics_menu()
                elif choice == "6":
                    await self.settings_menu()
                elif choice == "7":
                    if Confirm.ask("Are you sure you want to exit?"):
                        break
            except KeyboardInterrupt:
                console.print("\n[yellow]Operation cancelled[/yellow]")
                continue
            except Exception as e:
                console.print(f"[red]Error: {str(e)}[/red]")
                input("Press Enter to continue...")
    
    async def candidate_menu(self):
        """Candidate management menu"""
        while True:
            console.clear()
            console.print(Panel.fit("[bold blue]Candidate Management[/bold blue]"))
            
            console.print("\n[bold]Options:[/bold]")
            console.print("1. 📁 Add candidate from resume file")
            console.print("2. 📁 Bulk process resumes from folder")
            console.print("3. 👥 View all candidates")
            console.print("4. 🔍 Search candidates")
            console.print("5. 👤 View candidate details")
            console.print("6. ⬅️  Back to main menu")
            
            choice = Prompt.ask("\nSelect an option", choices=["1", "2", "3", "4", "5", "6"])
            
            if choice == "1":
                await self.add_candidate_from_resume()
            elif choice == "2":
                await self.bulk_process_resumes()
            elif choice == "3":
                await self.view_all_candidates()
            elif choice == "4":
                await self.search_candidates()
            elif choice == "5":
                await self.view_candidate_details()
            elif choice == "6":
                break
    
    async def add_candidate_from_resume(self):
        """Add a single candidate from resume file"""
        console.print("\n[bold]Add Candidate from Resume[/bold]")
        
        file_path = Prompt.ask("Enter the path to the resume file")
        
        if not Path(file_path).exists():
            console.print("[red]File not found![/red]")
            input("Press Enter to continue...")
            return
        
        console.print("Processing resume...")
        
        try:
            candidate = await self.ats_engine.add_candidate_from_resume(file_path)
            
            if candidate:
                console.print(f"[green]✓[/green] Successfully added candidate: {candidate.full_name}")
                console.print(f"   ID: {candidate.id}")
                console.print(f"   Skills: {', '.join(candidate.skills[:5])}")
                console.print(f"   Experience: {candidate.years_of_experience} years")
            else:
                console.print("[red]Failed to process resume[/red]")
        
        except Exception as e:
            console.print(f"[red]Error: {str(e)}[/red]")
        
        input("Press Enter to continue...")
    
    async def bulk_process_resumes(self):
        """Bulk process resumes from a directory"""
        console.print("\n[bold]Bulk Process Resumes[/bold]")
        
        directory = Prompt.ask("Enter the directory path containing resumes")
        
        if not Path(directory).exists():
            console.print("[red]Directory not found![/red]")
            input("Press Enter to continue...")
            return
        
        # Ask if they want to apply to a specific job
        apply_to_job = Confirm.ask("Do you want to automatically apply these candidates to a specific job?")
        job_id = None
        
        if apply_to_job:
            job_id = await self.select_job()
        
        console.print("Processing resumes...")
        
        try:
            results = await self.ats_engine.bulk_process_resumes(directory, job_id)
            
            console.print(f"\n[bold]Bulk Processing Results:[/bold]")
            console.print(f"   Processed: {results['processed']}")
            console.print(f"   Successful: {results['successful']}")
            console.print(f"   Failed: {results['failed']}")
            
            if results['applications']:
                console.print(f"   Applications created: {len(results['applications'])}")
        
        except Exception as e:
            console.print(f"[red]Error: {str(e)}[/red]")
        
        input("Press Enter to continue...")
    
    async def view_all_candidates(self):
        """View all candidates"""
        console.print("\n[bold]All Candidates[/bold]")
        
        try:
            candidates = await self.ats_engine.search_candidates(SearchFilters())
            
            if not candidates:
                console.print("No candidates found.")
                input("Press Enter to continue...")
                return
            
            table = Table(title="Candidates")
            table.add_column("ID", style="cyan")
            table.add_column("Name", style="green")
            table.add_column("Email", style="blue")
            table.add_column("Skills", style="yellow")
            table.add_column("Experience", style="magenta")
            
            for candidate in candidates[:20]:  # Show first 20
                skills_str = ", ".join(candidate.skills[:3]) + ("..." if len(candidate.skills) > 3 else "")
                exp_str = f"{candidate.years_of_experience} years" if candidate.years_of_experience else "N/A"
                
                table.add_row(
                    candidate.id[:8] + "...",
                    candidate.full_name,
                    candidate.contact_info.email or "N/A",
                    skills_str,
                    exp_str
                )
            
            console.print(table)
            
            if len(candidates) > 20:
                console.print(f"\n[yellow]Showing first 20 of {len(candidates)} candidates[/yellow]")
        
        except Exception as e:
            console.print(f"[red]Error: {str(e)}[/red]")
        
        input("Press Enter to continue...")
    
    async def job_menu(self):
        """Job management menu"""
        while True:
            console.clear()
            console.print(Panel.fit("[bold blue]Job Management[/bold blue]"))
            
            console.print("\n[bold]Options:[/bold]")
            console.print("1. ➕ Create new job posting")
            console.print("2. 💼 View all job postings")
            console.print("3. 🔍 Search job postings")
            console.print("4. 📝 View job details")
            console.print("5. ✏️  Edit job posting")
            console.print("6. ⬅️  Back to main menu")
            
            choice = Prompt.ask("\nSelect an option", choices=["1", "2", "3", "4", "5", "6"])
            
            if choice == "1":
                await self.create_job_posting()
            elif choice == "2":
                await self.view_all_jobs()
            elif choice == "3":
                await self.search_jobs()
            elif choice == "4":
                await self.view_job_details()
            elif choice == "5":
                await self.edit_job_posting()
            elif choice == "6":
                break
    
    async def create_job_posting(self):
        """Create a new job posting"""
        console.print("\n[bold]Create New Job Posting[/bold]")
        
        try:
            title = Prompt.ask("Job title")
            company = Prompt.ask("Company name")
            location = Prompt.ask("Location")
            job_type = Prompt.ask("Job type", choices=["full-time", "part-time", "contract", "internship"], default="full-time")
            description = Prompt.ask("Job description")
            
            # Parse skills from description or ask separately
            required_skills = Prompt.ask("Required skills (comma-separated)", default="").split(",")
            required_skills = [skill.strip() for skill in required_skills if skill.strip()]
            
            job_data = {
                "title": title,
                "company": company,
                "location": location,
                "job_type": job_type,
                "description": description,
                "required_skills": required_skills,
                "status": JobStatus.DRAFT
            }
            
            job = await self.ats_engine.create_job_posting(job_data)
            
            console.print(f"[green]✓[/green] Successfully created job posting: {job.title}")
            console.print(f"   ID: {job.id}")
            console.print(f"   Status: {job.status.value}")
        
        except Exception as e:
            console.print(f"[red]Error: {str(e)}[/red]")
        
        input("Press Enter to continue...")
    
    async def matching_menu(self):
        """Matching and search menu"""
        while True:
            console.clear()
            console.print(Panel.fit("[bold blue]Matching & Search[/bold blue]"))
            
            console.print("\n[bold]Options:[/bold]")
            console.print("1. 🎯 Find best candidates for a job")
            console.print("2. 💼 Find best jobs for a candidate")
            console.print("3. 📊 Calculate match score")
            console.print("4. 🔍 Advanced candidate search")
            console.print("5. ⬅️  Back to main menu")
            
            choice = Prompt.ask("\nSelect an option", choices=["1", "2", "3", "4", "5"])
            
            if choice == "1":
                await self.find_best_candidates()
            elif choice == "2":
                await self.find_best_jobs()
            elif choice == "3":
                await self.calculate_match_score()
            elif choice == "4":
                await self.advanced_candidate_search()
            elif choice == "5":
                break
    
    async def find_best_candidates(self):
        """Find best candidates for a job"""
        console.print("\n[bold]Find Best Candidates for Job[/bold]")
        
        job_id = await self.select_job()
        if not job_id:
            return
        
        console.print("Finding best matching candidates...")
        
        try:
            results = await self.ats_engine.find_best_candidates_for_job(job_id, limit=10)
            
            if not results:
                console.print("No candidates found.")
                input("Press Enter to continue...")
                return
            
            table = Table(title="Best Matching Candidates")
            table.add_column("Rank", style="cyan")
            table.add_column("Name", style="green")
            table.add_column("Overall Score", style="red")
            table.add_column("Skills Score", style="blue")
            table.add_column("Experience Score", style="yellow")
            table.add_column("Top Skills", style="magenta")
            
            for i, (candidate, match_score) in enumerate(results, 1):
                top_skills = ", ".join(match_score.matched_skills[:3])
                
                table.add_row(
                    str(i),
                    candidate.full_name,
                    f"{match_score.overall_score:.1f}%",
                    f"{match_score.skill_match_score:.1f}%",
                    f"{match_score.experience_match_score:.1f}%",
                    top_skills
                )
            
            console.print(table)
        
        except Exception as e:
            console.print(f"[red]Error: {str(e)}[/red]")
        
        input("Press Enter to continue...")
    
    async def analytics_menu(self):
        """Analytics and reports menu"""
        console.clear()
        console.print(Panel.fit("[bold blue]Analytics & Reports[/bold blue]"))
        
        try:
            stats = await self.ats_engine.get_ats_statistics()
            
            # Create statistics table
            table = Table(title="ATS Statistics")
            table.add_column("Metric", style="cyan")
            table.add_column("Value", style="green")
            
            table.add_row("Total Candidates", str(stats.total_candidates))
            table.add_row("Total Jobs", str(stats.total_jobs))
            table.add_row("Total Applications", str(stats.total_applications))
            table.add_row("Active Jobs", str(stats.active_jobs))
            table.add_row("Applications This Month", str(stats.applications_this_month))
            table.add_row("Average Match Score", f"{stats.avg_match_score:.1f}%")
            
            console.print(table)
            
            # Show top skills
            if stats.top_skills:
                console.print("\n[bold]Top Skills:[/bold]")
                for i, skill_data in enumerate(stats.top_skills[:10], 1):
                    console.print(f"{i:2d}. {skill_data['skill']} ({skill_data['count']} candidates)")
        
        except Exception as e:
            console.print(f"[red]Error: {str(e)}[/red]")
        
        input("Press Enter to continue...")
    
    async def settings_menu(self):
        """Settings and configuration menu"""
        console.clear()
        console.print(Panel.fit("[bold blue]Settings & Configuration[/bold blue]"))
        
        console.print(f"\n[bold]Current Configuration:[/bold]")
        console.print(f"App Name: {settings.app_name}")
        console.print(f"Version: {settings.app_version}")
        console.print(f"LM Studio URL: {settings.lm_studio_base_url}")
        console.print(f"Database: {settings.database_url}")
        console.print(f"Max File Size: {settings.max_file_size_mb}MB")
        console.print(f"Allowed File Types: {', '.join(settings.allowed_file_types)}")
        
        # Test LM Studio connection
        console.print("\n[bold]Testing LM Studio Connection...[/bold]")
        try:
            from services.lm_studio_service import LMStudioService
            async with LMStudioService() as lm_service:
                is_healthy = await lm_service.health_check()
                if is_healthy:
                    console.print("[green]✓[/green] LM Studio is accessible")
                else:
                    console.print("[red]✗[/red] LM Studio is not accessible")
        except Exception as e:
            console.print(f"[red]✗[/red] Error connecting to LM Studio: {str(e)}")
        
        input("Press Enter to continue...")
    
    async def select_job(self) -> Optional[str]:
        """Helper method to select a job from available jobs"""
        try:
            jobs = await self.ats_engine.search_job_postings(SearchFilters())
            
            if not jobs:
                console.print("No jobs available.")
                return None
            
            console.print("\n[bold]Available Jobs:[/bold]")
            for i, job in enumerate(jobs[:10], 1):
                console.print(f"{i}. {job.title} at {job.company} ({job.status.value})")
            
            choice = Prompt.ask(f"Select a job (1-{min(len(jobs), 10)})", default="1")
            
            try:
                index = int(choice) - 1
                if 0 <= index < len(jobs):
                    return jobs[index].id
            except ValueError:
                pass
            
            console.print("[red]Invalid selection[/red]")
            return None
        
        except Exception as e:
            console.print(f"[red]Error: {str(e)}[/red]")
            return None
    
    # Placeholder methods for other menu options
    async def search_candidates(self):
        console.print("Search candidates functionality - Coming soon!")
        input("Press Enter to continue...")
    
    async def view_candidate_details(self):
        console.print("View candidate details functionality - Coming soon!")
        input("Press Enter to continue...")
    
    async def view_all_jobs(self):
        console.print("View all jobs functionality - Coming soon!")
        input("Press Enter to continue...")
    
    async def search_jobs(self):
        console.print("Search jobs functionality - Coming soon!")
        input("Press Enter to continue...")
    
    async def view_job_details(self):
        console.print("View job details functionality - Coming soon!")
        input("Press Enter to continue...")
    
    async def edit_job_posting(self):
        console.print("Edit job posting functionality - Coming soon!")
        input("Press Enter to continue...")
    
    async def application_menu(self):
        console.print("Application management functionality - Coming soon!")
        input("Press Enter to continue...")
    
    async def find_best_jobs(self):
        console.print("Find best jobs functionality - Coming soon!")
        input("Press Enter to continue...")
    
    async def calculate_match_score(self):
        console.print("Calculate match score functionality - Coming soon!")
        input("Press Enter to continue...")
    
    async def advanced_candidate_search(self):
        console.print("Advanced candidate search functionality - Coming soon!")
        input("Press Enter to continue...")


@click.command()
@click.option('--debug', is_flag=True, help='Enable debug mode')
def main(debug):
    """ATS Python Project - Main Entry Point"""
    
    # Configure logging
    logger.remove()
    log_level = "DEBUG" if debug else settings.log_level
    logger.add(sys.stderr, level=log_level, format="<green>{time}</green> | <level>{level}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>")
    
    # Create and run the CLI app
    app = ATSCLIApp()
    
    async def run_app():
        try:
            await app.initialize()
            await app.show_main_menu()
        except KeyboardInterrupt:
            console.print("\n[yellow]Application interrupted by user[/yellow]")
        except Exception as e:
            console.print(f"[red]Unexpected error: {str(e)}[/red]")
            logger.exception("Unexpected error in main application")
        finally:
            await app.ats_engine.cleanup()
            console.print("[blue]Thank you for using ATS Python Project![/blue]")
    
    # Run the async application
    asyncio.run(run_app())


if __name__ == "__main__":
    main()
