
import re


# =========================================================
# COMMON TECHNICAL SKILLS
# =========================================================

SKILL_LIST = [

    # Programming
    "Python",
    "Java",
    "C",
    "C++",
    "PHP",
    "JavaScript",

    # Web
    "HTML",
    "CSS",
    "Django",
    "Flask",
    "React",
    "Node.js",

    # Database
    "SQL",
    "MySQL",
    "MongoDB",
    "PostgreSQL",

    # Data Science
    "Pandas",
    "NumPy",
    "TensorFlow",
    "Keras",
    "Scikit-learn",
    "Machine Learning",
    "Deep Learning",
    "Data Science",
    "Data Analysis",
    "Data Visualization",

    # Tools
    "Git",
    "GitHub",
    "Docker",
    "AWS",

    # Concepts
    "OOP",
    "Statistics",
    "NLP",
    "Computer Vision"
]


# =========================================================
# NORMALIZE TEXT
# =========================================================

def normalize_text(text):

    if not text:
        return ""

    text = text.lower()

    # Replace multiple spaces
    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


# =========================================================
# EXTRACT SKILLS FROM TEXT
# =========================================================

def extract_skills_from_text(text):

    normalized_text = normalize_text(
        text
    )

    found_skills = []

    for skill in SKILL_LIST:

        skill_lower = skill.lower()

        # Escape special regex characters
        pattern = (
            r"(?<!\w)"
            + re.escape(skill_lower)
            + r"(?!\w)"
        )

        if re.search(
            pattern,
            normalized_text
        ):

            found_skills.append(
                skill
            )

    return found_skills


# =========================================================
# COMPARE RESUME WITH JOB DESCRIPTION
# =========================================================

def compare_resume_with_job(
    resume_text,
    job_description
):

    resume_skills = extract_skills_from_text(
        resume_text
    )

    job_skills = extract_skills_from_text(
        job_description
    )

    resume_skill_set = {
        skill.lower()
        for skill in resume_skills
    }

    matched_skills = []

    missing_skills = []

    for skill in job_skills:

        if skill.lower() in resume_skill_set:

            matched_skills.append(
                skill
            )

        else:

            missing_skills.append(
                skill
            )


    # =====================================================
    # MATCH SCORE
    # =====================================================

    if job_skills:

        match_score = (
            len(matched_skills)
            / len(job_skills)
        ) * 100

    else:

        match_score = 0


    # =====================================================
    # PRIORITY SKILLS
    # =====================================================

    priority_skills = (
        missing_skills[:5]
    )


    return {

        "job_skills": job_skills,

        "resume_skills": resume_skills,

        "matched_skills": matched_skills,

        "missing_skills": missing_skills,

        "match_score": round(
            match_score,
            2
        ),

        "priority_skills": priority_skills
    }


# =========================================================
# DISPLAY JOB MATCH RESULT
# =========================================================

def display_job_match(
    result
):

    print("\n")

    print("=" * 60)

    print(
        "             JOB DESCRIPTION ANALYSIS"
    )

    print("=" * 60)


    # =====================================================
    # MATCH SCORE
    # =====================================================

    print(
        "\n📊 JOB DESCRIPTION MATCH"
    )

    print(
        "-----------------------------------"
    )

    print(
        f"Match Score: "
        f"{result['match_score']}%"
    )


    # =====================================================
    # JOB SKILLS
    # =====================================================

    print(
        "\n🎯 SKILLS REQUIRED BY JOB"
    )

    print(
        "-----------------------------------"
    )

    if result["job_skills"]:

        for skill in result["job_skills"]:

            print(
                f"• {skill}"
            )

    else:

        print(
            "No recognized technical skills found."
        )


    # =====================================================
    # MATCHED SKILLS
    # =====================================================

    print(
        "\n✅ SKILLS FOUND IN RESUME"
    )

    print(
        "-----------------------------------"
    )

    if result["matched_skills"]:

        for skill in result["matched_skills"]:

            print(
                f"• {skill}"
            )

    else:

        print(
            "No matching skills found."
        )


    # =====================================================
    # MISSING SKILLS
    # =====================================================

    print(
        "\n❌ SKILLS MISSING FROM RESUME"
    )

    print(
        "-----------------------------------"
    )

    if result["missing_skills"]:

        for skill in result["missing_skills"]:

            print(
                f"• {skill}"
            )

    else:

        print(
            "No important skills are missing."
        )


    # =====================================================
    # PRIORITY SKILLS
    # =====================================================

    print(
        "\n⭐ PRIORITY SKILLS TO LEARN"
    )

    print(
        "-----------------------------------"
    )

    if result["priority_skills"]:

        for index, skill in enumerate(
            result["priority_skills"],
            start=1
        ):

            print(
                f"{index}. {skill}"
            )

    else:

        print(
            "No priority skills identified."
        )


    print("\n")

    print("=" * 60)

