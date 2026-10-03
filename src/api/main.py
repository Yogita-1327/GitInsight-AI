import pandas as pd

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from tabpfn import TabPFNClassifier

from src.ingestion.github_client import github_client
from src.ingestion.pr_parser import PRParser
from src.feature_engineering.feature_builder import FeatureBuilder


# ============================================================
# GitInsight-AI - FastAPI Backend
# ============================================================

app = FastAPI(
    title="GitInsight-AI API",
    description="ML-powered GitHub Pull Request review-friction prediction API",
    version="1.0.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================
# Load Training Dataset
# ============================================================

print("Loading GitInsight-AI dataset...")

df = pd.read_csv(
    "data/processed/ml_dataset_v1.csv"
)

X = df.drop(columns=["review_friction"])
y = df["review_friction"]


# ============================================================
# Train TabPFN
# ============================================================

print("Training TabPFN model...")

model = TabPFNClassifier(
    random_state=42,
    device="auto"
)

model.fit(X, y)

print("TabPFN model loaded successfully.")


# ============================================================
# Request Models
# ============================================================

class PRFeatures(BaseModel):

    lines_added: float
    lines_deleted: float
    total_changes: float
    files_changed: float
    commit_count: float

    addition_ratio: float
    deletion_ratio: float
    changes_per_file: float
    commits_per_file: float

    repository_stars_log: float
    repository_forks_log: float
    repository_open_issues_log: float

    linked_issue_count: float
    open_linked_issue_count: float
    issue_density: float


class PRRequest(BaseModel):

    repository: str
    pr_number: int


# ============================================================
# Recommendation Generator
# ============================================================

def generate_recommendations(data, risk_level):

    recommendations = []

    total_changes = data["total_changes"]
    files_changed = data["files_changed"]
    commit_count = data["commit_count"]
    changes_per_file = data["changes_per_file"]
    commits_per_file = data["commits_per_file"]

    linked_issue_count = data["linked_issue_count"]
    open_linked_issue_count = data["open_linked_issue_count"]
    issue_density = data["issue_density"]


    if total_changes >= 500:

        recommendations.append(
            "Consider splitting the PR into smaller changes "
            "to reduce review complexity."
        )

    elif total_changes >= 200:

        recommendations.append(
            "The PR contains a moderate amount of code change; "
            "consider keeping the scope focused."
        )


    if changes_per_file >= 100:

        recommendations.append(
            "A large number of changes are concentrated per file; "
            "review the modified files carefully."
        )


    if files_changed >= 10:

        recommendations.append(
            "Multiple files are modified; organize the PR clearly "
            "to make review easier."
        )


    if commit_count >= 10:

        recommendations.append(
            "The PR contains many commits; consider consolidating "
            "related commits before review."
        )


    if commits_per_file >= 5:

        recommendations.append(
            "There are several commits per modified file; "
            "ensure commit history is organized."
        )


    if linked_issue_count == 0:

        recommendations.append(
            "No linked issue was detected; consider linking "
            "the relevant issue or requirement."
        )


    if open_linked_issue_count > 0:

        recommendations.append(
            "Review the linked open issues and ensure the PR "
            "addresses the relevant requirements."
        )


    if issue_density > 0.5:

        recommendations.append(
            "The PR has a high issue density; verify that "
            "all related issues are addressed."
        )


    if risk_level == "HIGH":

        recommendations.append(
            "High review-friction risk detected; consider "
            "additional reviewer attention before merging."
        )

    elif risk_level == "MEDIUM":

        recommendations.append(
            "Moderate review-friction risk detected; "
            "perform a focused review before merging."
        )

    else:

        recommendations.append(
            "Low review-friction risk detected; "
            "proceed with the normal review process."
        )


    return recommendations


# ============================================================
# Root Endpoint
# ============================================================

@app.get("/")
def root():

    return {
        "message": "GitInsight-AI API is running",
        "status": "online"
    }


# ============================================================
# Health Endpoint
# ============================================================

@app.get("/health")
def health():

    return {
        "status": "healthy",
        "model": "TabPFN"
    }


# ============================================================
# Manual Prediction Endpoint
# ============================================================

@app.post("/predict")
def predict_pr(data: PRFeatures):

    input_data = pd.DataFrame(
        [data.model_dump()]
    )

    input_data = input_data[X.columns]

    probability = model.predict_proba(
        input_data
    )[0][1]

    risk_score = probability * 100


    if probability < 0.25:

        risk_level = "LOW"

    elif probability < 0.50:

        risk_level = "MEDIUM"

    else:

        risk_level = "HIGH"


    recommendations = generate_recommendations(
        data.model_dump(),
        risk_level
    )


    return {

        "review_friction_probability":
            round(float(probability), 4),

        "risk_score":
            round(float(risk_score), 2),

        "risk_level":
            risk_level,

        "recommendations":
            recommendations
    }


# ============================================================
# Automatic GitHub PR Analysis
# ============================================================

@app.post("/analyze-pr")
def analyze_pr(request: PRRequest):

    try:

        # --------------------------------------------
        # Get GitHub repository
        # --------------------------------------------

        repository = github_client.get_repo(
            request.repository
        )


        # --------------------------------------------
        # Get Pull Request
        # --------------------------------------------

        pr = repository.get_pull(
            request.pr_number
        )


        # --------------------------------------------
        # Parse PR using existing pipeline
        # --------------------------------------------

        raw_pr_data = PRParser.parse(
            pr,
            repository
        )


        # --------------------------------------------
        # Build 15 ML features
        # --------------------------------------------

        features = FeatureBuilder.build(
            raw_pr_data
        )


        # --------------------------------------------
        # Convert to DataFrame
        # --------------------------------------------

        input_data = pd.DataFrame(
            [features]
        )


        # Ensure exact feature order
        input_data = input_data[X.columns]


        # --------------------------------------------
        # TabPFN prediction
        # --------------------------------------------

        probability = model.predict_proba(
            input_data
        )[0][1]


        risk_score = probability * 100


        # --------------------------------------------
        # Risk level
        # --------------------------------------------

        if probability < 0.25:

            risk_level = "LOW"

        elif probability < 0.50:

            risk_level = "MEDIUM"

        else:

            risk_level = "HIGH"


        # --------------------------------------------
        # Recommendations
        # --------------------------------------------

        recommendations = generate_recommendations(
            features,
            risk_level
        )


        # --------------------------------------------
        # Final API response
        # --------------------------------------------

        return {

            "repository":
                request.repository,

            "pr_number":
                request.pr_number,

            "title":
                raw_pr_data["title"],

            "author":
                raw_pr_data["author"],

            "files_changed":
                raw_pr_data["files_changed"],

            "lines_added":
                raw_pr_data["lines_added"],

            "lines_deleted":
                raw_pr_data["lines_deleted"],

            "commit_count":
                raw_pr_data["commit_count"],

            "linked_issue_count":
                raw_pr_data["linked_issue_count"],

            "review_friction_probability":
                round(float(probability), 4),

            "risk_score":
                round(float(risk_score), 2),

            "risk_level":
                risk_level,

            "recommendations":
                recommendations,

            "features":
                features
        }


    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )