import json
import os
from typing import Dict, List, Optional

class Database:
    """Simple file-based database for storing resumes and jobs"""
    
    def __init__(self, data_dir='data'):
        self.data_dir = data_dir
        self.resumes_file = os.path.join(data_dir, 'resumes.json')
        self.jobs_file = os.path.join(data_dir, 'jobs.json')
        
        # Create data directory if it doesn't exist
        os.makedirs(data_dir, exist_ok=True)
        
        # Initialize files if they don't exist
        if not os.path.exists(self.resumes_file):
            self._save_resumes([])
        
        if not os.path.exists(self.jobs_file):
            self._save_jobs([])
            self.initialize_sample_jobs()
    
    def _load_resumes(self) -> List[Dict]:
        """Load all resumes from file"""
        try:
            with open(self.resumes_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []
    
    def _save_resumes(self, resumes: List[Dict]):
        """Save resumes to file"""
        with open(self.resumes_file, 'w', encoding='utf-8') as f:
            json.dump(resumes, f, indent=2, ensure_ascii=False)
    
    def _load_jobs(self) -> List[Dict]:
        """Load all jobs from file"""
        try:
            with open(self.jobs_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []
    
    def _save_jobs(self, jobs: List[Dict]):
        """Save jobs to file"""
        with open(self.jobs_file, 'w', encoding='utf-8') as f:
            json.dump(jobs, f, indent=2, ensure_ascii=False)
    
    def save_resume(self, resume_data: Dict) -> int:
        """Save a new resume and return its ID"""
        resumes = self._load_resumes()
        
        # Generate new ID
        if resumes:
            new_id = max(r.get('id', 0) for r in resumes) + 1
        else:
            new_id = 1
        
        resume_data['id'] = new_id
        resumes.append(resume_data)
        self._save_resumes(resumes)
        
        return new_id
    
    def get_resume(self, resume_id: int) -> Optional[Dict]:
        """Get a resume by ID"""
        resumes = self._load_resumes()
        for resume in resumes:
            if resume.get('id') == resume_id:
                return resume
        return None
    
    def get_all_resumes(self) -> List[Dict]:
        """Get all resumes"""
        return self._load_resumes()
    
    def save_job(self, job_data: Dict) -> int:
        """Save a new job and return its ID"""
        jobs = self._load_jobs()
        
        # Generate new ID
        if jobs:
            new_id = max(j.get('id', 0) for j in jobs) + 1
        else:
            new_id = 1
        
        job_data['id'] = new_id
        jobs.append(job_data)
        self._save_jobs(jobs)
        
        return new_id
    
    def get_job(self, job_id: int) -> Optional[Dict]:
        """Get a job by ID"""
        jobs = self._load_jobs()
        for job in jobs:
            if job.get('id') == job_id:
                return job
        return None
    
    def get_all_jobs(self) -> List[Dict]:
        """Get all jobs"""
        return self._load_jobs()
    
    def update_job(self, job_id: int, job_data: Dict):
        """Update an existing job"""
        jobs = self._load_jobs()
        for i, job in enumerate(jobs):
            if job.get('id') == job_id:
                job_data['id'] = job_id
                jobs[i] = job_data
                self._save_jobs(jobs)
                return
        raise ValueError(f"Job with ID {job_id} not found")
    
    def delete_job(self, job_id: int):
        """Delete a job"""
        jobs = self._load_jobs()
        jobs = [j for j in jobs if j.get('id') != job_id]
        self._save_jobs(jobs)
    
    def initialize_sample_jobs(self):
        """Initialize database with sample job postings"""
        jobs = self._load_jobs()
        if jobs:  # Don't reinitialize if jobs already exist
            return
        
        sample_jobs = [
            {
                'id': 1,
                'title': 'Senior Python Developer',
                'company': 'Infosys',
                'description': 'Join Infosys as a Senior Python Developer. Work on enterprise-level applications, microservices, and cloud-based solutions. Collaborate with global teams to deliver high-quality software solutions for Fortune 500 clients.',
                'required_skills': ['Python', 'Django', 'Flask', 'REST API', 'PostgreSQL', 'Docker', 'Git', 'AWS'],
                'min_experience': 5,
                'location': 'Bangalore, Karnataka',
                'salary_range': '₹12,00,000 - ₹20,00,000'
            },
            {
                'id': 2,
                'title': 'Machine Learning Engineer',
                'company': 'TCS',
                'description': 'TCS is hiring Machine Learning Engineers to work on AI/ML projects for global clients. Develop and deploy ML models, work with data science teams, and implement MLOps practices. Experience with production ML systems required.',
                'required_skills': ['Python', 'Machine Learning', 'TensorFlow', 'PyTorch', 'Scikit-learn', 'Pandas', 'Numpy', 'SQL', 'MLOps'],
                'min_experience': 3,
                'location': 'Mumbai, Maharashtra',
                'salary_range': '₹10,00,000 - ₹18,00,000'
            },
            {
                'id': 3,
                'title': 'Full Stack Developer',
                'company': 'Wipro',
                'description': 'Wipro is looking for Full Stack Developers to build scalable web applications. Work on both frontend and backend development, participate in agile sprints, and deliver features for client projects across various domains.',
                'required_skills': ['JavaScript', 'React', 'Node.js', 'MongoDB', 'Express', 'HTML', 'CSS', 'Git', 'REST API'],
                'min_experience': 2,
                'location': 'Bangalore, Karnataka',
                'salary_range': '₹6,00,000 - ₹12,00,000'
            },
            {
                'id': 4,
                'title': 'Data Scientist',
                'company': 'HCL Technologies',
                'description': 'HCL is seeking Data Scientists to analyze business data and build predictive analytics solutions. Work with stakeholders to understand requirements, create data models, and provide actionable insights using advanced analytics.',
                'required_skills': ['Python', 'R', 'SQL', 'Machine Learning', 'Data Science', 'Pandas', 'Tableau', 'Statistics', 'Power BI'],
                'min_experience': 4,
                'location': 'Noida, Uttar Pradesh',
                'salary_range': '₹9,00,000 - ₹16,00,000'
            },
            {
                'id': 5,
                'title': 'DevOps Engineer',
                'company': 'Tech Mahindra',
                'description': 'Tech Mahindra requires DevOps Engineers to manage cloud infrastructure, automate deployments, and maintain CI/CD pipelines. Work with AWS/Azure, containerization technologies, and ensure system reliability and scalability.',
                'required_skills': ['AWS', 'Docker', 'Kubernetes', 'CI/CD', 'Linux', 'Python', 'Terraform', 'Jenkins', 'GitLab'],
                'min_experience': 3,
                'location': 'Pune, Maharashtra',
                'salary_range': '₹8,00,000 - ₹15,00,000'
            },
            {
                'id': 6,
                'title': 'Frontend Developer',
                'company': 'Flipkart',
                'description': 'Flipkart is hiring Frontend Developers to build user interfaces for our e-commerce platform. Work on React-based applications, optimize performance, and create seamless shopping experiences for millions of users.',
                'required_skills': ['React', 'TypeScript', 'HTML', 'CSS', 'JavaScript', 'Redux', 'Webpack', 'Git', 'Responsive Design'],
                'min_experience': 2,
                'location': 'Bangalore, Karnataka',
                'salary_range': '₹8,00,000 - ₹15,00,000'
            }
        ]
        
        self._save_jobs(sample_jobs)

