import os
import tempfile
from pathlib import Path

import streamlit as st

from resume_parser import read_uploaded_resume
from analyzer import analyze_resume
from job_matcher import compare_resume_with_job
from job_roles import JOB_ROLES


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="AI Resume Intelligence",
    page_icon="🤖",
    layout="wide"
)


# =========================================================
# HEADER
# =========================================================

st.title("🤖 AI Resume Intelligence")

st.write(
    "Resume Analysis • Job Matching • "
    "ML Career Prediction • Skill Gap Analysis"
)

st.divider()


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.header("⚙️ Resume Settings")

    selected_role = st.selectbox(
        "🎯 Target Job Role",
        JOB_ROLES
    )

    st.divider()

    st.info(
        "Upload a PDF or TXT resume to analyze "
        "its completeness, skills, job suitability "
        "and ML career prediction."
    )


# =========================================================
# RESUME UPLOAD
# =========================================================

st.header("📄 Upload Resume")

uploaded_file = st.file_uploader(
    "Choose your resume",
    type=["pdf", "txt"]
)


# =========================================================
# ANALYZE RESUME
# =========================================================

if uploaded_file is not None:

    st.success(
        f"Uploaded: {uploaded_file.name}"
    )

    if st.button(
        "🔍 ANALYZE RESUME",
        type="primary",
        use_container_width=True
    ):

        temp_path = None

        try:

            # -------------------------------------------------
            # CREATE TEMPORARY FILE
            # -------------------------------------------------

            file_extension = Path(
                uploaded_file.name
            ).suffix.lower()

            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=file_extension
            ) as temp_file:

                temp_file.write(
                    uploaded_file.getbuffer()
                )

                temp_path = temp_file.name


            # -------------------------------------------------
            # READ RESUME
            # -------------------------------------------------

            with st.spinner(
                "📖 Reading resume..."
            ):

                resume_text = read_uploaded_resume(
                    temp_path
                )


            if not resume_text.strip():

                st.error(
                    "❌ No readable text was found "
                    "in the uploaded resume."
                )

                st.stop()


            # -------------------------------------------------
            # ANALYZE RESUME
            # -------------------------------------------------

            with st.spinner(
                "🔍 Analyzing resume..."
            ):

                result = analyze_resume(
                    resume_text,
                    selected_role
                )


            # -------------------------------------------------
            # SAVE TO SESSION
            # -------------------------------------------------

            st.session_state["result"] = result

            st.session_state[
                "resume_text"
            ] = resume_text

            st.session_state[
                "selected_role"
            ] = selected_role

            st.session_state[
                "uploaded_name"
            ] = uploaded_file.name


            # Remove old JD result
            st.session_state.pop(
                "jd_result",
                None
            )


            st.success(
                "✅ Resume analysis completed successfully!"
            )


        except Exception as error:

            st.error(
                f"❌ Error while analyzing resume:\n\n{error}"
            )


        finally:

            if (
                temp_path
                and os.path.exists(temp_path)
            ):

                try:

                    os.remove(
                        temp_path
                    )

                except OSError:

                    pass


# =========================================================
# DISPLAY ANALYSIS
# =========================================================

if "result" in st.session_state:

    result = st.session_state["result"]

    selected_role = st.session_state[
        "selected_role"
    ]


    # =====================================================
    # CANDIDATE INFORMATION
    # =====================================================

    st.divider()

    st.header("👤 Candidate Information")

    candidate_col1, candidate_col2 = st.columns(2)


    with candidate_col1:

        st.write(
            f"**Name:** "
            f"{result.get('name') or 'Not detected'}"
        )

        st.write(
            f"**Email:** "
            f"{result.get('email') or 'Not found'}"
        )

        st.write(
            f"**Phone:** "
            f"{result.get('phone') or 'Not found'}"
        )


    with candidate_col2:

        st.write(
            f"**LinkedIn:** "
            f"{result.get('linkedin') or 'Not found'}"
        )

        st.write(
            f"**GitHub:** "
            f"{result.get('github') or 'Not found'}"
        )

        st.write(
            f"**Target Role:** "
            f"{selected_role}"
        )


    # =====================================================
    # EXTRACT MAIN DATA
    # =====================================================

    completeness = result.get(
        "completeness_score",
        0
    )


    job_match_all = result.get(
        "job_match",
        {}
    )


    role_data = job_match_all.get(
        selected_role,
        {}
    )


    job_match_score = role_data.get(
        "percentage",
        0
    )


    matched_skills = role_data.get(
        "matched",
        []
    )


    missing_skills = role_data.get(
        "missing",
        []
    )


    ml_prediction = result.get(
        "ml_prediction",
        {}
    )


    predicted_role = ml_prediction.get(
        "predicted_role"
    )


    ml_confidence = ml_prediction.get(
        "confidence",
        0
    )


    # =====================================================
    # RESUME OVERVIEW
    # =====================================================

    st.divider()

    st.header("📊 Resume Overview")


    overview1, overview2, overview3 = st.columns(3)


    # -----------------------------------------------------
    # COMPLETENESS
    # -----------------------------------------------------

    with overview1:

        st.metric(
            "📄 Resume Completeness",
            f"{completeness}%"
        )

        try:

            completeness_value = float(
                completeness
            )

        except:

            completeness_value = 0


        st.progress(
            max(
                0,
                min(
                    completeness_value / 100,
                    1
                )
            )
        )


    # -----------------------------------------------------
    # JOB MATCH
    # -----------------------------------------------------

    with overview2:

        st.metric(
            "🎯 Job Match",
            f"{job_match_score}%"
        )

        try:

            job_match_value = float(
                job_match_score
            )

        except:

            job_match_value = 0


        st.progress(
            max(
                0,
                min(
                    job_match_value / 100,
                    1
                )
            )
        )


    # -----------------------------------------------------
    # ML PREDICTION
    # -----------------------------------------------------

    with overview3:

        st.metric(
            "🤖 ML Predicted Role",
            predicted_role or "Unavailable"
        )

        st.write(
            f"Confidence: **{ml_confidence}%**"
        )


    # =====================================================
    # JOB ROLE MATCH
    # =====================================================

    st.divider()

    st.header("🎯 Job Role Match")

    st.write(
        f"**Target Role:** {selected_role}"
    )

    st.write(
        f"**Job Match Score:** "
        f"{job_match_score}%"
    )


    try:

        job_match_value = float(
            job_match_score
        )

    except:

        job_match_value = 0


    st.progress(
        max(
            0,
            min(
                job_match_value / 100,
                1
            )
        )
    )


    match_col, missing_col = st.columns(2)


    # -----------------------------------------------------
    # MATCHED SKILLS
    # -----------------------------------------------------

    with match_col:

        st.subheader(
            "✅ Matched Skills"
        )

        if matched_skills:

            for skill in matched_skills:

                st.success(
                    str(skill)
                )

        else:

            st.write(
                "No matching skills found."
            )


    # -----------------------------------------------------
    # MISSING SKILLS
    # -----------------------------------------------------

    with missing_col:

        st.subheader(
            "❌ Missing Recommended Skills"
        )

        if missing_skills:

            for skill in missing_skills:

                st.warning(
                    str(skill)
                )

        else:

            st.write(
                "No recommended skills are missing."
            )


    # =====================================================
    # ML CAREER PREDICTION
    # =====================================================

    st.divider()

    st.header("🤖 ML Career Prediction")


    if ml_prediction.get(
        "available",
        False
    ):

        st.success(
            f"Predicted Role: **{predicted_role}**"
        )

        st.write(
            f"Confidence: **{ml_confidence}%**"
        )


        probabilities = ml_prediction.get(
            "probabilities",
            []
        )


        if probabilities:

            st.subheader(
                "📊 Role Probabilities"
            )


            # Convert list of dictionaries
            # into a dictionary for Streamlit

            probability_data = {}


            for item in probabilities:

                role = item.get(
                    "role"
                )

                score = item.get(
                    "score",
                    0
                )

                if role:

                    probability_data[
                        role
                    ] = score


            if probability_data:

                st.bar_chart(
                    probability_data
                )


                # Also show exact values

                for role, score in probability_data.items():

                    st.write(
                        f"**{role}:** {score}%"
                    )

    else:

        st.warning(
            "ML career prediction is not available. "
            "Make sure job_role_model.pkl exists "
            "inside the models folder."
        )


    # =====================================================
    # TECHNICAL SKILLS
    # =====================================================

    st.divider()

    st.header("💻 Technical Skills Found")


    skills = result.get(
        "skills",
        []
    )


    if skills:

        skill_columns = st.columns(4)


        for index, skill in enumerate(
            skills
        ):

            with skill_columns[
                index % 4
            ]:

                st.info(
                    str(skill)
                )

    else:

        st.write(
            "No technical skills detected."
        )


    # =====================================================
    # RESUME SECTIONS
    # =====================================================

    st.divider()

    st.header("📋 Resume Sections")


    sections = result.get(
        "sections",
        {}
    )


    if sections:

        section_columns = st.columns(3)


        for index, item in enumerate(
            sections.items()
        ):

            section_name, found = item


            with section_columns[
                index % 3
            ]:

                if found:

                    st.success(
                        f"✅ {section_name}"
                    )

                else:

                    st.error(
                        f"❌ {section_name}"
                    )

    else:

        st.write(
            "No section information available."
        )


    # =====================================================
    # MISSING SECTIONS
    # =====================================================

    missing_sections = result.get(
        "missing_sections",
        []
    )


    if missing_sections:

        st.subheader(
            "⚠️ Missing Resume Sections"
        )


        for section in missing_sections:

            st.warning(
                str(section)
            )


    # =====================================================
    # SUGGESTIONS
    # =====================================================

    st.divider()

    st.header("💡 Resume Suggestions")


    suggestions = result.get(
        "suggestions",
        []
    )


    if suggestions:

        for suggestion in suggestions:

            st.info(
                str(suggestion)
            )

    else:

        st.success(
            "No suggestions. Your resume looks good!"
        )


    # =====================================================
    # JOB DESCRIPTION ANALYZER
    # =====================================================

    st.divider()

    st.header(
        "🧩 Job Description Analyzer"
    )


    st.write(
        "Paste a company's Job Description "
        "to compare it with your uploaded resume."
    )


    job_description = st.text_area(
        "Paste Job Description",
        height=250,
        placeholder=(
            "Example:\n\n"
            "We are looking for a Data Scientist "
            "with experience in Python, Pandas, "
            "NumPy, Machine Learning and SQL..."
        )
    )


    if st.button(
        "🔎 ANALYZE JOB DESCRIPTION",
        use_container_width=True
    ):

        if not job_description.strip():

            st.warning(
                "Please paste a Job Description first."
            )

        else:

            try:

                with st.spinner(
                    "🔍 Analyzing Job Description..."
                ):

                    jd_result = compare_resume_with_job(
                        st.session_state[
                            "resume_text"
                        ],
                        job_description
                    )


                st.session_state[
                    "jd_result"
                ] = jd_result


                st.success(
                    "✅ Job Description analyzed successfully!"
                )


            except Exception as error:

                st.error(
                    f"❌ Job Description analysis failed:\n\n"
                    f"{error}"
                )


    # =====================================================
    # DISPLAY JOB DESCRIPTION RESULT
    # =====================================================

    if "jd_result" in st.session_state:

        jd_result = st.session_state[
            "jd_result"
        ]


        st.subheader(
            "📊 Job Description Match"
        )


        jd_score = jd_result.get(
            "match_score",
            0
        )


        st.metric(
            "JD Match Score",
            f"{jd_score}%"
        )


        try:

            jd_score_value = float(
                jd_score
            )

        except:

            jd_score_value = 0


        st.progress(
            max(
                0,
                min(
                    jd_score_value / 100,
                    1
                )
            )
        )


        # -------------------------------------------------
        # REQUIRED SKILLS
        # -------------------------------------------------

        jd_col1, jd_col2 = st.columns(2)


        with jd_col1:

            st.subheader(
                "🎯 Skills Required by Job"
            )


            job_skills = jd_result.get(
                "job_skills",
                []
            )


            if job_skills:

                for skill in job_skills:

                    st.write(
                        f"• {skill}"
                    )

            else:

                st.write(
                    "No recognized technical skills found."
                )


        # -------------------------------------------------
        # MATCHED JD SKILLS
        # -------------------------------------------------

        with jd_col2:

            st.subheader(
                "✅ Skills Found in Resume"
            )


            jd_matched = jd_result.get(
                "matched_skills",
                []
            )


            if jd_matched:

                for skill in jd_matched:

                    st.success(
                        str(skill)
                    )

            else:

                st.write(
                    "No matching skills found."
                )


        # -------------------------------------------------
        # MISSING JD SKILLS
        # -------------------------------------------------

        st.subheader(
            "❌ Skills Missing From Resume"
        )


        jd_missing = jd_result.get(
            "missing_skills",
            []
        )


        if jd_missing:

            for skill in jd_missing:

                st.warning(
                    str(skill)
                )

        else:

            st.success(
                "No important skills are missing."
            )


        # -------------------------------------------------
        # PRIORITY SKILLS
        # -------------------------------------------------

        st.subheader(
            "⭐ Priority Skills to Learn"
        )


        priority_skills = jd_result.get(
            "priority_skills",
            []
        )


        if priority_skills:

            for index, skill in enumerate(
                priority_skills,
                start=1
            ):

                st.write(
                    f"**{index}.** {skill}"
                )

        else:

            st.success(
                "No priority skills identified."
            )


    # =====================================================
    # FINAL REPORT
    # =====================================================

    st.divider()

    st.header(
        "📄 Final Report"
    )


    if st.button(
        "📝 Generate Final Report",
        use_container_width=True
    ):


        # -------------------------------------------------
        # MATCHED SKILLS TEXT
        # -------------------------------------------------

        matched_text = (
            "\n".join(
                f"• {skill}"
                for skill in matched_skills
            )
            if matched_skills
            else
            "No matching skills found."
        )


        # -------------------------------------------------
        # MISSING SKILLS TEXT
        # -------------------------------------------------

        missing_text = (
            "\n".join(
                f"• {skill}"
                for skill in missing_skills
            )
            if missing_skills
            else
            "No recommended skills are missing."
        )


        # -------------------------------------------------
        # TECHNICAL SKILLS TEXT
        # -------------------------------------------------

        skills_text = (
            "\n".join(
                f"• {skill}"
                for skill in skills
            )
            if skills
            else
            "No technical skills detected."
        )


        # -------------------------------------------------
        # MISSING SECTIONS TEXT
        # -------------------------------------------------

        missing_sections_text = (
            "\n".join(
                f"• {section}"
                for section in missing_sections
            )
            if missing_sections
            else
            "None"
        )


        # -------------------------------------------------
        # SUGGESTIONS TEXT
        # -------------------------------------------------

        suggestions_text = (
            "\n".join(
                f"• {suggestion}"
                for suggestion in suggestions
            )
            if suggestions
            else
            "No suggestions."
        )


        # -------------------------------------------------
        # CREATE REPORT
        # -------------------------------------------------

        report = f"""
============================================================
                 AI RESUME ANALYSIS REPORT
============================================================

CANDIDATE INFORMATION
------------------------------------------------------------
Name: {result.get("name") or "Not detected"}
Email: {result.get("email") or "Not found"}
Phone: {result.get("phone") or "Not found"}
LinkedIn: {result.get("linkedin") or "Not found"}
GitHub: {result.get("github") or "Not found"}

============================================================
RESUME OVERVIEW
============================================================

Resume Completeness: {completeness}%

Target Job Role: {selected_role}

Job Match Score: {job_match_score}%

ML Predicted Role: {predicted_role or "Unavailable"}

ML Confidence: {ml_confidence}%

============================================================
MATCHED SKILLS
============================================================

{matched_text}

============================================================
MISSING RECOMMENDED SKILLS
============================================================

{missing_text}

============================================================
TECHNICAL SKILLS
============================================================

{skills_text}

============================================================
MISSING RESUME SECTIONS
============================================================

{missing_sections_text}

============================================================
RESUME SUGGESTIONS
============================================================

{suggestions_text}

============================================================
ML ROLE PROBABILITIES
============================================================
"""


        # -------------------------------------------------
        # ADD ML PROBABILITIES
        # -------------------------------------------------

        probabilities = ml_prediction.get(
            "probabilities",
            []
        )


        if probabilities:

            for item in probabilities:

                role = item.get(
                    "role"
                )

                score = item.get(
                    "score",
                    0
                )

                report += (
                    f"{role}: {score}%\n"
                )

        else:

            report += (
                "ML probabilities unavailable.\n"
            )


        # -------------------------------------------------
        # ADD JD REPORT IF AVAILABLE
        # -------------------------------------------------

        if "jd_result" in st.session_state:

            jd_result = st.session_state[
                "jd_result"
            ]


            report += f"""

============================================================
JOB DESCRIPTION ANALYSIS
============================================================

JD Match Score: {jd_result.get("match_score", 0)}%

JOB REQUIRED SKILLS
------------------------------------------------------------
"""


            report += "\n".join(
                f"• {skill}"
                for skill in jd_result.get(
                    "job_skills",
                    []
                )
            ) or "No recognized skills."


            report += """

MATCHED JD SKILLS
------------------------------------------------------------
"""


            report += "\n".join(
                f"• {skill}"
                for skill in jd_result.get(
                    "matched_skills",
                    []
                )
            ) or "No matching skills."


            report += """

MISSING JD SKILLS
------------------------------------------------------------
"""


            report += "\n".join(
                f"• {skill}"
                for skill in jd_result.get(
                    "missing_skills",
                    []
                )
            ) or "No missing skills."


            report += """

PRIORITY SKILLS TO LEARN
------------------------------------------------------------
"""


            report += "\n".join(
                f"{index}. {skill}"
                for index, skill in enumerate(
                    jd_result.get(
                        "priority_skills",
                        []
                    ),
                    start=1
                )
            ) or "No priority skills."


        report += """

============================================================
                    END OF REPORT
============================================================
"""


        st.success(
            "✅ Final report generated!"
        )


        st.download_button(
            label="📥 Download Resume Analysis Report",
            data=report,
            file_name="resume_analysis_report.txt",
            mime="text/plain",
            use_container_width=True
        )


# =========================================================
# EMPTY PAGE
# =========================================================

else:

    st.info(
        "👆 Upload a PDF or TXT resume above "
        "to start the analysis."
    )