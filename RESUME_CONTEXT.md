# Resume Context - ResearchIQ Development

## Purpose of This File

This file helps Claude Code resume development if a session expires. It provides essential context to continue building ResearchIQ without losing momentum.

---

## Project Overview

**ResearchIQ** - Investment Research Intelligence System

A web application that automates investment research by synthesizing technical analysis, sentiment data, social signals, and news into professional PDF reports in under 60 seconds.

**Key Principle:** Research synthesis tool (NOT trading bot). Transparent about data quality. Leads with reliable technical analysis.

---

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

---

## Technology Stack

### Backend
- Python 3.11+
- FastAPI (web framework)
- yfinance (market data)
- praw (Reddit API)
- pytrends (Google Trends)
- requests (API calls)
- pandas (data processing)
- WeasyPrint (PDF generation)

### Frontend
- HTML5
- Tailwind CSS
- Vanilla JavaScript
- Chart.js (visualizations)

### Deployment
- Railway (planned)
- Environment variables for API keys

---

## Project Structure

```
/InvestIQ (folder name)
├── /frontend          # HTML/CSS/JS web interface
├── /backend           # Python FastAPI application
│   ├── /data_sources  # API integrations (5 sources)
│   ├── /analyzers     # Analysis logic
│   ├── /utils         # Config, PDF generator
│   └── /templates     # PDF template
├── /reports_temp      # Temporary PDF storage
├── /.claude           # Session context (CLAUDE.md)
└── [documentation files]
```

---

## API Credentials

**Configured APIs:**
- NewsAPI Key: `1deee26aca4541d9b720f53a911e350a`
- Reddit Client ID: `2sRsQq4XE9OJxpOU2cS3qA`
- Reddit Client Secret: `eq-OjEvOlvUe3AjTRaHE4jyrZHbl9A`

**No Auth Needed:**
- yfinance
- Google Trends (pytrends)
- Fear & Greed Index

---

## Data Sources & Confidence Levels

1. **yfinance** → Technical Analysis (HIGH confidence)
2. **Fear & Greed Index** → Market Sentiment (MEDIUM confidence)
3. **Google Trends** → Search Interest (MEDIUM confidence)
4. **Reddit API** → Mention Volume (LOW confidence - directional only)
5. **NewsAPI** → Headlines (CONTEXT only - limited free tier)

**Strategy:** Lead with reliable data (technical), support with sentiment, honest about limitations.

---

## Asset Coverage (25 Total)

**Stocks (15):** AAPL, MSFT, GOOGL, AMZN, TSLA, NVDA, META, JPM, BAC, V, MA, WMT, HD, DIS, NFLX

**Crypto (5):** BTC-USD, ETH-USD, SOL-USD, BNB-USD, ADA-USD

**Indices (3):** ^GSPC, ^IXIC, ^DJI

**Commodities (2):** GC=F, SI=F

---

## If Session Expired: Resume Checklist

1. **Read `.claude/CLAUDE.md`** - Check current status
2. **Review `SYSTEM_INDEX.md`** - Understand architecture
3. **Check `DEV_LOG.md`** - See latest decisions
4. **Verify folder structure** - Ensure all directories exist
5. **Check last modified files** - See what was being worked on
6. **Continue from "Next Tasks"** in CLAUDE.md

---

## Testing Strategy

**Test with these tickers:**
- Stock: AAPL
- Crypto: BTC-USD
- Index: ^GSPC
- Commodity: GC=F

**Verify:**
- Data collection works
- Analysis calculations correct
- Report formatting clean
- PDF generation successful
- Error handling graceful
