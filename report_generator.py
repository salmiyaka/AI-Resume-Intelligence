from datetime import datetime


def generate_report(result, output_file):
    """
    Generate a detailed text report from the resume analysis.
    """

    with open(output_file, "w", encoding="utf-8") as file:

        # -----------------------------------------
        # Report Header
        # -----------------------------------------

        file.write("=" * 60 + "\n")
        file.write("              RESUME ANALYSIS REPORT\n")
        file.write("=" * 60 + "\n\n")

        file.write(
            "Report Generated: "
            + datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            + "\n\n"
        )

        # -----------------------------------------
        # Completeness Score
        # -----------------------------------------

        file.write("RESUME COMPLETENESS\n")
        file.write("-" * 35 + "\n")

        file.write(
            f"Completeness Score: "
            f"{result['completeness_score']}%\n\n"
        )

        # -----------------------------------------
        # Contact Information
        # -----------------------------------------

        file.write("CONTACT INFORMATION\n")
        file.write("-" * 35 + "\n")

        if result["email"]:
            file.write(f"Email: {result['email']}\n")
        else:
            file.write("Email: Not found\n")

        if result["phone"]:
            file.write(f"Phone: {result['phone']}\n")
        else:
            file.write("Phone: Not found\n")

        file.write("\n")

        # -----------------------------------------
        # Resume Sections
        # -----------------------------------------

        file.write("RESUME SECTIONS\n")
        file.write("-" * 35 + "\n")

        for section, found in result["sections"].items():

            if found:
                status = "Found"
            else:
                status = "Missing"

            file.write(
                f"{section}: {status}\n"
            )

        file.write("\n")

        # -----------------------------------------
        # Skills
        # -----------------------------------------

        file.write("TECHNICAL SKILLS FOUND\n")
        file.write("-" * 35 + "\n")

        if result["skills"]:

            for skill in result["skills"]:
                file.write(f"- {skill}\n")

        else:

            file.write("No technical skills detected.\n")

        file.write("\n")

        # -----------------------------------------
        # Missing Sections
        # -----------------------------------------

        file.write("MISSING SECTIONS\n")
        file.write("-" * 35 + "\n")

        if result["missing_sections"]:

            for section in result["missing_sections"]:
                file.write(f"- {section}\n")

        else:

            file.write("No important sections are missing.\n")

        file.write("\n")

        # -----------------------------------------
        # Suggestions
        # -----------------------------------------

        file.write("SUGGESTIONS FOR IMPROVEMENT\n")
        file.write("-" * 35 + "\n")

        if result["suggestions"]:

            for suggestion in result["suggestions"]:
                file.write(f"- {suggestion}\n")

        else:

            file.write(
                "Your resume contains all the required sections.\n"
            )

        file.write("\n")

        # -----------------------------------------
        # Footer
        # -----------------------------------------

        file.write("=" * 60 + "\n")
        file.write("                    END OF REPORT\n")
        file.write("=" * 60 + "\n")