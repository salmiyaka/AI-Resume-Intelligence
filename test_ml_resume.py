import os
import joblib

from resume_parser import read_uploaded_resume


# =========================================================
# MODEL PATH
# =========================================================

MODEL_PATH = os.path.join(
    "models",
    "job_role_model.pkl"
)


# =========================================================
# LOAD ML MODEL
# =========================================================

def load_ml_model():

    if not os.path.exists(MODEL_PATH):
        print("\n❌ ML model not found!")
        print("Please run train_model.py first.")
        return None

    return joblib.load(MODEL_PATH)


# =========================================================
# PREDICT JOB ROLE
# =========================================================

def predict_resume_role(resume_text):

    model = load_ml_model()

    if model is None:
        return

    probabilities = model.predict_proba(
        [resume_text]
    )[0]

    roles = model.classes_

    results = []

    for role, probability in zip(
        roles,
        probabilities
    ):
        results.append(
            (
                role,
                probability * 100
            )
        )

    results.sort(
        key=lambda x: x[1],
        reverse=True
    )

    print("\n")
    print("=" * 60)
    print("              🤖 ML CAREER PREDICTION")
    print("=" * 60)

    print("\n📊 ROLE PROBABILITIES")
    print("-" * 40)

    for role, score in results:

        print(
            f"{role:<22} {score:.2f}%"
        )

    print("\n🏆 PREDICTED ROLE")
    print("-" * 40)

    print(
        f"{results[0][0]}"
    )

    print(
        f"Confidence: {results[0][1]:.2f}%"
    )

    print("\n" + "=" * 60)


# =========================================================
# MAIN
# =========================================================

def main():

    print("\n" + "=" * 60)
    print("          ML RESUME TEST")
    print("=" * 60)

    resume_path = input(
        "\nEnter the path of your resume: "
    ).strip()

    if not os.path.exists(resume_path):

        print("\n❌ File not found.")

        return

    print("\n📖 Reading resume...")

    try:

        resume_text = read_uploaded_resume(
            resume_path
        )

    except Exception as e:

        print("\n❌ Error reading resume:")
        print(e)

        return

    if not resume_text:

        print("\n❌ No text could be extracted from the resume.")

        return

    print("🔍 Sending resume to ML model...")

    predict_resume_role(
        resume_text
    )


if __name__ == "__main__":
    main()