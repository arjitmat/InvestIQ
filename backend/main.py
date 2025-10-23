"""
ResearchIQ - FastAPI Backend Application
Main application coordinating all data collection and analysis
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import logging
from typing import Optional
import asyncio
import os
from pathlib import Path

# Import data collectors
from data_sources.yfinance_api import (
    get_price_data,
    get_options_sentiment,
    get_institutional_ownership,
    get_risk_metrics,
    get_insider_trading
)
from data_sources.news_api import get_headlines_for_ticker
from data_sources.reddit_api import get_mention_volume
from data_sources.google_trends import get_search_interest
from data_sources.fear_greed import get_fear_greed_index

# Import analyzers
from analyzers.technical import analyze_technical
from analyzers.sentiment import aggregate_sentiment
from analyzers.report_gen import generate_report_data
from analyzers.ai_insights import generate_ai_insights

# Import config
from utils.config import CORS_ORIGINS, APP_NAME, APP_VERSION, validate_ticker

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION,
    description="Investment Research Intelligence API - Educational tool for multi-source data synthesis"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request/Response Models
class AnalyzeRequest(BaseModel):
    ticker: str
    asset_type: Optional[str] = "stocks"  # stocks, crypto, indices, commodities

class AnalyzeResponse(BaseModel):
    status: str
    ticker: str
    report: Optional[dict] = None
    error: Optional[str] = None

# Routes

@app.get("/api")
async def root():
    """Root endpoint - API info"""
    return {
        "app": APP_NAME,
        "version": APP_VERSION,
        "description": "Investment Research Intelligence API",
        "disclaimer": "Educational tool only. Not financial advice.",
        "endpoints": {
            "/api/analyze": "POST - Analyze a ticker symbol",
            "/api/health": "GET - Health check",
            "/api/docs": "GET - API documentation"
        }
    }

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "app": APP_NAME,
        "version": APP_VERSION
    }

@app.post("/api/analyze", response_model=AnalyzeResponse)
async def analyze_asset(request: AnalyzeRequest):
    """
    Analyze an asset - main endpoint

    Orchestrates data collection from 5 sources and performs analysis

    Args:
        request: AnalyzeRequest with ticker and asset_type

    Returns:
        AnalyzeResponse with complete analysis report

    Process:
        1. Validate ticker
        2. Collect price data (yfinance) - REQUIRED
        3. Collect sentiment data (parallel):
           - News headlines (NewsAPI)
           - Reddit mentions (praw)
           - Google Trends (pytrends)
           - Fear & Greed Index
        4. Perform analysis:
           - Technical analysis (from price data)
           - Sentiment aggregation (from sentiment data)
        5. Generate formatted report
    """
    ticker = request.ticker.upper()
    asset_type = request.asset_type.lower()

    logger.info(f"Analysis request received for {ticker} ({asset_type})")

    try:
        # Step 1: Get price data (REQUIRED - if this fails, we can't proceed)
        logger.info(f"Fetching price data for {ticker}...")
        price_data = get_price_data(ticker)

        if not price_data:
            logger.error(f"Failed to fetch price data for {ticker}")
            raise HTTPException(
                status_code=404,
                detail=f"Asset '{ticker}' not found or no data available. Please check the ticker symbol."
            )

        company_name = price_data.get('company_name', ticker)

        # Step 2: Collect sentiment data in parallel (these are optional, won't fail if unavailable)
        logger.info(f"Collecting sentiment data for {ticker}...")

        # Use asyncio to gather data in parallel for faster response
        news_task = asyncio.to_thread(get_headlines_for_ticker, ticker, company_name)
        reddit_task = asyncio.to_thread(get_mention_volume, ticker, asset_type)
        trends_task = asyncio.to_thread(get_search_interest, company_name or ticker)
        fear_greed_task = asyncio.to_thread(get_fear_greed_index)

        # Gather all results
        news_data, reddit_data, trends_data, fear_greed_data = await asyncio.gather(
            news_task,
            reddit_task,
            trends_task,
            fear_greed_task,
            return_exceptions=True  # Don't fail if one source fails
        )

        # Handle exceptions from parallel tasks
        if isinstance(news_data, Exception):
            logger.warning(f"News data collection failed: {news_data}")
            news_data = None
        if isinstance(reddit_data, Exception):
            logger.warning(f"Reddit data collection failed: {reddit_data}")
            reddit_data = None
        if isinstance(trends_data, Exception):
            logger.warning(f"Trends data collection failed: {trends_data}")
            trends_data = None
        if isinstance(fear_greed_data, Exception):
            logger.warning(f"Fear & Greed data collection failed: {fear_greed_data}")
            fear_greed_data = None

        # Step 2b: Collect advanced market data (options, risk, institutional, insider)
        logger.info(f"Collecting advanced market data for {ticker}...")

        options_task = asyncio.to_thread(get_options_sentiment, ticker)
        risk_task = asyncio.to_thread(get_risk_metrics, ticker)
        institutional_task = asyncio.to_thread(get_institutional_ownership, ticker)
        insider_task = asyncio.to_thread(get_insider_trading, ticker)

        options_data, risk_data, institutional_data, insider_data = await asyncio.gather(
            options_task,
            risk_task,
            institutional_task,
            insider_task,
            return_exceptions=True
        )

        # Handle exceptions from parallel tasks
        if isinstance(options_data, Exception):
            logger.warning(f"Options data collection failed: {options_data}")
            options_data = None
        if isinstance(risk_data, Exception):
            logger.warning(f"Risk data collection failed: {risk_data}")
            risk_data = None
        if isinstance(institutional_data, Exception):
            logger.warning(f"Institutional data collection failed: {institutional_data}")
            institutional_data = None
        if isinstance(insider_data, Exception):
            logger.warning(f"Insider data collection failed: {insider_data}")
            insider_data = None

        # Step 3: Perform technical analysis
        logger.info(f"Performing technical analysis for {ticker}...")
        technical_analysis = analyze_technical(price_data)

        # Step 4: Aggregate sentiment
        logger.info(f"Aggregating sentiment for {ticker}...")
        sentiment_analysis = aggregate_sentiment(
            ticker,
            fear_greed_data,
            trends_data,
            reddit_data
        )

        # Step 5: Generate AI insights (optional - won't fail if unavailable)
        logger.info(f"Generating AI insights for {ticker}...")
        ai_insights = None
        try:
            ai_insights = await generate_ai_insights(
                ticker,
                price_data,
                technical_analysis,
                sentiment_analysis,
                news_data,
                risk_data,
                options_data,
                insider_data,
                institutional_data
            )
            logger.info(f"AI insights generated for {ticker}")
        except Exception as ai_error:
            logger.warning(f"AI insights generation failed (non-critical): {ai_error}")
            # Continue without AI insights - graceful degradation

        # Step 6: Generate complete report
        logger.info(f"Generating report for {ticker}...")
        report = generate_report_data(
            ticker,
            price_data,
            technical_analysis,
            sentiment_analysis,
            news_data,
            ai_insights,
            risk_data,
            options_data,
            insider_data,
            institutional_data
        )

        logger.info(f"Analysis complete for {ticker}")

        return AnalyzeResponse(
            status="success",
            ticker=ticker,
            report=report
        )

    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        logger.error(f"Error analyzing {ticker}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Internal error analyzing {ticker}: {str(e)}"
        )

@app.get("/api/assets")
async def get_supported_assets():
    """
    Get list of supported assets

    Returns:
        dict: Lists of supported stocks, crypto, indices, commodities
    """
    from utils.config import STOCKS, CRYPTO, INDICES, COMMODITIES

    return {
        "stocks": STOCKS,
        "crypto": CRYPTO,
        "indices": INDICES,
        "commodities": COMMODITIES,
        "total": len(STOCKS) + len(CRYPTO) + len(INDICES) + len(COMMODITIES)
    }

@app.get("/api/disclaimer")
async def get_disclaimer():
    """Get full disclaimer text"""
    return {
        "title": "⚠️ Important Disclaimer",
        "content": """
This is an educational research tool built as a portfolio project.

NOT:
- Financial advice
- Investment recommendations
- Professional analysis service
- Substitute for licensed financial advisor

Purpose:
Demonstrates systematic research methodology and
multi-source data synthesis for portfolio purposes only.

Data Limitations:
Uses free public APIs with known constraints.
Not suitable for actual investment decisions.

Legal:
No warranty. Use at own risk.
Consult licensed professionals for financial decisions.
        """.strip()
    }

# Mount static files FIRST (before any routes that might conflict)
frontend_path = Path(__file__).parent.parent / "frontend" / "dist"
if frontend_path.exists():
    # Mount static assets (JS, CSS, images) - this must be before catch-all
    app.mount("/assets", StaticFiles(directory=str(frontend_path / "assets")), name="assets")
    logger.info("Frontend assets mounted at /assets")
else:
    logger.warning("Frontend build not found. API-only mode.")

# Error handlers

@app.exception_handler(404)
async def not_found_handler(request, exc):
    return {
        "status": "error",
        "message": "Resource not found",
        "detail": str(exc.detail) if hasattr(exc, 'detail') else "Not found"
    }

@app.exception_handler(500)
async def internal_error_handler(request, exc):
    return {
        "status": "error",
        "message": "Internal server error",
        "detail": "An unexpected error occurred. Please try again later."
    }

# Serve React frontend - MUST be defined AFTER all API routes
if frontend_path.exists():
    # Serve index.html at root
    @app.get("/")
    async def serve_root():
        """Serve React frontend at root"""
        return FileResponse(frontend_path / "index.html")

    # Catch-all route to serve index.html for React Router (defined LAST)
    @app.get("/{full_path:path}")
    async def serve_frontend(full_path: str):
        """Serve React frontend for all non-API routes"""
        # If requesting a file with extension, try to serve it
        if "." in full_path.split("/")[-1]:
            file_path = frontend_path / full_path
            if file_path.exists():
                return FileResponse(file_path)

        # Otherwise serve index.html (for React Router)
        return FileResponse(frontend_path / "index.html")

# Run the application
if __name__ == "__main__":
    import uvicorn

    logger.info(f"Starting {APP_NAME} v{APP_VERSION}")
    logger.info("⚠️  EDUCATIONAL TOOL ONLY - NOT FINANCIAL ADVICE")

    # Get port from environment variable (for HuggingFace/Docker deployment)
    port = int(os.getenv("PORT", 8000))

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=False,  # Disable reload in production
        log_level="info"
    )
