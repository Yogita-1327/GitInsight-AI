import pandas as pd


# ============================================================
# GitInsight-AI - PR-Level Recommendations
# ============================================================

print("GitInsight-AI - PR Recommendations")
print("=" * 55)


# ------------------------------------------------------------
# Load PR risk assessment
# ------------------------------------------------------------

risk_df = pd.read_csv(
    "data/processed/pr_risk_assessment.csv"
)

risk = risk_df.iloc[0]

pr_index = int(risk["pr_index"])
probability = float(risk["review_friction_probability"])
risk_score = float(risk["risk_score"])
risk_level = risk["risk_level"]


# ------------------------------------------------------------
# Load ML dataset
# ------------------------------------------------------------

df = pd.read_csv(
    "data/processed/ml_dataset_v1.csv"
)

pr = df.loc[df.index == pr_index].iloc[0]


# ------------------------------------------------------------
# Extract feature values
# ------------------------------------------------------------

lines_added = pr["lines_added"]
lines_deleted = pr["lines_deleted"]
total_changes = pr["total_changes"]
files_changed = pr["files_changed"]
commit_count = pr["commit_count"]
changes_per_file = pr["changes_per_file"]
commits_per_file = pr["commits_per_file"]

linked_issue_count = pr["linked_issue_count"]
open_linked_issue_count = pr["open_linked_issue_count"]
issue_density = pr["issue_density"]


# ------------------------------------------------------------
# Generate recommendations
# ------------------------------------------------------------

recommendations = []


# Large change size
if total_changes >= 500:
    recommendations.append(
        "Consider splitting the PR into smaller changes to reduce review complexity."
    )

elif total_changes >= 200:
    recommendations.append(
        "The PR contains a moderate amount of code change; consider keeping the scope focused."
    )


# High changes per file
if changes_per_file >= 100:
    recommendations.append(
        "A large number of changes are concentrated per file; review the modified files carefully."
    )


# Many files changed
if files_changed >= 10:
    recommendations.append(
        "Multiple files are modified; organize the PR clearly to make review easier."
    )


# Multiple commits
if commit_count >= 10:
    recommendations.append(
        "The PR contains many commits; consider consolidating related commits before review."
    )


# High commit density
if commits_per_file >= 5:
    recommendations.append(
        "There are several commits per modified file; ensure commit history is organized."
    )


# Linked issue check
if linked_issue_count == 0:
    recommendations.append(
        "No linked issue was detected; consider linking the relevant issue or requirement."
    )


# Open issue check
if open_linked_issue_count > 0:
    recommendations.append(
        "Review the linked open issues and ensure the PR addresses the relevant requirements."
    )


# Issue density
if issue_density > 0.5:
    recommendations.append(
        "The PR has a high issue density; verify that all related issues are addressed."
    )


# Risk-based recommendation
if risk_level == "HIGH":
    recommendations.append(
        "High review-friction risk detected; consider additional reviewer attention before merging."
    )

elif risk_level == "MEDIUM":
    recommendations.append(
        "Moderate review-friction risk detected; perform a focused review before merging."
    )

else:
    recommendations.append(
        "Low review-friction risk detected; proceed with the normal review process."
    )


# ------------------------------------------------------------
# Display assessment
# ------------------------------------------------------------

print("\n" + "=" * 55)
print("PR RECOMMENDATION")
print("=" * 55)

print(f"PR Index                   : {pr_index}")
print(f"Review Friction Probability: {probability:.4f}")
print(f"Risk Score                 : {risk_score:.2f}/100")
print(f"Risk Level                 : {risk_level}")


# ------------------------------------------------------------
# Display recommendations
# ------------------------------------------------------------

print("\nRecommendations")
print("-" * 55)

for i, recommendation in enumerate(recommendations, start=1):
    print(f"{i}. {recommendation}")


# ------------------------------------------------------------
# Save recommendations
# ------------------------------------------------------------

recommendation_df = pd.DataFrame({
    "pr_index": [pr_index] * len(recommendations),
    "risk_score": [risk_score] * len(recommendations),
    "risk_level": [risk_level] * len(recommendations),
    "recommendation": recommendations
})

recommendation_df.to_csv(
    "data/processed/pr_recommendations.csv",
    index=False
)


print("\nRecommendations saved to:")
print("data/processed/pr_recommendations.csv")

print("\nPR recommendation generation completed.")