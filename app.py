
import os
import tempfile
import streamlit as st

from resume_parser import read_uploaded_resume
from analyzer import analyze_resume
from job_matcher import compare_resume_with_job
from job_roles import JOB_ROLES


# =====================================================
# 1. PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="AI Resume Intelligence",
    page_icon="📄",
    layout="wide"
)


# =====================================================
# 2. HELPER FUNCTIONS
# =====================================================

def safe_percentage(value):

    try:
        return max(0.0, min(float(value), 100.0))
    except (TypeError, ValueError):
        return 0.0


def display_list(items, empty_message="No information detected."):

    if isinstance(items, (list, tuple, set)):

        if items:
            for item in items:
                st.write(f"• {item}")
        else:
            st.info(empty_message)

    elif items:
        st.write(items)

    else:
        st.info(empty_message)


def get_value(data, possible_keys, default=None):

    if not isinstance(data, dict):
        return default

    for key in possible_keys:

        if key in data and data[key] is not None:
            return data[key]

    return default


# =====================================================
# 3. MACHINE LEARNING PREDICTION
# =====================================================

def display_ml_prediction(ml_result, selected_role):

    st.header("Machine Learning Prediction")

    if not isinstance(ml_result, dict):

        st.info("Machine Learning prediction is unavailable.")
        return

    if not ml_result.get("available", False):

        st.warning(
            "The trained Machine Learning model is unavailable. "
            "Please check your model file."
        )
        return

    probabilities = ml_result.get("probabilities", [])

    if not isinstance(probabilities, list):

        st.warning("Prediction data has an invalid format.")
        return

    selected_score = None

    for item in probabilities:

        if not isinstance(item, dict):
            continue

        role = item.get("role", "")

        if str(role).strip().lower() == selected_role.strip().lower():

            selected_score = item.get("score")
            break

    if selected_score is None:

        st.warning(
            f"No prediction score found for {selected_role}."
        )
        return

    selected_score = safe_percentage(selected_score)

    st.subheader(f"Selected Job Role: {selected_role}")

    st.metric(
        label="Prediction Probability",
        value=f"{selected_score:.2f}%"
    )

    st.progress(selected_score / 100)

    st.caption(
        "This is the model's estimated probability for the selected "
        "role. It is not a measure of actual job suitability."
    )


# =====================================================
# 4. JOB ROLE MATCHING
# =====================================================

def display_role_match(job_match, selected_role):

    st.header("Job Role Matching")

    if not isinstance(job_match, dict):

        st.info("Job-role matching information is unavailable.")
        return

    role_data = job_match.get(selected_role, {})

    if not isinstance(role_data, dict) or not role_data:

        st.info(
            f"No matching information available for {selected_role}."
        )
        return

    score = safe_percentage(
        get_value(
            role_data,
            ["percentage", "match_score", "score"],
            0
        )
    )

    matched = get_value(
        role_data,
        ["matched", "matched_skills"],
        []
    )

    missing = get_value(
        role_data,
        ["missing", "missing_skills"],
        []
    )

    st.metric("Role Match Score", f"{score:.2f}%")

    st.progress(score / 100)

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("Matched Skills")

        display_list(
            matched,
            "No matched skills detected."
        )

    with col2:

        st.subheader("Missing Skills")

        display_list(
            missing,
            "No missing skills detected."
        )


# =====================================================
# 5. REPORT GENERATION
# =====================================================

def create_report(result, selected_role, resume_name):

    missing_sections = result.get("missing_sections", [])
    skills = result.get("skills", [])
    suggestions = result.get("suggestions", [])

    job_match = result.get("job_match", {})

    role_data = (
        job_match.get(selected_role, {})
        if isinstance(job_match, dict)
        else {}
    )

    ml_result = result.get("ml_prediction", {})

    ml_score = "Unavailable"

    if isinstance(ml_result, dict):

        for item in ml_result.get("probabilities", []):

            if not isinstance(item, dict):
                continue

            if str(item.get("role", "")).strip().lower() == selected_role.lower():

                ml_score = item.get("score", "Unavailable")
                break

    report = f"""
====================================================
             AI RESUME INTELLIGENCE REPORT
====================================================

Resume Name: {resume_name}

CANDIDATE INFORMATION
---------------------
Name: {result.get('name') or 'Not detected'}
Email: {result.get('email') or 'Not detected'}
Phone: {result.get('phone') or 'Not detected'}
LinkedIn: {result.get('linkedin') or 'Not detected'}
GitHub: {result.get('github') or 'Not detected'}

RESUME COMPLETENESS
-------------------
Score: {result.get('completeness_score', 0)}%

Missing Sections:
{', '.join(map(str, missing_sections)) if missing_sections else 'None'}

TECHNICAL SKILLS
----------------
{', '.join(map(str, skills)) if skills else 'None detected'}

SELECTED JOB ROLE
-----------------
{selected_role}

JOB ROLE MATCH
--------------
{role_data}

MACHINE LEARNING PREDICTION
---------------------------
Selected Role: {selected_role}
Prediction Probability: {ml_score}

IMPROVEMENT SUGGESTIONS
----------------------
{chr(10).join(map(str, suggestions)) if suggestions else 'None'}

====================================================
                  END OF REPORT
====================================================
"""

    return report


# =====================================================
# 6. MAIN APPLICATION
# =====================================================

st.title("📄 AI Resume Intelligence")

st.write(
    "Analyze your resume, identify skill gaps, "
    "and discover suitable career opportunities."
)

st.divider()


# =====================================================
# 7. SIDEBAR
# =====================================================

st.sidebar.title("Resume Analyzer")

st.sidebar.write(
    "Upload your resume and select your target job role."
)

selected_role = st.sidebar.selectbox(
    "Select Target Job Role",
    options=list(JOB_ROLES.keys())
)

st.sidebar.divider()

st.sidebar.info("Supported formats: PDF and TXT")


# =====================================================
# 8. RESUME UPLOAD
# =====================================================

st.header("1. Upload Your Resume")

uploaded_file = st.file_uploader(
    "Choose your resume",
    type=["pdf", "txt"]
)


if uploaded_file is not None:

    st.success(f"Uploaded: {uploaded_file.name}")

    if st.button("Analyze Resume", type="primary"):

        temporary_path = None

        try:

            extension = os.path.splitext(
                uploaded_file.name
            )[1].lower()

            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=extension
            ) as temporary_file:

                temporary_file.write(
                    uploaded_file.getvalue()
                )

                temporary_path = temporary_file.name

            with st.spinner("Analyzing your resume..."):

                resume_text = read_uploaded_resume(
                    temporary_path
                )

                if not resume_text.strip():

                    st.error(
                        "No readable text was found in this resume."
                    )

                    st.stop()

                analysis_result = analyze_resume(
                    resume_text,
                    selected_role=selected_role
                )

            if not isinstance(analysis_result, dict):

                raise ValueError(
                    "The analyzer returned an unexpected result."
                )

            st.session_state["resume_text"] = resume_text

            st.session_state["analysis_result"] = analysis_result

            st.session_state["resume_name"] = uploaded_file.name

            st.session_state["selected_role"] = selected_role

            st.session_state.pop("jd_result", None)

            st.success("Resume analysis completed successfully!")

        except Exception as error:

            st.error(f"Resume analysis failed: {error}")

        finally:

            if temporary_path and os.path.exists(temporary_path):

                os.remove(temporary_path)


# =====================================================
# 9. DISPLAY ANALYSIS RESULTS
# =====================================================

if "analysis_result" in st.session_state:

    result = st.session_state["analysis_result"]

    resume_text = st.session_state["resume_text"]

    current_role = st.session_state["selected_role"]

    st.divider()


    # -------------------------------------------------
    # CANDIDATE INFORMATION
    # -------------------------------------------------

    st.header("2. Candidate Information")

    col1, col2 = st.columns(2)

    with col1:

        st.write(
            "**Name:**",
            result.get("name") or "Not detected"
        )

        st.write(
            "**Email:**",
            result.get("email") or "Not detected"
        )

        st.write(
            "**Phone:**",
            result.get("phone") or "Not detected"
        )

    with col2:

        st.write(
            "**LinkedIn:**",
            result.get("linkedin") or "Not detected"
        )

        st.write(
            "**GitHub:**",
            result.get("github") or "Not detected"
        )

        st.write(
            "**Resume:**",
            st.session_state["resume_name"]
        )

    st.divider()


    # -------------------------------------------------
    # RESUME COMPLETENESS
    # -------------------------------------------------

    st.header("3. Resume Completeness")

    completeness = safe_percentage(
        result.get("completeness_score", 0)
    )

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Completeness Score",
            f"{completeness:.2f}%"
        )

        st.progress(completeness / 100)

    with col2:

        st.subheader("Missing Sections")

        display_list(
            result.get("missing_sections", []),
            "No missing sections detected."
        )

    st.divider()


    # -------------------------------------------------
    # TECHNICAL SKILLS
    # -------------------------------------------------

    st.header("4. Technical Skills")

    display_list(
        result.get("skills", []),
        "No technical skills detected."
    )

    st.divider()


    # -------------------------------------------------
    # JOB ROLE MATCHING
    # -------------------------------------------------

    st.header("5. Job Role Matching")

    display_role_match(
        result.get("job_match", {}),
        current_role
    )

    st.divider()


    # -------------------------------------------------
    # RESUME SECTIONS
    # -------------------------------------------------

    st.header("6. Resume Sections")

    sections = result.get("sections", {})

    if isinstance(sections, dict):

        for section, status in sections.items():

            if status:
                st.write(f"✅ {section}")
            else:
                st.write(f"❌ {section}")

    elif isinstance(sections, list):

        display_list(sections)

    else:

        st.info("Section information is unavailable.")

    st.divider()


    # -------------------------------------------------
    # MACHINE LEARNING PREDICTION
    # -------------------------------------------------

    ml_result = result.get("ml_prediction")

    if ml_result:

        display_ml_prediction(
            ml_result,
            current_role
        )

    st.divider()


    # -------------------------------------------------
    # IMPROVEMENT SUGGESTIONS
    # -------------------------------------------------

    st.header("7. Resume Improvement Suggestions")

    display_list(
        result.get("suggestions", []),
        "No improvement suggestions available."
    )

    st.divider()


    # -------------------------------------------------
    # JOB DESCRIPTION ANALYZER
    # -------------------------------------------------

    st.header("8. Job Description Analyzer")

    st.write(
        "Compare your resume with a job description "
        "to identify matching and missing skills."
    )

    job_description = st.text_area(
        "Paste Job Description",
        height=200,
        placeholder="Paste the job description here..."
    )

    if st.button("Compare With Job Description"):

        if not job_description.strip():

            st.warning("Please enter a job description.")

        else:

            try:

                with st.spinner(
                    "Comparing resume with job description..."
                ):

                    jd_result = compare_resume_with_job(
                        resume_text,
                        job_description
                    )

                if not isinstance(jd_result, dict):

                    raise ValueError(
                        "Unexpected job matcher result."
                    )

                st.session_state["jd_result"] = jd_result

            except Exception as error:

                st.error(
                    f"Job description comparison failed: {error}"
                )


    # Display comparison result

    if "jd_result" in st.session_state:

        jd_result = st.session_state["jd_result"]

        st.subheader("Job Description Match Report")

        jd_score = safe_percentage(
            jd_result.get("match_score", 0)
        )

        st.metric(
            "Job Description Match Score",
            f"{jd_score:.2f}%"
        )

        st.progress(jd_score / 100)

        col1, col2 = st.columns(2)

        with col1:

            st.subheader("Matched Skills")

            display_list(
                jd_result.get("matched_skills", []),
                "No matched skills found."
            )

        with col2:

            st.subheader("Missing Skills")

            display_list(
                jd_result.get("missing_skills", []),
                "No missing skills found."
            )

        st.subheader("Priority Skills to Learn")

        display_list(
            jd_result.get("priority_skills", []),
            "No priority skills identified."
        )

    st.divider()


    # -------------------------------------------------
    # DOWNLOAD REPORT
    # -------------------------------------------------

    st.header("9. Download Analysis Report")

    report = create_report(
        result,
        current_role,
        st.session_state["resume_name"]
    )

    st.download_button(
        label="📥 Download Resume Analysis Report",
        data=report,
        file_name="resume_analysis_report.txt",
        mime="text/plain"
    )


else:

    st.info(
        "Upload a PDF or TXT resume and click "
        "'Analyze Resume' to view your analysis."
    )


# =====================================================
# 10. FOOTER
# =====================================================

st.divider()

st.caption(
    "AI Resume Intelligence | Resume Analysis and Career Matching"
)
