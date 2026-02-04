from flask import Flask, render_template, request, jsonify, send_from_directory
import os
import sys
import json
from werkzeug.utils import secure_filename

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from resume_parser import ResumeParser
from job_matcher import JobMatcher
from database import Database

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['ALLOWED_EXTENSIONS'] = {'pdf', 'docx', 'txt', 'doc'}

# Initialize components
db = Database()
resume_parser = ResumeParser()
job_matcher = JobMatcher()

# Create uploads directory if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs('static', exist_ok=True)
os.makedirs('templates', exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    """Main page with resume upload and job matching interface"""
    return render_template('index.html')

@app.route('/about')
def about():
    """About page with system information"""
    return render_template('about.html')

@app.route('/jobs')
def jobs():
    """Page to view and manage job postings"""
    jobs = db.get_all_jobs()
    return render_template('jobs.html', jobs=jobs)

@app.route('/api/upload-resume', methods=['POST'])
def upload_resume():
    """API endpoint to upload and parse a resume"""
    if 'resume' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['resume']
    candidate_name = request.form.get('candidate_name', 'Unknown')
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if file and file.filename and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        try:
            # Parse resume
            resume_data = resume_parser.parse(filepath)
            resume_data['candidate_name'] = candidate_name
            resume_data['filename'] = filename
            
            # Save to database
            resume_id = db.save_resume(resume_data)
            
            # Get job matches
            matches = job_matcher.find_matches(resume_data, top_n=5)
            
            return jsonify({
                'success': True,
                'resume_id': resume_id,
                'resume_data': resume_data,
                'matches': matches
            })
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'error': 'Invalid file type'}), 400

@app.route('/api/resumes')
def get_resumes():
    """Get all parsed resumes"""
    resumes = db.get_all_resumes()
    return jsonify(resumes)

@app.route('/api/resume/<int:resume_id>/matches')
def get_resume_matches(resume_id):
    """Get job matches for a specific resume"""
    resume = db.get_resume(resume_id)
    if not resume:
        return jsonify({'error': 'Resume not found'}), 404
    
    matches = job_matcher.find_matches(resume, top_n=10)
    return jsonify(matches)

@app.route('/api/jobs', methods=['GET', 'POST'])
def manage_jobs():
    """Get all jobs or create a new job posting"""
    if request.method == 'POST':
        job_data = request.json
        if not job_data:
            return jsonify({'error': 'No job data provided'}), 400
        job_id = db.save_job(job_data)
        return jsonify({'success': True, 'job_id': job_id})
    else:
        jobs = db.get_all_jobs()
        return jsonify(jobs)

@app.route('/api/job/<int:job_id>', methods=['GET', 'PUT', 'DELETE'])
def manage_job(job_id):
    """Get, update, or delete a specific job"""
    if request.method == 'GET':
        job = db.get_job(job_id)
        if not job:
            return jsonify({'error': 'Job not found'}), 404
        return jsonify(job)
    elif request.method == 'PUT':
        job_data = request.json
        if not job_data:
            return jsonify({'error': 'No job data provided'}), 400
        db.update_job(job_id, job_data)
        return jsonify({'success': True})
    elif request.method == 'DELETE':
        db.delete_job(job_id)
        return jsonify({'success': True})
    else:
        return jsonify({'error': 'Method not allowed'}), 405

if __name__ == '__main__':
    # Initialize with sample jobs
    db.initialize_sample_jobs()
    app.run(debug=True, port=5000)

