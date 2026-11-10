import os
import joblib
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score, classification_report


# =========================================================
# TRAINING DATASET
# =========================================================

data = [

    # =====================================================
    # PYTHON DEVELOPER
    # =====================================================

    ("Python Developer",
     "python django flask backend development api sql mysql git github"),

    ("Python Developer",
     "python programming django web application backend database"),

    ("Python Developer",
     "python developer flask django rest api mysql sql"),

    ("Python Developer",
     "python scripting automation backend programming django"),

    ("Python Developer",
     "python oop django flask sql database github"),

    ("Python Developer",
     "python backend development flask mysql sqlite api"),

    ("Python Developer",
     "python django rest api software development sql"),

    ("Python Developer",
     "python flask backend developer git github database"),

    ("Python Developer",
     "python programming django mysql api backend"),

    ("Python Developer",
     "python application development flask sql mysql oop"),

    ("Python Developer",
     "python django backend web application development"),

    ("Python Developer",
     "python developer programming flask django git github"),

    ("Python Developer",
     "python backend engineer django sql rest api"),

    ("Python Developer",
     "python software development django flask database"),

    ("Python Developer",
     "python coding django flask mysql github"),


    # =====================================================
    # DATA ANALYST
    # =====================================================

    ("Data Analyst",
     "data analysis excel sql mysql pandas numpy power bi"),

    ("Data Analyst",
     "data analyst python pandas excel statistics visualization"),

    ("Data Analyst",
     "sql excel power bi tableau data analysis reporting"),

    ("Data Analyst",
     "data cleaning pandas numpy excel sql visualization"),

    ("Data Analyst",
     "business analytics sql python excel power bi"),

    ("Data Analyst",
     "data visualization tableau power bi excel sql"),

    ("Data Analyst",
     "analytical skills python pandas sql statistics"),

    ("Data Analyst",
     "data reporting excel sql mysql dashboard"),

    ("Data Analyst",
     "business intelligence data analysis power bi tableau"),

    ("Data Analyst",
     "data analyst python sql pandas numpy visualization"),

    ("Data Analyst",
     "excel reporting dashboard sql data analysis"),

    ("Data Analyst",
     "data cleaning visualization python excel pandas"),

    ("Data Analyst",
     "statistics sql excel tableau data analyst"),

    ("Data Analyst",
     "power bi data visualization sql python"),

    ("Data Analyst",
     "data analysis mysql excel pandas reporting"),


    # =====================================================
    # DATA SCIENTIST
    # =====================================================

    ("Data Scientist",
     "data science machine learning python pandas numpy tensorflow"),

    ("Data Scientist",
     "machine learning python data science statistics pandas"),

    ("Data Scientist",
     "data scientist python machine learning numpy pandas"),

    ("Data Scientist",
     "artificial intelligence machine learning python tensorflow"),

    ("Data Scientist",
     "predictive analytics machine learning python statistics"),

    ("Data Scientist",
     "python data science machine learning data analysis"),

    ("Data Scientist",
     "machine learning tensorflow pandas numpy predictive modeling"),

    ("Data Scientist",
     "data science statistical modeling python pandas"),

    ("Data Scientist",
     "deep learning machine learning python tensorflow numpy"),

    ("Data Scientist",
     "data scientist artificial intelligence python pandas"),

    ("Data Scientist",
     "machine learning data analysis statistics python"),

    ("Data Scientist",
     "predictive modeling python pandas numpy tensorflow"),

    ("Data Scientist",
     "data science python machine learning visualization"),

    ("Data Scientist",
     "python statistics machine learning pandas numpy"),

    ("Data Scientist",
     "AI data science machine learning tensorflow python"),


    # =====================================================
    # WEB DEVELOPER
    # =====================================================

    ("Web Developer",
     "html css javascript php bootstrap web development mysql"),

    ("Web Developer",
     "frontend development html css javascript responsive website"),

    ("Web Developer",
     "web developer html css javascript php mysql"),

    ("Web Developer",
     "website development javascript html css bootstrap"),

    ("Web Developer",
     "frontend developer html css javascript responsive design"),

    ("Web Developer",
     "php mysql html css web application development"),

    ("Web Developer",
     "javascript frontend html css bootstrap website"),

    ("Web Developer",
     "web application php javascript mysql html css"),

    ("Web Developer",
     "responsive website development html css javascript"),

    ("Web Developer",
     "frontend web developer javascript bootstrap css html"),

    ("Web Developer",
     "php web development mysql javascript html"),

    ("Web Developer",
     "website programmer html css javascript php"),

    ("Web Developer",
     "frontend development css javascript html responsive"),

    ("Web Developer",
     "web design html css bootstrap javascript"),

    ("Web Developer",
     "web application development php mysql javascript"),


    # =====================================================
    # SOFTWARE DEVELOPER
    # =====================================================

    ("Software Developer",
     "software development java python c c++ oop programming"),

    ("Software Developer",
     "software engineer java python c++ sql programming"),

    ("Software Developer",
     "application development java python database software"),

    ("Software Developer",
     "programming software development java c c++ algorithms"),

    ("Software Developer",
     "software engineer python java sql github git"),

    ("Software Developer",
     "application developer java python c++ oop"),

    ("Software Developer",
     "software programming java c++ data structures"),

    ("Software Developer",
     "software developer java python mysql git"),

    ("Software Developer",
     "object oriented programming java c++ software"),

    ("Software Developer",
     "software engineering python java database"),

    ("Software Developer",
     "programming java c++ sql github"),

    ("Software Developer",
     "application software development python java"),

    ("Software Developer",
     "software developer c c++ java algorithms"),

    ("Software Developer",
     "software engineer programming python java oop"),

    ("Software Developer",
     "software development java python sql database")
]


# =========================================================
# CREATE DATAFRAME
# =========================================================

df = pd.DataFrame(
    data,
    columns=["job_role", "resume_text"]
)


print("\n" + "=" * 60)
print("              ML MODEL TRAINING")
print("=" * 60)

print("\nTotal training samples:", len(df))

print("\nJob Role Distribution:")
print(df["job_role"].value_counts())


# =========================================================
# FEATURES AND TARGET
# =========================================================

X = df["resume_text"]
y = df["job_role"]


# =========================================================
# TRAIN / TEST SPLIT
# =========================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)


# =========================================================
# ML PIPELINE
# =========================================================

model = Pipeline(
    [
        (
            "tfidf",
            TfidfVectorizer(
                lowercase=True,
                stop_words="english",
                ngram_range=(1, 2),
                sublinear_tf=True
            )
        ),

        (
            "classifier",
            LogisticRegression(
                max_iter=3000,
                C=2.0
            )
        )
    ]
)


# =========================================================
# TRAIN MODEL
# =========================================================

print("\nTraining ML model...")

model.fit(
    X_train,
    y_train
)


# =========================================================
# TEST MODEL
# =========================================================

predictions = model.predict(
    X_test
)

accuracy = accuracy_score(
    y_test,
    predictions
)


print("\n" + "-" * 60)
print("MODEL PERFORMANCE")
print("-" * 60)

print(
    f"\nTest Accuracy: {accuracy * 100:.2f}%"
)

print("\nClassification Report:\n")

print(
    classification_report(
        y_test,
        predictions,
        zero_division=0
    )
)


# =========================================================
# CROSS VALIDATION
# =========================================================

print("-" * 60)
print("CROSS VALIDATION")
print("-" * 60)

cv_scores = cross_val_score(
    model,
    X,
    y,
    cv=5
)

print(
    "\nCross-validation scores:"
)

for i, score in enumerate(
    cv_scores,
    start=1
):

    print(
        f"Fold {i}: {score * 100:.2f}%"
    )


print(
    f"\nAverage CV Accuracy: "
    f"{cv_scores.mean() * 100:.2f}%"
)


# =========================================================
# SAVE MODEL
# =========================================================

model_folder = "models"

os.makedirs(
    model_folder,
    exist_ok=True
)


model_path = os.path.join(
    model_folder,
    "job_role_model.pkl"
)


joblib.dump(
    model,
    model_path
)


print("\n" + "-" * 60)

print(
    "\nModel saved successfully!"
)

print(
    f"Location: {model_path}"
)


# =========================================================
# COMPLETE
# =========================================================

print("\n" + "=" * 60)
print("             TRAINING COMPLETE")
print("=" * 60)