"""
Vercel serverless function handler for FastAPI
"""
from mangum import Mangum
from main import app

# Wrap FastAPI app with Mangum for serverless deployment
handler = Mangum(app)
