# InvestIQ - Claude Code Session Context

## Current Status
- **Phase:** ✅ FULLY DEPLOYED & PRODUCTION READY WITH ENHANCEMENTS
- **Last working:** Successfully deployed to HuggingFace Spaces with advanced features
- **Live URL:** https://huggingface.co/spaces/arjitmat/investiq
- **Previous URLs (deprecated):**
  - Frontend: https://invest-iq-wheat.vercel.app
  - Backend: https://investiq-backend.onrender.com
- **Next step:** Optional improvements (custom domain, demo video)
- **Blocked on:** Nothing - fully functional in production

## Recent Changes (Enhancement Session - Oct 23, 2025)
- [2025-10-23] **MAJOR ENHANCEMENT**: Added advanced market data analysis
  - Options sentiment (Put/Call ratio analysis with interpretation)
  - Insider trading activity (buys vs sells with sentiment scoring)
  - Institutional ownership (top 5 holders, concentration data)
  - Risk metrics (volatility 30d/90d, beta, 52-week ranges, risk scoring)
- [2025-10-23] **Expanded AI insights from 3 to 7**:
  - Price momentum analysis
  - Support/resistance level identification
  - Volume anomaly detection
  - Technical pattern recognition (existing)
  - News sentiment extraction (existing)
  - Cross-signal validation (existing)
  - Risk assessment insight (new)
- [2025-10-23] Updated frontend with 4 new sections:
  - Risk Metrics card (color-coded risk levels)
  - Options Market card (Put/Call visualization)
  - Insider Activity card (buy/sell breakdown)
  - Institutional Ownership card (top holders)
- [2025-10-23] Deployed to HuggingFace Spaces (https://huggingface.co/spaces/arjitmat/investiq)
- [2025-10-23] All enhancements use existing yfinance API (no new keys needed)
- [2025-10-23] Graceful degradation for all new data sources

## Previous Changes (Deployment Session - Oct 21-22, 2025)
- [2025-10-22] Deployed frontend to Vercel (https://invest-iq-wheat.vercel.app)
- [2025-10-22] Deployed backend to Render (https://investiq-backend.onrender.com)
- [2025-10-22] Created render.yaml for infrastructure as code deployment
- [2025-10-22] Attempted Vercel backend deployment (hit serverless limitations)
- [2025-10-22] Created api/ directory with Mangum adapter for serverless attempts
- [2025-10-22] Optimized requirements.txt for serverless (removed weasyprint, lighter pandas/numpy)
- [2025-10-22] Configured CORS to allow Vercel frontend
- [2025-10-22] Fixed all UI components (card, button, alert, badge, progress)
- [2025-10-22] Fixed AnimatedBackground MotionStyle errors
- [2025-10-22] Added recharts dependency for charts
- [2025-10-22] Updated vite.config.ts with preview configuration
- [2025-10-22] Successfully integrated React frontend with FastAPI backend

## Frontend Build Changes (Current Session)
- [2025-10-21] Created frontend/css/styles.css with complete Figma design system
- [2025-10-21] Built frontend/index.html with hero section, asset selector, theme toggle
- [2025-10-21] Created frontend/js/main.js with API integration and loading states
- [2025-10-21] Built frontend/report.html with all analysis sections (technical, sentiment, news, AI)
- [2025-10-21] Created frontend/js/report.js to render backend data dynamically
- [2025-10-21] Fixed Python typing import bug in reddit_api.py
- [2025-10-21] Started both servers: Backend (port 8000), Frontend (port 8080)

## AI Enhancement Changes (Previous Session)
- [2025-10-21] Added Gemini API key to .env and config
- [2025-10-21] Created smart caching system (backend/utils/cache.py) with TTL and invalidation
- [2025-10-21] Built AI insights analyzer (backend/analyzers/ai_insights.py) with 3 AI functions:
  - Technical pattern recognition (divergences, anomalies)
  - News sentiment extraction (sentiment + themes + notable events)
  - Cross-signal analysis (spots contradictions across data sources)
- [2025-10-21] Integrated AI insights into /analyze endpoint with graceful degradation
- [2025-10-21] Updated report_gen.py to include AI insights section
- [2025-10-21] Added google-generativeai to requirements.txt
- [2025-10-21] Tested AI integration successfully with sample data
- [2025-10-21] Received Figma designs for report page structure

## Known Issues
- Backend on Render free tier has 15-minute cold start (acceptable for portfolio)
- Frontend needs VITE_API_URL environment variable updated in Vercel dashboard
- PDF export feature disabled (WeasyPrint removed for size optimization)

## Environment & Configuration
- **APIs Configured:**
  - NewsAPI: ✅ Key obtained
  - Reddit API: ✅ Client ID & Secret obtained
  - Gemini AI: ✅ API key obtained (Google AI Studio)
  - yfinance: ✅ No key needed
  - Google Trends: ✅ No key needed
  - Fear & Greed Index: ✅ No key needed

- **Tech Stack:**
  - Backend: Python 3.11, FastAPI, Uvicorn
  - Frontend: React 18, TypeScript, Vite 7, Tailwind CSS, shadcn/ui
  - Charts: Recharts
  - AI: Google Gemini 2.0 Flash
  - Deployment:
    - Frontend: Vercel (serverless, instant)
    - Backend: Render (free tier, 15-min cold start)

- **Development Status:**
  - Backend structure: ✅ Complete & Deployed
  - Data collectors: ✅ Complete (9 data sources working in production)
    - Price data (yfinance)
    - News headlines (NewsAPI)
    - Reddit sentiment (praw)
    - Google Trends (pytrends)
    - Fear & Greed Index
    - **NEW**: Options sentiment (yfinance)
    - **NEW**: Insider trading (yfinance)
    - **NEW**: Institutional ownership (yfinance)
    - **NEW**: Risk metrics (yfinance)
  - Analysis engine: ✅ Complete (technical + sentiment + risk)
  - AI insights engine: ✅ Complete (7 insights with Gemini 2.0 Flash)
  - Report generation: ✅ Complete (with 9 report sections)
  - FastAPI endpoints: ✅ Complete & Live
  - Smart caching: ✅ Complete
  - Frontend: ✅ Complete & Deployed (React + TypeScript)
  - Frontend-Backend Integration: ✅ Working in Production
  - PDF generation: ❌ Disabled (removed for deployment size)
  - Full Integration testing: ✅ Tested & Working
  - Deployment: ✅ COMPLETE (HuggingFace Spaces)

## Important Decisions
- **Deployment Architecture:**
  - Split deployment: Frontend (Vercel) + Backend (Render)
  - Chose free tier with cold starts over paid hosting
  - Acceptable for portfolio (noted in documentation)
- **Frontend:**
  - Migrated from vanilla JS to React + TypeScript for better scalability
  - Used shadcn/ui component library for professional UI
  - Tailwind CSS for responsive design
- **Backend:**
  - Removed WeasyPrint to fit Vercel serverless limits (ultimately stayed on Render)
  - Downgraded pandas/numpy for lighter bundle
  - Report data stored temporarily (no database)
- **Data Strategy:**
  - Leading with technical analysis (most reliable data)
  - Honest about data limitations in UI
  - Free API tier constraints accepted
- **AI Integration Strategy:**
  - Subtle AI co-analyst approach (not overwhelming)
  - AI spots patterns/anomalies that math misses
  - Educational framing ("suggests" not "will")
  - Graceful degradation (works without AI)
  - Smart caching (1-hour TTL, reduces API calls)
  - Gemini 2.0 Flash for speed and free tier

## API Keys (Environment Variables)
- NEWSAPI_KEY: Configured
- REDDIT_CLIENT_ID: Configured
- REDDIT_CLIENT_SECRET: Configured
- GEMINI_API_KEY: Configured

## Asset Coverage
**25 Total Assets:**
- 15 Stocks: AAPL, MSFT, GOOGL, AMZN, TSLA, NVDA, META, JPM, BAC, V, MA, WMT, HD, DIS, NFLX
- 5 Crypto: BTC-USD, ETH-USD, SOL-USD, BNB-USD, ADA-USD
- 3 Indices: ^GSPC (S&P 500), ^IXIC (Nasdaq), ^DJI (Dow)
- 2 Commodities: GC=F (Gold), SI=F (Silver)

## Production URLs
- **Production (HuggingFace Spaces):** https://huggingface.co/spaces/arjitmat/investiq
- **GitHub Repository:** https://github.com/arjitmat/InvestIQ
- **Previous URLs (deprecated):**
  - Frontend (Vercel): https://invest-iq-wheat.vercel.app
  - Backend (Render): https://investiq-backend.onrender.com

## Optional Future Enhancements
1. Custom domain (e.g., investiq.com) - $10-15/year
2. Demo video recording (2-3 minutes for recruiters)
3. Upgrade Render to paid tier ($7/month) to remove cold starts
4. Re-enable PDF export with alternative lighter library
5. Add user authentication for saved reports
6. Database integration for persistent report storage
