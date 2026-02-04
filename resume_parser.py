import re
import docx
import PyPDF2
from typing import Dict, List
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords', quiet=True)

class ResumeParser:
    """Extract and parse information from resume files"""
    
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))
        # Common skills keywords
        self.skill_keywords = [
            'python', 'java', 'javascript', 'react', 'node', 'sql', 'mongodb',
            'aws', 'docker', 'kubernetes', 'git', 'linux', 'machine learning',
            'deep learning', 'tensorflow', 'pytorch', 'nlp', 'data science',
            'pandas', 'numpy', 'scikit-learn', 'django', 'flask', 'angular',
            'vue', 'html', 'css', 'typescript', 'c++', 'c#', 'php', 'ruby',
            'go', 'rust', 'swift', 'kotlin', 'scala', 'r', 'matlab', 'excel',
            'tableau', 'power bi', 'agile', 'scrum', 'devops', 'ci/cd',
            'rest api', 'graphql', 'microservices', 'blockchain', 'cybersecurity'
        ]
    
    def extract_text_from_pdf(self, filepath: str) -> str:
        """Extract text from PDF file"""
        text = ""
        try:
            with open(filepath, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
        except Exception as e:
            raise Exception(f"Error reading PDF: {str(e)}")
        return text
    
    def extract_text_from_docx(self, filepath: str) -> str:
        """Extract text from DOCX file"""
        text = ""
        try:
            doc = docx.Document(filepath)
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
        except Exception as e:
            raise Exception(f"Error reading DOCX: {str(e)}")
        return text
    
    def extract_text_from_txt(self, filepath: str) -> str:
        """Extract text from TXT file"""
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                return file.read()
        except Exception as e:
            raise Exception(f"Error reading TXT: {str(e)}")
    
    def extract_text(self, filepath: str) -> str:
        """Extract text from resume file based on extension"""
        ext = filepath.rsplit('.', 1)[-1].lower()
        
        if ext == 'pdf':
            return self.extract_text_from_pdf(filepath)
        elif ext in ['docx', 'doc']:
            return self.extract_text_from_docx(filepath)
        elif ext == 'txt':
            return self.extract_text_from_txt(filepath)
        else:
            raise Exception(f"Unsupported file type: {ext}")
    
    def extract_email(self, text: str) -> str:
        """Extract email address from text"""
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, text)
        return emails[0] if emails else ""
    
    def extract_phone(self, text: str) -> str:
        """Extract phone number from text"""
        phone_patterns = [
            r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
            r'\(\d{3}\)\s?\d{3}[-.]?\d{4}',
            r'\+\d{1,3}[-.]?\d{1,4}[-.]?\d{1,4}[-.]?\d{1,9}'
        ]
        for pattern in phone_patterns:
            phones = re.findall(pattern, text)
            if phones:
                return phones[0]
        return ""
    
    def extract_skills(self, text: str) -> List[str]:
        """Extract skills from resume text"""
        text_lower = text.lower()
        found_skills = []
        
        for skill in self.skill_keywords:
            if skill.lower() in text_lower:
                found_skills.append(skill)
        
        # Also look for skills mentioned in common formats
        skill_patterns = [
            r'skills?[:\-]?\s*([^\n]+)',
            r'technical skills?[:\-]?\s*([^\n]+)',
            r'proficienc(?:y|ies)[:\-]?\s*([^\n]+)'
        ]
        
        for pattern in skill_patterns:
            matches = re.findall(pattern, text_lower, re.IGNORECASE)
            for match in matches:
                # Extract individual skills from the match
                skills = re.split(r'[,;|•\-\n]', match)
                for skill in skills:
                    skill = skill.strip()
                    if len(skill) > 2 and skill not in found_skills:
                        found_skills.append(skill)
        
        return list(set(found_skills))  # Remove duplicates
    
    def extract_experience(self, text: str) -> Dict:
        """Extract work experience information"""
        experience = {
            'years': 0,
            'companies': [],
            'positions': []
        }
        
        # Look for years of experience
        exp_patterns = [
            r'(\d+)\+?\s*years?\s*(?:of\s*)?experience',
            r'experience[:\-]?\s*(\d+)\+?\s*years?'
        ]
        
        for pattern in exp_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                try:
                    experience['years'] = max([int(m) for m in matches])
                except:
                    pass
        
        # Extract company names and positions (simplified)
        # In production, use more sophisticated NLP models
        lines = text.split('\n')
        for line in lines:
            if any(keyword in line.lower() for keyword in ['engineer', 'developer', 'manager', 'analyst', 'specialist']):
                experience['positions'].append(line.strip())
        
        return experience
    
    def extract_education(self, text: str) -> List[str]:
        """Extract education information"""
        education = []
        degree_patterns = [
            r'(?:bachelor|master|ph\.?d|doctorate|mba|b\.?s|m\.?s|b\.?a|m\.?a)',
            r'(?:degree|diploma|certification)'
        ]
        
        lines = text.split('\n')
        for line in lines:
            if any(re.search(pattern, line, re.IGNORECASE) for pattern in degree_patterns):
                education.append(line.strip())
        
        return education
    
    def clean_text(self, text: str) -> str:
        """Clean and preprocess text"""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove special characters but keep basic punctuation
        text = re.sub(r'[^\w\s\.\,\!\?\-]', ' ', text)
        return text.strip()
    
    def parse(self, filepath: str) -> Dict:
        """Main parsing function that extracts all information from resume"""
        # Extract raw text
        raw_text = self.extract_text(filepath)
        cleaned_text = self.clean_text(raw_text)
        
        # Extract structured information
        parsed_data = {
            'raw_text': raw_text,
            'cleaned_text': cleaned_text,
            'email': self.extract_email(raw_text),
            'phone': self.extract_phone(raw_text),
            'skills': self.extract_skills(raw_text),
            'experience': self.extract_experience(raw_text),
            'education': self.extract_education(raw_text),
            'word_count': len(cleaned_text.split()),
            'char_count': len(cleaned_text)
        }
        
        return parsed_data

