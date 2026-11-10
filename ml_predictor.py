import os
import joblib


# =========================================================
# MODEL PATH
# =========================================================

MODEL_PATH = os.path.join(
    "models",
    "job_role_model.pkl"
)


# =========================================================
# LOAD MODEL
# =========================================================

def load_model():

    if not os.path.exists(MODEL_PATH):

        raise FileNotFoundError(
            "ML model not found. "
            "Please run train_model.py first."
        )

    return joblib.load(MODEL_PATH)


# =========================================================
# PREDICT JOB ROLE
# =========================================================

def predict_job_role(text):

    model = load_model()

    # Predict probabilities
    probabilities = model.predict_proba(
        [text]
    )[0]

    classes = model.classes_

    results = []

    for role, probability in zip(
        classes,
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
        key=lambda x: x["score"],
        reverse=True
    )

    predicted_role = results[0]["role"]

    confidence = results[0]["score"]

    return {
        "predicted_role": predicted_role,
        "confidence": confidence,
        "all_roles": results
    }


# =========================================================
# TEST
# =========================================================

if __name__ == "__main__":

    print("\n" + "=" * 60)
    print("             ML JOB ROLE PREDICTOR")
    print("=" * 60)

    sample_resume = """
    Python developer with experience in Python,
    Django, Flask, SQL, MySQL and backend development.
    Developed web applications and REST APIs.
    """

    result = predict_job_role(
        sample_resume
    )

    print("\n🤖 PREDICTED JOB ROLE")
    print("-----------------------------------")

    print(
        f"Role: {result['predicted_role']}"
    )

    print(
        f"Confidence: {result['confidence']}%"
    )

    print("\n📊 ROLE PROBABILITIES")
    print("-----------------------------------")

    for item in result["all_roles"]:

        print(
            f"{item['role']:<22} "
            f"{item['score']}%"
        )

    print("\n" + "=" * 60)