import re
import os
import joblib

from job_roles import JOB_ROLES


# =========================================================
# ML MODEL
# =========================================================

MODEL_PATH = os.path.join(
    os.path.dirname(__file__),
    "models",
    "job_role_model.pkl"
)


def load_ml_model():
    """
    Load the trained ML job-role prediction model.
    """

    if not os.path.exists(MODEL_PATH):
        return None

    try:
        return joblib.load(MODEL_PATH)
    except Exception:
        return None


# =========================================================
# ML JOB ROLE PREDICTION
# =========================================================

def predict_job_role_ml(text):
    """
    Predict suitable job roles using the trained ML model.
    """

    model = load_ml_model()

    if model is None:
        return {
            "available": False,
            "predicted_role": None,
            "confidence": 0.0,
            "probabilities": []
        }

    try:

        probabilities = model.predict_proba(
            [text]
        )[0]

        roles = model.classes_

        results = []

        for role, probability in zip(
            roles,
            probabilities
        ):

            results.append(
                {
                    "role": role,
                    "score": round(
                        probability * 100,
                        2
                    )
                }
            )

        # Highest probability first
        results.sort(
            key=lambda item: item["score"],
            reverse=True
        )

        return {
            "available": True,
            "predicted_role": results[0]["role"],
            "confidence": results[0]["score"],
            "probabilities": results
        }

    except Exception:

        return {
            "available": False,
            "predicted_role": None,
            "confidence": 0.0,
            "probabilities": []
        }


# =========================================================
# RESUME SECTIONS
# =========================================================

REQUIRED_SECTIONS = {

    "Contact Details": [
        "email",
        "phone",
        "linkedin",
        "contact"
    ],

    "Career Objective": [
        "career objective",
        "objective",
        "professional summary",
        "summary"
    ],

    "Education": [
        "education",
        "academic"
    ],

    "Skills": [
        "skills",
        "technical skills"
    ],

    "Experience": [
        "experience",
        "work experience",
        "internship",
        "employment"
    ],

    "Projects": [
        "projects",
        "project"
    ],

    "Certifications": [
        "certifications",
        "certification",
        "certificate",
        "certificates",
        "workshop"
    ],

    "Languages": [
        "languages",
        "language"
    ],

    "Achievements": [
        "achievements",
        "achievement"
    ]
}


# =========================================================
# SKILLS
# =========================================================

SKILLS_LIST = [

    "Python",
    "Java",
    "C++",
    "C",
    "SQL",
    "MySQL",
    "SQLite",

    "HTML",
    "CSS",
    "JavaScript",
    "PHP",

    "Django",
    "Flask",

    "NumPy",
    "Pandas",
    "TensorFlow",

    "Machine Learning",
    "Data Science",
    "Data Analysis",

    "Excel",
    "Power BI",
    "Tableau",

    "Git",
    "GitHub",

    "Bootstrap",
    "OOP"
]


# =========================================================
# TEXT CLEANING
# =========================================================

def clean_line(line):

    line = line.replace(
        "\xa0",
        " "
    )

    line = re.sub(
        r"\s+",
        " ",
        line
    )

    return line.strip()


# =========================================================
# EMAIL
# =========================================================

def find_email(text):

    match = re.search(
        r"[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}",
        text
    )

    if match:
        return match.group(0)

    return None


# =========================================================
# PHONE
# =========================================================

def find_phone(text):

    patterns = [

        r"(?<!\d)(?:\+91[\s-]?)?[6-9]\d{9}(?!\d)",

        r"(?<!\d)\d{10}(?!\d)"
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text
        )

        if match:
            return match.group(0)

    return None


# =========================================================
# LINKEDIN
# =========================================================

def find_linkedin(text):

    match = re.search(
        r"(?:https?://)?(?:www\.)?linkedin\.com/[^\s|,]+",
        text,
        re.IGNORECASE
    )

    if match:

        return match.group(0).rstrip(
            ".,;)"
        )

    return None


# =========================================================
# GITHUB
# =========================================================

def find_github(text):

    match = re.search(
        r"(?:https?://)?(?:www\.)?github\.com/[^\s|,]+",
        text,
        re.IGNORECASE
    )

    if match:

        return match.group(0).rstrip(
            ".,;)"
        )

    return None


# =========================================================
# NAME DETECTION
# =========================================================

def find_name(text):

    lines = [
        clean_line(line)
        for line in text.splitlines()
        if clean_line(line)
    ]

    blocked = {

        "resume",
        "cv",
        "curriculum vitae",
        "profile",
        "summary",
        "professional summary",
        "career objective",
        "objective",
        "contact",
        "contact details",
        "education",
        "skills",
        "technical skills",
        "experience",
        "work experience",
        "internship",
        "projects",
        "certifications",
        "certification",
        "languages",
        "achievements"
    }

    # -----------------------------------------------------
    # FIRST: Search first 10 meaningful lines
    # -----------------------------------------------------

    for line in lines[:10]:

        lower = line.lower().strip()

        if lower in blocked:
            continue

        if "@" in line:
            continue

        if "linkedin.com" in lower:
            continue

        if "github.com" in lower:
            continue

        if re.search(
            r"\d{7,}",
            line
        ):
            continue

        words = line.split()

        if not (
            1 <= len(words) <= 5
        ):
            continue

        valid = True

        for word in words:

            cleaned = (
                word
                .replace(".", "")
                .replace("-", "")
            )

            if not cleaned.isalpha():
                valid = False
                break

            if len(cleaned) == 1:
                continue

            if (
                len(cleaned) == 2
                and word.endswith(".")
            ):
                continue

            if len(cleaned) >= 3:
                continue

            valid = False
            break

        if valid:

            if any(
                len(
                    word
                    .replace(".", "")
                    .replace("-", "")
                ) >= 3
                for word in words
            ):

                return line

    # -----------------------------------------------------
    # SECOND FALLBACK
    # -----------------------------------------------------

    for line in lines:

        lower = line.lower()

        if lower in {
            "professional summary",
            "career objective",
            "objective",
            "technical skills",
            "skills",
            "education"
        }:
            break

        if "@" in line:
            continue

        if "linkedin.com" in lower:
            continue

        if "github.com" in lower:
            continue

        if re.search(
            r"\d{7,}",
            line
        ):
            continue

        words = line.split()

        if not (
            1 <= len(words) <= 5
        ):
            continue

        if all(
            word
            .replace(".", "")
            .replace("-", "")
            .isalpha()
            for word in words
        ):

            if any(
                len(
                    word
                    .replace(".", "")
                    .replace("-", "")
                ) >= 3
                for word in words
            ):

                return line

    return None


# =========================================================
# SKILL DETECTION
# =========================================================

def find_skills(text):

    found = []

    text_lower = text.lower()

    for skill in SKILLS_LIST:

        pattern = (
            r"(?<![a-zA-Z0-9+#])"
            + re.escape(
                skill.lower()
            )
            + r"(?![a-zA-Z0-9+#])"
        )

        if re.search(
            pattern,
            text_lower
        ):

            if skill not in found:

                found.append(skill)

    return found


# =========================================================
# SECTION DETECTION
# =========================================================

def check_sections(text):

    text_lower = text.lower()

    sections = {}

    for section, keywords in REQUIRED_SECTIONS.items():

        sections[section] = any(
            keyword.lower() in text_lower
            for keyword in keywords
        )

    return sections


# =========================================================
# COMPLETENESS
# =========================================================

def calculate_completeness(sections):

    total = len(sections)

    present = sum(
        1
        for value in sections.values()
        if value
    )

    if total == 0:
        return 0.0

    return round(
        (present / total) * 100,
        2
    )


# =========================================================
# JOB MATCHING
# =========================================================

def calculate_job_match(
    skills,
    selected_role
):

    required = JOB_ROLES.get(
        selected_role,
        []
    )

    if not isinstance(
        required,
        list
    ):

        required = []

    found_lower = {
        skill.lower()
        for skill in skills
    }

    matched = []
    missing = []

    for skill in required:

        if skill.lower() in found_lower:

            matched.append(
                skill
            )

        else:

            missing.append(
                skill
            )

    if len(required) > 0:

        percentage = round(
            (
                len(matched)
                /
                len(required)
            )
            * 100,
            2
        )

    else:

        percentage = 0.0

    return {

        "percentage": percentage,

        "matched": matched,

        "missing": missing
    }


# =========================================================
# SUGGESTIONS
# =========================================================

def generate_suggestions(
    name,
    email,
    phone,
    linkedin,
    github,
    sections
):

    suggestions = []

    if not name:

        suggestions.append(
            "Add your full name clearly at the top of the resume."
        )

    if not email:

        suggestions.append(
            "Add your email address."
        )

    if not phone:

        suggestions.append(
            "Add your phone number."
        )

    if not linkedin:

        suggestions.append(
            "Add your LinkedIn profile."
        )

    if not github:

        suggestions.append(
            "Add your GitHub profile if you have one."
        )

    if not sections.get(
        "Contact Details",
        False
    ):

        suggestions.append(
            "Add a Contact Details section."
        )

    if not sections.get(
        "Certifications",
        False
    ):

        suggestions.append(
            "Add relevant certifications, workshops, or training."
        )

    if not sections.get(
        "Languages",
        False
    ):

        suggestions.append(
            "Add the languages you can communicate in."
        )

    if not sections.get(
        "Achievements",
        False
    ):

        suggestions.append(
            "Add important academic, professional, or other achievements."
        )

    return suggestions


# =========================================================
# MAIN ANALYZER
# =========================================================

def analyze_resume(
    text,
    selected_role=None
):

    # -----------------------------------------------------
    # Candidate information
    # -----------------------------------------------------

    name = find_name(text)

    email = find_email(text)

    phone = find_phone(text)

    linkedin = find_linkedin(text)

    github = find_github(text)


    # -----------------------------------------------------
    # Skills
    # -----------------------------------------------------

    skills = find_skills(text)


    # -----------------------------------------------------
    # Sections
    # -----------------------------------------------------

    sections = check_sections(text)


    # -----------------------------------------------------
    # Completeness
    # -----------------------------------------------------

    completeness_score = calculate_completeness(
        sections
    )


    # -----------------------------------------------------
    # Missing sections
    # -----------------------------------------------------

    missing_sections = [

        section

        for section, found
        in sections.items()

        if not found
    ]


    # -----------------------------------------------------
    # Rule-based job matching
    # -----------------------------------------------------

    job_match = {}

    if selected_role:

        job_match[selected_role] = calculate_job_match(
            skills,
            selected_role
        )


    # -----------------------------------------------------
    # ML CAREER PREDICTION
    # -----------------------------------------------------

    ml_prediction = predict_job_role_ml(
        text
    )


    # -----------------------------------------------------
    # Suggestions
    # -----------------------------------------------------

    suggestions = generate_suggestions(

        name,

        email,

        phone,

        linkedin,

        github,

        sections
    )


    # -----------------------------------------------------
    # FINAL RESULT
    # -----------------------------------------------------

    return {

        "name": name,

        "email": email,

        "phone": phone,

        "linkedin": linkedin,

        "github": github,

        "skills": skills,

        "sections": sections,

        "completeness_score":
            completeness_score,

        "missing_sections":
            missing_sections,

        "job_match":
            job_match,

        "ml_prediction":
            ml_prediction,

        "suggestions":
            suggestions
    }