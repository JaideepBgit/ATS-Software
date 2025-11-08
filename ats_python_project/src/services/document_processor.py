"""
Document processing service for handling resumes and job descriptions
"""
import os
import re
from typing import Dict, List, Optional, Tuple
from pathlib import Path
import PyPDF2
from docx import Document
import pandas as pd
from loguru import logger
from config.settings import settings


class DocumentProcessor:
    """Service for processing various document formats"""
    
    def __init__(self):
        self.allowed_extensions = settings.allowed_file_types
        self.max_file_size = settings.max_file_size_mb * 1024 * 1024  # Convert to bytes
    
    def validate_file(self, file_path: str) -> Tuple[bool, str]:
        """Validate file size and type"""
        try:
            path = Path(file_path)
            
            # Check if file exists
            if not path.exists():
                return False, "File does not exist"
            
            # Check file size
            file_size = path.stat().st_size
            if file_size > self.max_file_size:
                return False, f"File size exceeds {settings.max_file_size_mb}MB limit"
            
            # Check file extension
            extension = path.suffix.lower().lstrip('.')
            if extension not in self.allowed_extensions:
                return False, f"File type '{extension}' not allowed. Allowed types: {', '.join(self.allowed_extensions)}"
            
            return True, "File is valid"
            
        except Exception as e:
            logger.error(f"Error validating file {file_path}: {str(e)}")
            return False, f"Error validating file: {str(e)}"
    
    def extract_text_from_pdf(self, file_path: str) -> str:
        """Extract text from PDF file"""
        try:
            text = ""
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
            return text.strip()
        except Exception as e:
            logger.error(f"Error extracting text from PDF {file_path}: {str(e)}")
            return ""
    
    def extract_text_from_docx(self, file_path: str) -> str:
        """Extract text from DOCX file"""
        try:
            doc = Document(file_path)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text.strip()
        except Exception as e:
            logger.error(f"Error extracting text from DOCX {file_path}: {str(e)}")
            return ""
    
    def extract_text_from_txt(self, file_path: str) -> str:
        """Extract text from TXT file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read().strip()
        except UnicodeDecodeError:
            # Try with different encoding
            try:
                with open(file_path, 'r', encoding='latin-1') as file:
                    return file.read().strip()
            except Exception as e:
                logger.error(f"Error extracting text from TXT {file_path}: {str(e)}")
                return ""
        except Exception as e:
            logger.error(f"Error extracting text from TXT {file_path}: {str(e)}")
            return ""
    
    def extract_text(self, file_path: str) -> str:
        """Extract text from supported file formats"""
        # Validate file first
        is_valid, message = self.validate_file(file_path)
        if not is_valid:
            logger.error(f"File validation failed: {message}")
            return ""
        
        # Determine file type and extract text
        extension = Path(file_path).suffix.lower().lstrip('.')
        
        if extension == 'pdf':
            return self.extract_text_from_pdf(file_path)
        elif extension == 'docx':
            return self.extract_text_from_docx(file_path)
        elif extension == 'txt':
            return self.extract_text_from_txt(file_path)
        else:
            logger.error(f"Unsupported file type: {extension}")
            return ""
    
    def extract_contact_info(self, text: str) -> Dict[str, Optional[str]]:
        """Extract contact information from text"""
        contact_info = {
            "email": None,
            "phone": None,
            "linkedin": None,
            "github": None
        }
        
        # Email pattern
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        email_match = re.search(email_pattern, text)
        if email_match:
            contact_info["email"] = email_match.group()
        
        # Phone pattern (various formats)
        phone_patterns = [
            r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',  # 123-456-7890 or 123.456.7890 or 1234567890
            r'\(\d{3}\)\s*\d{3}[-.]?\d{4}',   # (123) 456-7890
            r'\+\d{1,3}[-.\s]?\d{3}[-.\s]?\d{3}[-.\s]?\d{4}'  # International format
        ]
        
        for pattern in phone_patterns:
            phone_match = re.search(pattern, text)
            if phone_match:
                contact_info["phone"] = phone_match.group()
                break
        
        # LinkedIn pattern
        linkedin_pattern = r'linkedin\.com/in/[\w-]+'
        linkedin_match = re.search(linkedin_pattern, text, re.IGNORECASE)
        if linkedin_match:
            contact_info["linkedin"] = linkedin_match.group()
        
        # GitHub pattern
        github_pattern = r'github\.com/[\w-]+'
        github_match = re.search(github_pattern, text, re.IGNORECASE)
        if github_match:
            contact_info["github"] = github_match.group()
        
        return contact_info
    
    def extract_education(self, text: str) -> List[Dict[str, str]]:
        """Extract education information from text"""
        education = []
        
        # Common degree patterns
        degree_patterns = [
            r'(Bachelor|Master|PhD|Ph\.D|MBA|B\.S|B\.A|M\.S|M\.A|B\.Sc|M\.Sc)\.?\s+(?:of\s+)?(?:Science\s+)?(?:Arts\s+)?(?:in\s+)?([A-Za-z\s]+)',
            r'(Associate|Diploma|Certificate)\s+(?:in\s+)?([A-Za-z\s]+)'
        ]
        
        for pattern in degree_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                education.append({
                    "degree": match.group(1),
                    "field": match.group(2).strip(),
                    "full_text": match.group(0)
                })
        
        return education
    
    def extract_experience_years(self, text: str) -> Optional[int]:
        """Extract years of experience from text"""
        experience_patterns = [
            r'(\d+)\+?\s*years?\s+(?:of\s+)?experience',
            r'(\d+)\+?\s*yrs?\s+(?:of\s+)?experience',
            r'experience.*?(\d+)\+?\s*years?',
            r'(\d+)\+?\s*years?\s+in'
        ]
        
        for pattern in experience_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return int(match.group(1))
        
        return None
    
    def clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove special characters but keep basic punctuation
        text = re.sub(r'[^\w\s\.\,\;\:\!\?\-\(\)]', ' ', text)
        
        # Remove extra spaces
        text = ' '.join(text.split())
        
        return text.strip()
    
    def get_text_statistics(self, text: str) -> Dict[str, int]:
        """Get basic statistics about the text"""
        words = text.split()
        sentences = text.split('.')
        
        return {
            "character_count": len(text),
            "word_count": len(words),
            "sentence_count": len([s for s in sentences if s.strip()]),
            "paragraph_count": len([p for p in text.split('\n\n') if p.strip()])
        }
