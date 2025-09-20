from flask import Flask, request, render_template, send_file
import os
import PyPDF2
import docx
import spacy
import pandas as pd
import re

app = Flask(_name_)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['REPORT_FOLDER'] = 'reports'

nlp = spacy.load('en_core_web_sm')

criteria = {
    'education': 30,
    'experience': 40,
    'skills': 30
}

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])
if not os.path.exists(app.config['REPORT_FOLDER']):
    os.makedirs(app.config['REPORT_FOLDER'])

def extract_pdf(file_path):
    text = ''
    with open(file_path, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            text += page.extract_text()
    return text

def extract_docx(file_path):
    doc = docx.Document(file_path)
    text = ''
    for para in doc.paragraphs:
        text += para.text + ' '
    return text

def parse_resume(file_path, file_ext):
    if file_ext == '.pdf':
        text = extract_pdf(file_path)
    elif file_ext == '.docx':
        text = extract_docx(file_path)
    else:
        text = ''
    return text.lower()

def extract_experience(text):
    # Find numbers followed by 'year' or 'years'
    matches = re.findall(r'(\d+)\s+year', text)
    total_exp = sum(int(x) for x in matches)
    return total_exp

def detect_education(text):
    degrees = ['phd', 'doctor', 'master', 'bachelor', 'mba', 'b.sc', 'm.sc']
    for degree in degrees:
        if degree in text:
            return True
    return False

def detect_skills(text, required_skills):
    found = [skill for skill in required_skills if skill.lower() in text]
    return found

def score_resume(text, required_skills):
    score = 0
    # Education
    if detect_education(text):
        score += criteria['education']
    # Experience
    exp_years = extract_experience(text)
    exp_score = min((exp_years / 5) * criteria['experience'], criteria['experience'])  # Max 40 points
    score += exp_score
    # Skills
    skills_found = detect_skills(text, required_skills)
    skills_score = (len(skills_found) / len(required_skills)) * criteria['skills']
    score += skills_score
    return score, exp_years, skills_found

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        required_skills = request.form.get('skills').split(',')
        uploaded_files = request.files.getlist('resumes')
        
        candidates = []
        for file in uploaded_files:
            filename = file.filename
            file_ext = os.path.splitext(filename)[1]
            save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(save_path)
            
            text = parse_resume(save_path, file_ext)
            score, exp_years, skills_found = score_resume(text, required_skills)
            
            candidates.append({
                'name': filename,
                'score': round(score, 2),
                'experience': exp_years,
                'skills_found': ', '.join(skills_found)
            })
        
        # Pick the best candidate
        best_candidate = max(candidates, key=lambda x: x['score'])
        
        # Generate CSV report
        df = pd.DataFrame(candidates)
        report_path = os.path.join(app.config['REPORT_FOLDER'], 'resume_report.csv')
        df.to_csv(report_path, index=False)
        
        return render_template('index.html', best_candidate=best_candidate, candidates=candidates, report_ready=True)
    
    return render_template('index.html', best_candidate=None, candidates=None, report_ready=False)

@app.route('/download')
def download_report():
    report_path = os.path.join(app.config['REPORT_FOLDER'], 'resume_report.csv')

    return send_file(report_path, as_attachment=True)

if _name_ == '_main_':
    app.run(debug=True)
enakku varla pahfrom flask import Flask, request, render_template, send_file
import os
import PyPDF2
import docx
import spacy
import pandas as pd
import re

app = Flask(_name_)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['REPORT_FOLDER'] = 'reports'

nlp = spacy.load('en_core_web_sm')

criteria = {
    'education': 30,
    'experience': 40,
    'skills': 30
}

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])
if not os.path.exists(app.config['REPORT_FOLDER']):
    os.makedirs(app.config['REPORT_FOLDER'])

def extract_pdf(file_path):
    text = ''
    with open(file_path, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            text += page.extract_text()
    return text

def extract_docx(file_path):
    doc = docx.Document(file_path)
    text = ''
    for para in doc.paragraphs:
        text += para.text + ' '
    return text

def parse_resume(file_path, file_ext):
    if file_ext == '.pdf':
        text = extract_pdf(file_path)
    elif file_ext == '.docx':
        text = extract_docx(file_path)
    else:
        text = ''
    return text.lower()

def extract_experience(text):
    # Find numbers followed by 'year' or 'years'
    matches = re.findall(r'(\d+)\s+year', text)
    total_exp = sum(int(x) for x in matches)
    return total_exp

def detect_education(text):
    degrees = ['phd', 'doctor', 'master', 'bachelor', 'mba', 'b.sc', 'm.sc']
    for degree in degrees:
        if degree in text:
            return True
    return False

def detect_skills(text, required_skills):
    found = [skill for skill in required_skills if skill.lower() in text]
    return found

def score_resume(text, required_skills):
    score = 0
    # Education
    if detect_education(text):
        score += criteria['education']
    # Experience
    exp_years = extract_experience(text)
    exp_score = min((exp_years / 5) * criteria['experience'], criteria['experience'])  # Max 40 points
    score += exp_score
    # Skills
    skills_found = detect_skills(text, required_skills)
    skills_score = (len(skills_found) / len(required_skills)) * criteria['skills']
    score += skills_score
    return score, exp_years, skills_found

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        required_skills = request.form.get('skills').split(',')
        uploaded_files = request.files.getlist('resumes')
        
        candidates = []
        for file in uploaded_files:
            filename = file.filename
            file_ext = os.path.splitext(filename)[1]
            save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(save_path)
            
            text = parse_resume(save_path, file_ext)
            score, exp_years, skills_found = score_resume(text, required_skills)
            
            candidates.append({
                'name': filename,
                'score': round(score, 2),
                'experience': exp_years,
                'skills_found': ', '.join(skills_found)
            })
        
        # Pick the best candidate
        best_candidate = max(candidates, key=lambda x: x['score'])
        
        # Generate CSV report
        df = pd.DataFrame(candidates)
        report_path = os.path.join(app.config['REPORT_FOLDER'], 'resume_report.csv')
        df.to_csv(report_path, index=False)
        
        return render_template('index.html', best_candidate=best_candidate, candidates=candidates, report_ready=True)
    
    return render_template('index.html', best_candidate=None, candidates=None, report_ready=False)

@app.route('/download')
def download_report():
    report_path = os.path.join(app.config['REPORT_FOLDER'], 'resume_report.csv')

    return send_file(report_path, as_attachment=True)

if _name_ == '_main_':
    app.run(debug=True)
enakku varla pah
