"""
Vercel serverless function handler for FastAPI
"""
# Import the FastAPI app directly (all files are in api/ directory)
from main import app

# Export for Vercel
handler = app
