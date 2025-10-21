"""
Vercel serverless function handler for FastAPI
"""
import sys
import os

# Add backend directory to Python path so imports work
backend_path = os.path.join(os.path.dirname(__file__), '..', 'backend')
sys.path.insert(0, backend_path)

# Now import the FastAPI app
from main import app

# Export for Vercel
handler = app
