# AI Resume Intelligence 

AI Resume Intelligence is a Python-based project developed using Machine Learning and Streamlit. It helps users analyze their resumes, evaluate their skills, and understand how well their profiles match selected job roles and specific job descriptions.

The system provides resume analysis, job matching, Machine Learning-based job role prediction, skill gap identification, and downloadable reports through an interactive dashboard.

## ✨ Features

### 1. Resume Upload
- Upload resumes in PDF and TXT formats.
- Extract information from uploaded resumes.

### 2. Resume Analysis
- Extract candidate information such as name, email, and contact details.
- Identify technical skills.
- Check resume completeness.
- Identify missing resume sections.

### 3. Job Role Matching
- Select a target job role.
- Compare resume skills with the selected role.
- Display matched and missing skills.
- Calculate a job role matching score.

### 4. Machine Learning Prediction
- Predict the job role based on resume information.
- Display the prediction probability for the selected role.

### 5. Job Description Comparison
- Compare an uploaded resume with a given job description.
- Calculate the matching score.
- Identify matched and missing skills.
- Highlight priority skills that need improvement.

### 6. Downloadable Report
- Generate a resume analysis report.
- Download the analysis results for future reference.

## 🛠️ Technologies Used

- **Programming Language:** Python
- **Machine Learning:** Scikit-learn
- **Data Analysis:** Pandas, NumPy
- **Frontend:** Streamlit
- **PDF Processing:** PyPDF

## 📂 Project Structure

```text
AI-Resume-Intelligence/
│
├── app.py
├── resume_parser.py
├── analyzer.py
├── job_matcher.py
├── job_roles.py
│
├── models/
│   └── job_role_model.pkl
│
├── screenshots/
│   ├── dashboard.png
│   ├── resume-analysis.png
│   └── job-description.png
│
├── requirements.txt
├── README.md
└── .gitignore
```

## 📸 Application Screenshots

### Main Dashboard

![Main Dashboard](screenshots/dashboard.png)

### Resume Analysis

![Resume Analysis](screenshots/resume-analysis.png)

### Job Description Comparison

![Job Description Comparison](screenshots/job-description.png)

## ⚙️ Installation and Setup

### Step 1: Clone the Repository

```bash
git clone https://github.com/salmiyaka/AI-Resume-Intelligence.git
```

### Step 2: Navigate to the Project Folder

```bash
cd AI-Resume-Intelligence
```

### Step 3: Install Required Libraries

```bash
pip install -r requirements.txt
```

### Step 4: Run the Application

```bash
python -m streamlit run app.py
```

The application will open in your browser.

## 🎯 Project Objective

The main objective of this project is to simplify resume evaluation and job matching by combining Python, Machine Learning, and data analysis techniques.

It aims to help users understand their resume strengths, identify skill gaps, and improve their preparation for specific job opportunities.

## 👩‍💻 Author

**Salmiya K A**

GitHub: [salmiyaka](https://github.com/salmiyaka)

---

⭐ If you find this project interesting, feel free to explore the repository!
