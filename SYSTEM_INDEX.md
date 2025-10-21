# System Index - ResearchIQ Investment Research Intelligence

## ⚠️ Important Disclaimer

This is an educational research tool built as a portfolio project.

**NOT:**
- Financial advice
- Investment recommendations
- Professional analysis service
- Substitute for licensed financial advisor

**Purpose:**
Demonstrates systematic research methodology and
multi-source data synthesis for portfolio purposes only.

**Data Limitations:**
Uses free public APIs with known constraints.
Not suitable for actual investment decisions.

**Legal:**
No warranty. Use at own risk.
Consult licensed professionals for financial decisions.

## Project Structure

```
/InvestIQ
├── /frontend                   # Web interface
│   ├── index.html             # Homepage with asset selection
│   ├── report.html            # Analysis report display page
│   ├── /css
│   │   └── styles.css         # Tailwind + custom styling
│   ├── /js
│   │   ├── main.js            # Homepage interactions & API calls
│   │   └── report.js          # Report page data display logic
│   └── /assets
│       ├── logo.svg           # InvestIQ logo (from Figma)
│       └── /design            # Figma exports
├── /backend                   # Python FastAPI application
│   ├── main.py               # FastAPI app & endpoints
│   ├── /data_sources         # API integrations
│   │   ├── yfinance_api.py   # Price data (technical analysis source)
│   │   ├── news_api.py       # NewsAPI integration
│   │   ├── reddit_api.py     # Reddit mention volume
│   │   ├── google_trends.py  # Google Trends search interest
│   │   └── fear_greed.py     # Fear & Greed Index
│   ├── /analyzers            # Analysis logic
│   │   ├── technical.py      # Technical indicators (RSI, MA, volume)
│   │   ├── sentiment.py      # Sentiment aggregation
│   │   └── report_gen.py     # Report data formatter
│   ├── /utils                # Utilities
│   │   ├── config.py         # API keys, asset lists
│   │   └── pdf_generator.py  # PDF export functionality
│   └── /templates
│       └── report_template.html  # PDF report HTML template
├── /reports_temp             # Temporary PDF storage
├── /.claude                  # Claude Code context
│   └── CLAUDE.md            # Session state & memory
├── requirements.txt          # Python dependencies
├── runtime.txt              # Python version
├── Procfile                 # Railway deployment config
├── .env                     # API keys (not in git)
├── .env.example             # Example environment variables
├── .gitignore               # Git ignore rules
├── README.md                # Public documentation
├── DEV_LOG.md               # Development journal
├── SYSTEM_INDEX.md          # This file - technical map
├── NAVIGATION.md            # Non-technical usage guide
├── PROJECT_EXPLANATION.md   # Project overview & purpose
├── RESUME_CONTEXT.md        # Session resume context
└── PORTFOLIO_CONTEXT.md     # Career documentation
```

## Key Files & Purpose

### Frontend
- **index.html**: Homepage with hero section, asset type selector, ticker input
- **report.html**: Multi-section analysis report with confidence badges
- **main.js**: Form handling, API calls to backend, loading states
- **report.js**: Display report data, render visualizations, PDF download
- **styles.css**: Revolut-style aesthetic, responsive design, animations

### Backend
- **main.py**: FastAPI application with /analyze and /generate-pdf endpoints
- **technical.py**: Calculate RSI, Moving Averages, volume analysis from price data
- **sentiment.py**: Aggregate Fear & Greed, Google Trends, Reddit signals
- **report_gen.py**: Format all analysis data into structured JSON report
- **pdf_generator.py**: Convert report to professional PDF using WeasyPrint

### Data Sources (All with error handling)
- **yfinance_api.py**: Real-time price, volume, historical data (HIGH confidence)
- **news_api.py**: Recent headlines via NewsAPI (CONTEXT only)
- **reddit_api.py**: Mention volume from investing subreddits (LOW confidence)
- **google_trends.py**: Search interest trends (MEDIUM confidence)
- **fear_greed.py**: Market sentiment index (MEDIUM confidence)

## Data Flow

1. **User Input** → Frontend (index.html)
   - Select asset type: Stocks | Crypto | Indices | Commodities
   - Enter ticker symbol: e.g., AAPL, BTC-USD, ^GSPC

2. **API Request** → Backend (POST /analyze)
   - Frontend sends ticker + asset_type
   - Backend validates input

3. **Parallel Data Collection**
   - yfinance: Price history, volume data
   - NewsAPI: Recent headlines
   - Reddit: Mention counts
   - Google Trends: Search volume
   - Fear & Greed: Market sentiment score

4. **Analysis Processing**
   - Technical analysis: RSI, MA, volume trends
   - Sentiment aggregation: Combine all signals
   - Data validation & error handling
   - Confidence level assignment

5. **Report Generation**
   - Format structured JSON response
   - Include metadata, confidence levels
   - Return to frontend

6. **Display** → Frontend (report.html)
   - Render sections with confidence badges
   - Visualize data (charts, gauges)
   - Enable PDF download option

7. **PDF Export** (Optional)
   - POST report data to /generate-pdf
   - Backend generates PDF with WeasyPrint
   - Download triggered on frontend

## Data Confidence Levels

**HIGH Confidence:**
- Technical Analysis (yfinance data)
- Calculated indicators (RSI, MA, volume)

**MEDIUM Confidence:**
- Fear & Greed Index
- Google Trends signals

**LOW Confidence (Directional Only):**
- Reddit mention volume
- Social signals

**CONTEXT Only:**
- News headlines (limited coverage)

## Technology Stack

**Backend:**
- Python 3.11+
- FastAPI (web framework)
- yfinance (market data)
- praw (Reddit API)
- pytrends (Google Trends)
- requests (API calls)
- pandas (data processing)
- WeasyPrint (PDF generation)

**Frontend:**
- HTML5
- Tailwind CSS (styling)
- Vanilla JavaScript (no framework)
- Chart.js (visualizations)

**Deployment:**
- Railway (backend hosting)
- Environment variables for API keys
- Temporary file storage for PDFs

## API Rate Limits

- NewsAPI: 100 requests/day (free tier)
- Reddit: Generous limits (no concern)
- Google Trends: No hard limits
- yfinance: No official limits (respectful usage)
- Fear & Greed: Public API, no limits

## Error Handling Strategy

- Invalid ticker → User-friendly message
- API failures → Graceful degradation
- Rate limits → Clear notification
- Network errors → Retry logic
- Missing data → Section omitted with note

## Security & Privacy

- API keys in environment variables
- .env file not committed to git
- No user data stored
- Temporary PDFs auto-cleaned
- CORS configured for frontend access
