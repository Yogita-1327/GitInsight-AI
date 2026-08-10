"""
github_client.py

Purpose:
Creates an authenticated GitHub client using
the Personal Access Token stored in .env
"""

from github import Github
from dotenv import load_dotenv
from pathlib import Path
import os


# -----------------------------
# Load Environment Variables
# -----------------------------

BASE_DIR = Path(__file__).resolve().parents[2]

load_dotenv(BASE_DIR / ".env")

TOKEN = os.getenv("GITHUB_TOKEN")

if TOKEN is None:
    raise ValueError("GitHub Token not found in .env")


# -----------------------------
# Create GitHub Client
# -----------------------------

github_client = Github(TOKEN)