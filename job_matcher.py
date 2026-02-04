import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from typing import Dict, List
import pickle
import os

class JobMatcher:
    """Match resumes to job postings using TF-IDF and cosine similarity"""
    
    def __init__(self):
        self.vectorizer = TfidfVectorizer(
            max_features=5000,
            stop_words='english',
            ngram_range=(1, 2),  # Unigrams and bigrams
            min_df=1,
            max_df=0.95
        )
        self.fitted = False
        self.job_vectors = None
        self.job_ids = []
    
    def fit_vectorizer(self, job_descriptions: List[str], job_ids: List[int] = None):
        """Fit TF-IDF vectorizer on job descriptions"""
        if not job_descriptions:
            return
        
        # Combine job title, description, and required skills
        combined_texts = []
        for job in job_descriptions:
            if isinstance(job, dict):
                text = f"{job.get('title', '')} {job.get('description', '')} {' '.join(job.get('required_skills', []))}"
            else:
                text = str(job)
            combined_texts.append(text)
        
        # Fit and transform
        self.job_vectors = self.vectorizer.fit_transform(combined_texts)
        self.job_ids = job_ids if job_ids else list(range(len(job_descriptions)))
        self.fitted = True
    
    def create_resume_vector(self, resume_data: Dict) -> np.ndarray:
        """Create TF-IDF vector for a resume"""
        if not self.fitted:
            raise ValueError("Vectorizer must be fitted first")
        
        # Combine resume text components
        resume_text = f"{resume_data.get('cleaned_text', '')} {' '.join(resume_data.get('skills', []))}"
        
        # Transform resume to vector space
        resume_vector = self.vectorizer.transform([resume_text])
        return resume_vector
    
    def calculate_similarity(self, resume_vector: np.ndarray, job_vectors: np.ndarray) -> np.ndarray:
        """Calculate cosine similarity between resume and jobs"""
        similarities = cosine_similarity(resume_vector, job_vectors)[0]
        return similarities
    
    def find_matches(self, resume_data: Dict, jobs: List[Dict] = None, top_n: int = 5) -> List[Dict]:
        """Find top matching jobs for a resume"""
        if jobs is None:
            from database import Database
            db = Database()
            jobs = db.get_all_jobs()
        
        if not jobs:
            return []
        
        # Fit vectorizer if not already fitted or if jobs changed
        job_ids = [job['id'] for job in jobs]
        self.fit_vectorizer(jobs, job_ids)
        
        # Create resume vector
        resume_vector = self.create_resume_vector(resume_data)
        
        # Calculate similarities
        similarities = self.calculate_similarity(resume_vector, self.job_vectors)
        
        # Get top matches
        top_indices = np.argsort(similarities)[::-1][:top_n]
        
        matches = []
        for idx in top_indices:
            if similarities[idx] > 0:  # Only include matches with similarity > 0
                job = jobs[idx]
                match_score = float(similarities[idx] * 100)  # Convert to percentage
                
                # Calculate additional matching features
                skill_match = self.calculate_skill_match(
                    resume_data.get('skills', []),
                    job.get('required_skills', [])
                )
                
                experience_match = self.calculate_experience_match(
                    resume_data.get('experience', {}).get('years', 0),
                    job.get('min_experience', 0)
                )
                
                matches.append({
                    'job_id': job['id'],
                    'job_title': job.get('title', 'Unknown'),
                    'company': job.get('company', 'Unknown'),
                    'similarity_score': round(match_score, 2),
                    'skill_match': skill_match,
                    'experience_match': experience_match,
                    'overall_score': round((match_score * 0.6 + skill_match * 30 + experience_match * 10), 2),
                    'job_description': job.get('description', ''),
                    'required_skills': job.get('required_skills', [])
                })
        
        # Sort by overall score
        matches.sort(key=lambda x: x['overall_score'], reverse=True)
        return matches
    
    def calculate_skill_match(self, resume_skills: List[str], job_skills: List[str]) -> float:
        """Calculate percentage of matching skills"""
        if not job_skills:
            return 0.0
        
        resume_skills_lower = [s.lower() for s in resume_skills]
        job_skills_lower = [s.lower() for s in job_skills]
        
        matched_skills = sum(1 for skill in job_skills_lower if any(rs in skill or skill in rs for rs in resume_skills_lower))
        
        return (matched_skills / len(job_skills)) * 100 if job_skills else 0.0
    
    def calculate_experience_match(self, resume_years: float, job_min_years: float) -> float:
        """Calculate experience match score"""
        if job_min_years == 0:
            return 100.0
        
        if resume_years >= job_min_years:
            return 100.0
        else:
            # Partial match based on percentage
            return max(0, (resume_years / job_min_years) * 100)
    
    def get_matching_skills(self, resume_skills: List[str], job_skills: List[str]) -> List[str]:
        """Get list of matching skills between resume and job"""
        resume_skills_lower = [s.lower() for s in resume_skills]
        job_skills_lower = [s.lower() for s in job_skills]
        
        matching = []
        for job_skill in job_skills_lower:
            for resume_skill in resume_skills_lower:
                if job_skill in resume_skill or resume_skill in job_skill:
                    matching.append(job_skill)
                    break
        
        return matching
    
    def get_missing_skills(self, resume_skills: List[str], job_skills: List[str]) -> List[str]:
        """Get list of skills required by job but missing in resume"""
        resume_skills_lower = [s.lower() for s in resume_skills]
        job_skills_lower = [s.lower() for s in job_skills]
        
        missing = []
        for job_skill in job_skills_lower:
            if not any(job_skill in rs or rs in job_skill for rs in resume_skills_lower):
                missing.append(job_skill)
        
        return missing

