# Resume Screening & Job Matching System

An AI-powered resume screening and job matching system that uses Natural Language Processing (NLP), TF-IDF vectorization, and cosine similarity to automatically match resumes with job postings.

## 🎯 Features

- **Resume Parsing**: Extract text, skills, experience, education, and contact information from PDF, DOCX, and TXT files
- **TF-IDF Vectorization**: Convert resumes and job descriptions into high-dimensional vectors for similarity comparison
- **Cosine Similarity Matching**: Calculate similarity scores between resumes and jobs using cosine similarity
- **Multi-factor Scoring**: Combine text similarity, skill overlap, and experience requirements for accurate matching
- **Web Interface**: User-friendly web application for uploading resumes and viewing matches
- **Job Management**: Add, edit, and manage job postings through the web interface

## 🛠️ Technology Stack

- **Backend**: Flask (Python)
- **NLP**: NLTK for text processing
- **ML**: scikit-learn for TF-IDF and cosine similarity
- **Frontend**: HTML, CSS, JavaScript
- **File Processing**: PyPDF2, python-docx for resume parsing

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

## 🚀 Installation

1. **Clone or download this repository**

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python app.py
   ```

4. **Open your browser** and navigate to:
   ```
   http://localhost:5000
   ```

## 📖 Usage

### Uploading a Resume

1. Go to the home page
2. Enter the candidate's name
3. Select a resume file (PDF, DOCX, or TXT)
4. Click "Upload & Analyze"
5. View the parsed resume information and top job matches

### Managing Job Postings

1. Navigate to the "Jobs" page
2. Click "+ Add New Job" to create a new job posting
3. Fill in the job details:
   - Job Title
   - Company Name
   - Description
   - Required Skills (comma-separated)
   - Minimum Experience
   - Location
   - Salary Range
4. Edit or delete existing jobs as needed

## 🔬 How It Works

### 1. Resume Parsing
- Extracts raw text from resume files
- Identifies skills using keyword matching and pattern recognition
- Extracts contact information (email, phone)
- Calculates years of experience
- Identifies education credentials

### 2. TF-IDF Vectorization
- Converts resume text and job descriptions into TF-IDF vectors
- Uses unigrams and bigrams for better feature representation
- Filters common stop words
- Creates a high-dimensional vector space for comparison

### 3. Cosine Similarity
- Calculates cosine similarity between resume and job vectors
- Returns similarity scores ranging from 0 to 1 (0% to 100%)

### 4. Multi-factor Matching
The final match score combines:
- **Text Similarity (60%)**: TF-IDF cosine similarity
- **Skill Match (30%)**: Percentage of required skills found in resume
- **Experience Match (10%)**: How well candidate's experience meets job requirements

## 📁 Project Structure

```
Resume Screening and Job Matching System/
│
├── app.py                 # Flask application and API endpoints
├── resume_parser.py      # Resume parsing and text extraction
├── job_matcher.py        # TF-IDF and cosine similarity matching
├── database.py           # File-based database for resumes and jobs
├── requirements.txt      # Python dependencies
├── README.md             # This file
│
├── templates/            # HTML templates
│   ├── base.html        # Base template
│   ├── index.html       # Home page
│   └── jobs.html        # Jobs management page
│
├── static/              # Static files
│   ├── style.css       # Stylesheet
│   └── script.js       # JavaScript utilities
│
├── uploads/             # Uploaded resume files (created automatically)
└── data/                # Database files (created automatically)
    ├── resumes.json    # Stored resumes
    └── jobs.json       # Stored job postings
```

## 🧪 ML Concepts Used

- **Natural Language Processing (NLP)**: Text extraction, tokenization, stop word removal
- **TF-IDF (Term Frequency-Inverse Document Frequency)**: Feature extraction and vectorization
- **Cosine Similarity**: Measuring similarity between documents in vector space
- **Feature Engineering**: Combining multiple factors (text, skills, experience) for better matching

## 🔧 API Endpoints

- `GET /` - Home page
- `GET /jobs` - Jobs management page
- `POST /api/upload-resume` - Upload and parse a resume
- `GET /api/resumes` - Get all parsed resumes
- `GET /api/resume/<id>/matches` - Get job matches for a resume
- `GET /api/jobs` - Get all job postings
- `POST /api/jobs` - Create a new job posting
- `GET /api/job/<id>` - Get a specific job
- `PUT /api/job/<id>` - Update a job posting
- `DELETE /api/job/<id>` - Delete a job posting

## 📝 Notes

- The system comes pre-loaded with 6 sample job postings
- Resume files are stored in the `uploads/` directory
- All data is stored in JSON files in the `data/` directory
- Maximum file upload size is 16MB
- Supported file formats: PDF, DOCX, DOC, TXT

## 🚀 Future Enhancements

- Integration with real databases (PostgreSQL, MongoDB)
- Advanced NLP models (BERT, GPT embeddings)
- Resume ranking and filtering
- Batch resume processing
- Export matching results to CSV/Excel
- User authentication and role-based access
- Email notifications for matches

## 📄 License

This project is open source and available for educational and commercial use.

## 👥 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

