# AI Resume Intelligence

AI Resume Intelligence is a Python-based project that helps users analyze their resumes and understand how well they match a selected job role or a specific job description.

## Features

- Resume Upload: Supports PDF and TXT formats.
- Candidate Information Extraction: Extracts personal and professional details.
- Resume Completeness Analysis: Identifies missing resume sections.
- Technical Skills Analysis: Identifies skills mentioned in the resume.
- Job Role Matching: Compares resumes with selected job roles.
- Machine Learning Prediction: Predicts the probability associated with a selected job role.
- Job Description Comparison: Compares resumes with a given job description and identifies skill gaps.
- Report Generation: Generates downloadable resume analysis reports.

## Technologies Used

- Python
- Machine Learning
- Streamlit
- Pandas
- NumPy
- Scikit-learn
- PyPDF

## Project Structure

```text
AI-Resume-Intelligence/
│
├── app.py
├── analyzer.py
├── dashboard.py
├── job_matcher.py
├── job_roles.py
├── ml_predictor.py
├── report_generator.py
├── resume_parser.py
├── job_role_model.pkl
├── requirements.txt
├── README.md
└── .gitignore
```

## Installation

1. Clone the repository:

```bash
git clone https://github.com/salmiyaka/AI-Resume-Intelligence.git
```

2. Open the project folder:

```bash
cd AI-Resume-Intelligence
```

3. Install the required libraries:

```bash
pip install -r requirements.txt
```

4. Run the application:

```bash
python -m streamlit run app.py
```

## Project Purpose

This project was developed as a practical learning experience to apply Python, Machine Learning, and data analysis concepts to resume evaluation and job matching.
