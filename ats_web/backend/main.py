"""
FastAPI Backend for ATS Web Application
"""
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional
import os
from ats_service import ATSService, ATSResult
from job_tracker import JobTracker
from feedback_store import feedback_store
from rag_service import rag_service
from tts_service import get_tts_service
from job_storage import JobStorage
from resume_storage import ResumeStorage
from analysis_storage import AnalysisStorage
from dataclasses import asdict
from fastapi.responses import FileResponse, StreamingResponse
from pathlib import Path

app = FastAPI(title="ATS Web API")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize ATS Service and Job Tracker
ats_service = ATSService()
job_tracker = JobTracker()

# Initialize storage systems
job_storage = JobStorage()
resume_storage = ResumeStorage()
analysis_storage = AnalysisStorage()

# In-memory storage (for backward compatibility)
analysis_results: Dict[str, Dict] = {}
resume_texts: Dict[str, str] = {}
job_description: str = ""
company_name: str = ""
role_name: str = ""
current_job_id: str = ""  # Track current job ID


def load_recent_analyses():
    """Load recent analyses into memory for backward compatibility"""
    global analysis_results, resume_texts
    
    try:
        # Load recent analyses
        analyses = analysis_storage.list_analyses(limit=100)
        
        for analysis_summary in analyses:
            # Get full analysis
            full_analysis = analysis_storage.get_analysis(analysis_summary['analysis_id'])
            if full_analysis:
                # Create candidate_id in old format
                candidate_id = f"{full_analysis['candidate_name']}_{full_analysis['created_at']}"
                
                # Store in memory
                analysis_results[candidate_id] = full_analysis['analysis_result']
                
                # Load resume text
                resume_text = resume_storage.get_resume_text(full_analysis['resume_id'])
                if resume_text:
                    resume_texts[candidate_id] = resume_text
        
        print(f"[STARTUP] Loaded {len(analysis_results)} analyses into memory")
    except Exception as e:
        print(f"[STARTUP ERROR] Could not load analyses: {e}")


# Load analyses on startup
load_recent_analyses()


class JobDescriptionRequest(BaseModel):
    job_description: str
    company_name: Optional[str] = ""
    role_name: Optional[str] = ""


class QuestionRequest(BaseModel):
    candidate_id: str
    question: str


class JobApplicationRequest(BaseModel):
    company: str
    job_title: str
    portal: Optional[str] = "LinkedIn"
    employment_type: Optional[str] = "Full Time"


class FeedbackRequest(BaseModel):
    interaction_id: str
    query: str
    context: List[str] = []
    response: str
    rating: int
    correct_points: List[str] = []
    incorrect_points: List[str] = []
    missing_points: List[str] = []
    ideal_response: str
    analysis_id: Optional[str] = None
    job_id: Optional[str] = None


@app.get("/")
async def root():
    return {"message": "ATS Web API", "status": "running"}


@app.post("/api/job-description")
async def set_job_description(request: JobDescriptionRequest):
    """Set the job description and save to persistent storage"""
    global job_description, company_name, role_name, current_job_id
    job_description = request.job_description
    company_name = request.company_name or ""
    role_name = request.role_name or ""
    
    # Save to persistent storage
    job_record = job_storage.add_job(
        job_description=job_description,
        company_name=company_name,
        role_name=role_name
    )
    current_job_id = job_record['job_id']
    
    print(f"\n[DEBUG] ===== JOB DESCRIPTION SAVED =====")
    print(f"[DEBUG] Job ID: {current_job_id}")
    print(f"[DEBUG] Company: '{company_name}'")
    print(f"[DEBUG] Role: '{role_name}'")
    print(f"[DEBUG] Job Desc Length: {len(job_description)}")
    print(f"[DEBUG] Job Desc (first 200 chars): {job_description[:200]}")
    print(f"[DEBUG] ====================================\n")
    
    return {
        "message": "Job description saved", 
        "job_id": current_job_id,
        "length": len(job_description),
        "company_name": company_name,
        "role_name": role_name
    }


@app.get("/api/job-description")
async def get_job_description():
    """Get current job description"""
    global job_description, company_name, role_name
    
    return {
        "job_description": job_description,
        "company_name": company_name,
        "role_name": role_name
    }


@app.post("/api/upload-resume-only")
async def upload_resume_only(file: UploadFile = File(...)):
    """Upload a resume without analyzing (just store it)"""
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")
    
    try:
        # Read PDF
        pdf_bytes = await file.read()
        resume_text = ats_service.extract_text_from_pdf(pdf_bytes)
        
        if not resume_text:
            raise HTTPException(status_code=400, detail="Could not extract text from PDF")
        
        # Extract candidate name quickly
        lines = resume_text.split('\n')
        candidate_name = lines[0].strip() if lines else "Unknown"
        
        # Save resume to persistent storage
        resume_record = resume_storage.save_resume(
            pdf_bytes=pdf_bytes,
            resume_text=resume_text,
            filename=file.filename,
            candidate_name=candidate_name
        )
        
        print(f"[DEBUG] Resume uploaded: {resume_record['resume_id']} - {candidate_name}")
        
        return {
            "message": "Resume uploaded successfully",
            "resume_id": resume_record['resume_id'],
            "candidate_name": candidate_name,
            "filename": file.filename
        }
    
    except Exception as e:
        print(f"[ERROR] Error uploading resume: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error uploading resume: {str(e)}")


@app.post("/api/analyze-resume/{resume_id}")
async def analyze_resume(resume_id: str):
    """Analyze a previously uploaded resume against current job"""
    global job_description, company_name, role_name, current_job_id
    
    if not job_description:
        raise HTTPException(status_code=400, detail="Please set job description first")
    
    if not current_job_id:
        raise HTTPException(status_code=400, detail="No job ID found. Please set job description again.")
    
    try:
        # Get resume from storage
        resume_text = resume_storage.get_resume_text(resume_id)
        if not resume_text:
            raise HTTPException(status_code=404, detail="Resume not found")
        
        resume_record = resume_storage.get_resume(resume_id)
        
        print(f"\n[DEBUG] ===== ANALYZING RESUME =====")
        print(f"[DEBUG] Resume ID: {resume_id}")
        print(f"[DEBUG] Job ID: {current_job_id}")
        print(f"[DEBUG] Company: '{company_name}'")
        print(f"[DEBUG] Role: '{role_name}'")
        
        # Analyze
        result = ats_service.analyze_resume(
            resume_text, 
            job_description, 
            resume_record['original_filename'], 
            company_name, 
            role_name
        )
        
        # Store analysis results
        result_dict = asdict(result)
        analysis_record = analysis_storage.save_analysis(
            job_id=current_job_id,
            resume_id=resume_id,
            analysis_result=result_dict,
            candidate_name=result.candidate_name
        )
        analysis_id = analysis_record['analysis_id']
        
        # Update job analysis count
        job_storage.increment_analysis_count(current_job_id)
        
        # Store in memory for backward compatibility
        candidate_id = f"{result.candidate_name}_{result.timestamp}"
        analysis_results[candidate_id] = result_dict
        resume_texts[candidate_id] = resume_text
        
        print(f"[DEBUG] ===== ANALYSIS COMPLETE =====")
        print(f"[DEBUG] Analysis ID: {analysis_id}")
        print(f"[DEBUG] Overall Score: {result_dict.get('overall_score')}%")
        print(f"[DEBUG] ==============================\n")
        
        return {
            "candidate_id": candidate_id,
            "analysis_id": analysis_id,
            "resume_id": resume_id,
            "job_id": current_job_id,
            "result": result_dict
        }
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"[ERROR] Error analyzing resume: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error analyzing resume: {str(e)}")


@app.post("/api/upload-resume")
async def upload_resume(file: UploadFile = File(...)):
    """Upload and analyze a resume with persistent storage (legacy endpoint)"""
    global job_description, company_name, role_name, current_job_id
    
    if not job_description:
        raise HTTPException(status_code=400, detail="Please set job description first")
    
    if not current_job_id:
        raise HTTPException(status_code=400, detail="No job ID found. Please set job description again.")
    
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")
    
    try:
        # Read PDF
        pdf_bytes = await file.read()
        resume_text = ats_service.extract_text_from_pdf(pdf_bytes)
        
        if not resume_text:
            raise HTTPException(status_code=400, detail="Could not extract text from PDF")
        
        # Analyze with current job description and company/role info
        print(f"\n[DEBUG] ===== ANALYZING RESUME =====")
        print(f"[DEBUG] File: {file.filename}")
        print(f"[DEBUG] Job ID: {current_job_id}")
        print(f"[DEBUG] Company: '{company_name}'")
        print(f"[DEBUG] Role: '{role_name}'")
        print(f"[DEBUG] Job Desc (first 200 chars): {job_description[:200]}")
        
        result = ats_service.analyze_resume(resume_text, job_description, file.filename, company_name, role_name)
        
        # Save resume to persistent storage
        resume_record = resume_storage.save_resume(
            pdf_bytes=pdf_bytes,
            resume_text=resume_text,
            filename=file.filename,
            candidate_name=result.candidate_name
        )
        resume_id = resume_record['resume_id']
        
        # Store analysis results
        result_dict = asdict(result)
        analysis_record = analysis_storage.save_analysis(
            job_id=current_job_id,
            resume_id=resume_id,
            analysis_result=result_dict,
            candidate_name=result.candidate_name
        )
        analysis_id = analysis_record['analysis_id']
        
        # Update job analysis count
        job_storage.increment_analysis_count(current_job_id)
        
        # Store in memory for backward compatibility
        candidate_id = f"{result.candidate_name}_{result.timestamp}"
        analysis_results[candidate_id] = result_dict
        resume_texts[candidate_id] = resume_text
        
        print(f"[DEBUG] ===== RESULT CREATED =====")
        print(f"[DEBUG] Analysis ID: {analysis_id}")
        print(f"[DEBUG] Resume ID: {resume_id}")
        print(f"[DEBUG] Job ID: {current_job_id}")
        print(f"[DEBUG] Candidate ID: {candidate_id}")
        print(f"[DEBUG] Company in result: '{result_dict.get('company_name')}'")
        print(f"[DEBUG] Role in result: '{result_dict.get('role_name')}'")
        print(f"[DEBUG] Overall Score: {result_dict.get('overall_score')}%")
        print(f"[DEBUG] Recommendation: {result_dict.get('hiring_recommendation')}")
        print(f"[DEBUG] ==============================\n")
        
        return {
            "candidate_id": candidate_id,
            "analysis_id": analysis_id,
            "resume_id": resume_id,
            "job_id": current_job_id,
            "result": result_dict
        }
    
    except Exception as e:
        print(f"[ERROR] Error processing resume: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing resume: {str(e)}")


@app.get("/api/results")
async def get_all_results():
    """Get all analysis results sorted by timestamp (most recent first)"""
    # Reload from persistent storage to get latest
    load_recent_analyses()
    
    results = list(analysis_results.values())
    # Sort by timestamp (most recent first), then by score
    results.sort(key=lambda x: (x.get('timestamp', ''), x.get('overall_score', 0)), reverse=True)
    return {"results": results}


@app.get("/api/result/{candidate_id}")
async def get_result(candidate_id: str):
    """Get specific candidate result"""
    if candidate_id not in analysis_results:
        raise HTTPException(status_code=404, detail="Candidate not found")
    
    return {"result": analysis_results[candidate_id]}


@app.post("/api/ask")
async def ask_question(request: QuestionRequest):
    """Ask a question about a candidate with RAG enhancement"""
    global job_description
    
    if request.candidate_id not in analysis_results:
        raise HTTPException(status_code=404, detail="Candidate not found")
    
    result = analysis_results[request.candidate_id]
    resume_text = resume_texts.get(request.candidate_id, "")
    
    context = {
        "candidate_name": result['candidate_name'],
        "overall_score": result['overall_score'],
        "hiring_recommendation": result['hiring_recommendation'],
        "resume_text": resume_text,
        "job_desc": job_description
    }
    
    # Use RAG-enhanced response
    answer = rag_service.ask_with_rag(request.question, context, ats_service)
    
    return {"answer": answer}


@app.get("/api/debug/storage")
async def debug_storage():
    """Debug endpoint to see what's stored"""
    global job_description, company_name, role_name
    
    return {
        "job_description_length": len(job_description),
        "company_name": company_name,
        "role_name": role_name,
        "total_results": len(analysis_results),
        "sample_result": list(analysis_results.values())[0] if analysis_results else None
    }


@app.delete("/api/results")
async def clear_results():
    """Clear all results"""
    global analysis_results, resume_texts
    analysis_results = {}
    resume_texts = {}
    return {"message": "All results cleared"}


# Job Tracking Endpoints

@app.post("/api/job-application")
async def log_job_application(request: JobApplicationRequest):
    """Log a job application"""
    try:
        result = job_tracker.add_job_application(
            company=request.company,
            job_title=request.job_title,
            portal=request.portal,
            employment_type=request.employment_type
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error logging application: {str(e)}")


@app.get("/api/job-applications")
async def get_job_applications():
    """Get all job applications"""
    try:
        applications = job_tracker.get_all_applications()
        return {"applications": applications, "total": len(applications)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting applications: {str(e)}")


@app.get("/api/job-applications/recent")
async def get_recent_applications(limit: int = 10):
    """Get recent job applications"""
    try:
        applications = job_tracker.get_recent_applications(limit=limit)
        return {"applications": applications}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting recent applications: {str(e)}")


@app.get("/api/job-applications/statistics")
async def get_application_statistics():
    """Get job application statistics"""
    try:
        stats = job_tracker.get_statistics()
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting statistics: {str(e)}")


@app.get("/api/job-applications/check")
async def check_if_applied(company: str, job_title: str):
    """Check if already applied to a job"""
    try:
        already_applied = job_tracker.check_if_applied(company, job_title)
        return {"already_applied": already_applied}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error checking application: {str(e)}")


# Feedback Collection Endpoints

@app.post("/api/feedback/submit")
async def submit_feedback(request: FeedbackRequest):
    """Submit feedback for model training with analysis and job linking"""
    try:
        feedback_data = feedback_store.add_feedback(
            interaction_id=request.interaction_id,
            query=request.query,
            context=request.context,
            response=request.response,
            rating=request.rating,
            correct_points=request.correct_points,
            incorrect_points=request.incorrect_points,
            missing_points=request.missing_points,
            ideal_response=request.ideal_response,
            analysis_id=request.analysis_id,
            job_id=request.job_id
        )
        
        # Increment feedback count for analysis
        if request.analysis_id:
            analysis_storage.increment_feedback_count(request.analysis_id)
        
        return {
            "status": "success",
            "message": "Feedback saved successfully",
            "feedback_id": feedback_data["id"],
            "analysis_id": request.analysis_id,
            "job_id": request.job_id
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving feedback: {str(e)}")


@app.get("/api/feedback/statistics")
async def get_feedback_statistics():
    """Get feedback statistics"""
    try:
        stats = feedback_store.get_statistics()
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting statistics: {str(e)}")


@app.get("/api/feedback/search")
async def search_feedback(query: str, n_results: int = 5, min_rating: Optional[int] = None):
    """Search for similar feedback using ChromaDB"""
    try:
        results = feedback_store.search_similar_chromadb(query, n_results, min_rating)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching feedback: {str(e)}")


@app.get("/api/feedback/high-quality")
async def get_high_quality_feedback(min_rating: int = 4, limit: int = 100):
    """Get high-quality feedback samples for training"""
    try:
        samples = feedback_store.get_high_quality_samples(min_rating, limit)
        return {"samples": samples, "count": len(samples)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting samples: {str(e)}")


@app.get("/api/feedback/export-csv")
async def export_feedback_csv():
    """Export feedback to CSV"""
    import csv
    import io
    from fastapi.responses import StreamingResponse
    
    try:
        jsonl_file = "feedback_db/interactions.jsonl"
        
        # Create CSV in memory
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow([
            'ID', 'Timestamp', 'Rating', 'Query', 'Response',
            'Correct Points', 'Incorrect Points', 'Missing Points', 'Ideal Response'
        ])
        
        # Read JSONL and write to CSV
        import json
        from pathlib import Path
        
        jsonl_path = Path(jsonl_file)
        if jsonl_path.exists():
            with open(jsonl_path, 'r', encoding='utf-8') as f:
                for line in f:
                    data = json.loads(line)
                    writer.writerow([
                        data['id'],
                        data['timestamp'],
                        data['feedback']['rating'],
                        data['query'],
                        data['response'],
                        ', '.join(data['feedback']['correct_points']),
                        ', '.join(data['feedback']['incorrect_points']),
                        ', '.join(data['feedback'].get('missing_points', [])),
                        data['feedback']['ideal_response']
                    ])
        
        # Return as downloadable file
        output.seek(0)
        return StreamingResponse(
            iter([output.getvalue()]),
            media_type="text/csv",
            headers={"Content-Disposition": "attachment; filename=feedback_export.csv"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error exporting CSV: {str(e)}")


# TTS Endpoints

@app.post("/api/tts/generate")
async def generate_tts(text: str):
    """Generate TTS audio from text"""
    try:
        tts_service = get_tts_service()
        audio_path = tts_service.text_to_speech(text)
        audio_info = tts_service.get_audio_info(audio_path)
        
        return {
            "status": "success",
            "audio_path": audio_path,
            "duration": audio_info.get('duration', 0),
            "url": f"/api/tts/audio/{Path(audio_path).name}"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"TTS generation failed: {str(e)}")


@app.get("/api/tts/audio/{filename}")
async def get_tts_audio(filename: str):
    """Serve generated TTS audio file"""
    try:
        tts_service = get_tts_service()
        audio_path = tts_service.output_dir / filename
        
        if not audio_path.exists():
            raise HTTPException(status_code=404, detail="Audio file not found")
        
        return FileResponse(
            audio_path,
            media_type="audio/wav",
            filename=filename
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error serving audio: {str(e)}")


@app.post("/api/tts/summary/{candidate_id}")
async def generate_candidate_summary_tts(candidate_id: str):
    """Generate TTS for candidate summary"""
    print(f"[TTS] Generating summary for candidate: {candidate_id}")
    
    if candidate_id not in analysis_results:
        print(f"[TTS ERROR] Candidate not found: {candidate_id}")
        print(f"[TTS ERROR] Available candidates: {list(analysis_results.keys())}")
        raise HTTPException(status_code=404, detail="Candidate not found")
    
    result = analysis_results[candidate_id]
    
    # Create summary text
    summary_text = f"""
    Candidate Analysis Summary for {result['candidate_name']}.
    
    Overall Score: {result['overall_score']} percent.
    
    Skills Match: {result['skill_match_score']:.1f} percent.
    Experience Match: {result['experience_match_score']:.1f} percent.
    Education Match: {result['education_match_score']:.1f} percent.
    
    Hiring Recommendation: {result['hiring_recommendation']}.
    
    Executive Summary: {result['executive_summary']}
    """
    
    try:
        print(f"[TTS] Initializing TTS service...")
        tts_service = get_tts_service()
        print(f"[TTS] Generating audio...")
        
        # Use single filename that gets overwritten
        audio_path = tts_service.text_to_speech(
            summary_text,
            output_filename="candidate_summary.wav"
        )
        print(f"[TTS] Audio generated: {audio_path}")
        audio_info = tts_service.get_audio_info(audio_path)
        
        return {
            "status": "success",
            "candidate_id": candidate_id,
            "audio_path": audio_path,
            "duration": audio_info.get('duration', 0),
            "url": f"/api/tts/audio/{Path(audio_path).name}"
        }
    except Exception as e:
        print(f"[TTS ERROR] Failed to generate TTS: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"TTS generation failed: {str(e)}")


@app.post("/api/tts/speak")
async def speak_text(request: dict):
    """Generate TTS for any text (questions, responses, etc.)"""
    text = request.get('text', '')
    
    if not text or not text.strip():
        raise HTTPException(status_code=400, detail="Text is required")
    
    print(f"[TTS] Generating speech for text: {text[:50]}...")
    
    try:
        tts_service = get_tts_service()
        
        # Use single filename that gets overwritten
        audio_path = tts_service.text_to_speech(
            text,
            output_filename="speech.wav"
        )
        
        audio_info = tts_service.get_audio_info(audio_path)
        
        return {
            "status": "success",
            "audio_path": audio_path,
            "duration": audio_info.get('duration', 0),
            "url": f"/api/tts/audio/{Path(audio_path).name}"
        }
    except Exception as e:
        print(f"[TTS ERROR] Failed to generate TTS: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"TTS generation failed: {str(e)}")


@app.get("/api/tts/status")
async def get_tts_status():
    """Check TTS service status"""
    try:
        tts_service = get_tts_service()
        return {
            "status": "available",
            "model": tts_service.model_path,
            "executable": tts_service.piper_executable,
            "output_dir": str(tts_service.output_dir)
        }
    except Exception as e:
        print(f"[TTS STATUS ERROR] {str(e)}")
        import traceback
        traceback.print_exc()
        return {
            "status": "unavailable",
            "error": str(e)
        }


# New Storage Management Endpoints

@app.get("/api/jobs")
async def list_jobs(limit: int = 50):
    """List all saved job descriptions"""
    try:
        jobs = job_storage.list_jobs(limit=limit)
        return {"jobs": jobs, "total": len(jobs)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing jobs: {str(e)}")


@app.get("/api/jobs/{job_id}")
async def get_job(job_id: str):
    """Get a specific job description"""
    try:
        job = job_storage.get_job(job_id)
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
        return {"job": job}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting job: {str(e)}")


@app.post("/api/jobs/{job_id}/select")
async def select_job(job_id: str):
    """Select a job as the current active job"""
    global job_description, company_name, role_name, current_job_id
    
    try:
        job = job_storage.get_job(job_id)
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
        
        # Set as current job
        current_job_id = job_id
        job_description = job['job_description']
        company_name = job['company_name']
        role_name = job['role_name']
        
        return {
            "message": "Job selected",
            "job_id": job_id,
            "company_name": company_name,
            "role_name": role_name
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error selecting job: {str(e)}")


@app.get("/api/jobs/search")
async def search_jobs(query: str):
    """Search jobs by company or role name"""
    try:
        jobs = job_storage.search_jobs(query)
        return {"jobs": jobs, "total": len(jobs)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching jobs: {str(e)}")


@app.get("/api/resumes")
async def list_resumes(limit: int = 50):
    """List all uploaded resumes"""
    try:
        resumes = resume_storage.list_resumes(limit=limit)
        return {"resumes": resumes, "total": len(resumes)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing resumes: {str(e)}")


@app.get("/api/resumes/{resume_id}")
async def get_resume(resume_id: str):
    """Get resume metadata"""
    try:
        resume = resume_storage.get_resume(resume_id)
        if not resume:
            raise HTTPException(status_code=404, detail="Resume not found")
        return {"resume": resume}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting resume: {str(e)}")


@app.get("/api/resumes/{resume_id}/text")
async def get_resume_text(resume_id: str):
    """Get resume text content"""
    try:
        text = resume_storage.get_resume_text(resume_id)
        if not text:
            raise HTTPException(status_code=404, detail="Resume not found")
        return {"resume_id": resume_id, "text": text}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting resume text: {str(e)}")


@app.get("/api/analyses")
async def list_analyses(job_id: Optional[str] = None, limit: int = 50):
    """List all analyses (optionally filtered by job_id)"""
    try:
        analyses = analysis_storage.list_analyses(job_id=job_id, limit=limit)
        return {"analyses": analyses, "total": len(analyses)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing analyses: {str(e)}")


@app.get("/api/analyses/{analysis_id}")
async def get_analysis(analysis_id: str):
    """Get a specific analysis"""
    try:
        analysis = analysis_storage.get_analysis(analysis_id)
        if not analysis:
            raise HTTPException(status_code=404, detail="Analysis not found")
        return {"analysis": analysis}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting analysis: {str(e)}")


@app.get("/api/storage/stats")
async def get_storage_stats():
    """Get storage statistics"""
    try:
        jobs = job_storage.list_jobs(limit=10000)
        resumes = resume_storage.list_resumes(limit=10000)
        analyses = analysis_storage.list_analyses(limit=10000)
        feedback_stats = feedback_store.get_statistics()
        
        return {
            "jobs": {
                "total": len(jobs),
                "recent": jobs[:5] if jobs else []
            },
            "resumes": {
                "total": len(resumes),
                "recent": resumes[:5] if resumes else []
            },
            "analyses": {
                "total": len(analyses),
                "recent": analyses[:5] if analyses else []
            },
            "feedback": feedback_stats,
            "current_job_id": current_job_id
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting stats: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    from pathlib import Path
    uvicorn.run(app, host="0.0.0.0", port=8000)
