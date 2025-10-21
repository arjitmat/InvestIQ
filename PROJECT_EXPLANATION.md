# ResearchIQ - Project Explanation

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

## The Problem

Investment research is time-consuming and fragmented. Conducting thorough due diligence on an asset requires:
- Analyzing technical charts and indicators
- Scanning news across multiple sources
- Checking social sentiment on various platforms
- Reviewing market-wide sentiment metrics

This process typically takes 30-60 minutes per asset. The quality depends on thoroughness and available time.

---

## The Solution

**ResearchIQ** is an automated research assistant that synthesizes multiple data dimensions into professional research briefs. It combines quantitative (technical) analysis with qualitative (sentiment) signals for systematic due diligence.

**Positioning:** This is a research synthesis tool, not a trading bot or signal generator.

---

## What It Analyzes

### Asset Coverage (25 Assets)
- **15 Major Stocks:** AAPL, MSFT, GOOGL, AMZN, TSLA, NVDA, META, JPM, BAC, V, MA, WMT, HD, DIS, NFLX
- **5 Cryptocurrencies:** BTC-USD, ETH-USD, SOL-USD, BNB-USD, ADA-USD
- **3 Stock Indices:** S&P 500 (^GSPC), Nasdaq (^IXIC), Dow (^DJI)
- **2 Commodities:** Gold (GC=F), Silver (SI=F)

### Data Dimensions

**1. Technical Analysis (HIGH Confidence)**
- RSI (Relative Strength Index)
- Moving Averages (20, 50, 200-day)
- Volume trends
- Calculated from real price data via yfinance
- Most reliable component of the analysis

**2. Market Sentiment (MEDIUM Confidence)**
- Fear & Greed Index (established market metric)
- Google Trends (retail search interest)
- Quantifiable sentiment signals
- Directional indicators

**3. Social Signals (LOW Confidence - Volume Only)**
- Reddit mention volume from investing subreddits
- Attention spike detection vs baseline
- NOT deep sentiment analysis (too noisy with free data)
- Context only, not actionable

**4. News Scan (CONTEXT Only)**
- Recent headlines with keywords
- Limited by NewsAPI free tier (100/day)
- Not comprehensive coverage
- Supporting context for awareness

---

## Key Differentiator

### Most Investment Tools:
- Promise trading signals
- Claim high accuracy
- Black box predictions
- Overpromise capabilities

### ResearchIQ Approach:
- **Transparent Methodology:** Clear data sources shown
- **Honest Limitations:** Explicit confidence levels for each section
- **Research Over Prediction:** Synthesis tool, not crystal ball
- **Professional Presentation:** Clean, accessible reports
- **Data Quality First:** Leads with reliable technical analysis
- **No Overpromising:** What you see is what you get

### Design Philosophy:
- Revolut-style professional aesthetic
- Minimalist, confident, accessible
- Not another cluttered financial dashboard
- Subtle interactions (professional, not flashy)
- Mobile-responsive modern design

---

## Technical Approach

### Data Quality Strategy
1. **Lead with reliability:** Technical analysis from real price data
2. **Support with signals:** Sentiment as directional context
3. **Cross-validate:** Multiple sources when possible
4. **Explicit confidence:** Every section labeled (HIGH/MEDIUM/LOW/CONTEXT)
5. **Honest about constraints:** Free API limitations acknowledged

### Architecture
- **Simple & Fast:** 2-page web application
- **Python Backend:** FastAPI for API endpoints
- **No Database:** Stateless design for simplicity
- **Free APIs:** All data sources on free tiers
- **PDF Export:** Professional deliverable format
- **Temporary Storage:** Reports auto-cleaned

### Data Sources (All Free)
- **yfinance:** Price/volume data (excellent quality)
- **Fear & Greed Index:** Established sentiment metric
- **Google Trends:** Search volume interest
- **Reddit API:** Mention volume tracking
- **NewsAPI:** Headlines (limited by free tier)

---

## Outcomes & Value

### Deliverable
- Professional research briefs in under 60 seconds
- Systematic analysis across 25 major assets
- Downloadable PDF reports
- Clean, accessible web interface

### Time Savings
- **Manual Research:** 30-60 minutes per asset
- **InvestIQ:** <1 minute per asset
- **Quality Improvement:** Systematic coverage vs ad-hoc analysis

### Demonstrated Capabilities
- Research methodology and systematic approach
- Multi-source data synthesis
- Professional deliverable creation
- Practical AI application (tool, not magic)
- Full-stack product thinking
- Honest data quality communication
- Design sensibility

---

## Technologies Used

**Frontend:**
- HTML5
- Tailwind CSS (responsive styling)
- Vanilla JavaScript (no framework bloat)

**Backend:**
- Python 3.11+
- FastAPI (modern web framework)

**Data Sources:**
- yfinance (market data)
- NewsAPI (news headlines)
- Reddit API via PRAW (social mentions)
- Google Trends via pytrends (search interest)
- Fear & Greed Index (public API)

**Tools:**
- WeasyPrint (PDF generation)
- pandas (data processing)
- Chart.js (visualizations)

**Deployment:**
- Railway (free tier hosting)
- Environment variables for API keys

---

## Development Timeline

**Total:** 4-5 days (estimated)

- **Day 1:** Project setup, documentation, backend foundation
- **Day 2:** Data collectors, analysis engine, API endpoints
- **Day 3:** Frontend (homepage + report page)
- **Day 4:** PDF generation, integration, testing
- **Day 5:** Deployment, polish, documentation

---

## What Makes This Valuable

### Not Just a Coding Exercise

This project demonstrates:

1. **Research Thinking:** Systematic validation approach
2. **Domain Knowledge:** Understanding of financial markets
3. **Data Literacy:** Ability to assess and communicate data quality
4. **Professional Communication:** Report format, confidence levels
5. **Practical AI Use:** AI as tool, not engineer
6. **Design Sensibility:** Professional aesthetic matters
7. **Honest Positioning:** Transparency builds credibility

---

## Use Cases

### For Individual Investors
- Quick due diligence before research deep-dive
- Systematic coverage of watchlist assets
- Multi-dimensional view (technical + sentiment + news)
- Professional reports for record-keeping

### For Learning & Practice
- Understand technical indicators
- See how different data sources compare
- Practice research methodology
- Learn to assess data quality

### As Portfolio Project
- Demonstrates full-stack capabilities
- Shows business understanding (what analysts need)
- Proves ability to work with constraints (free APIs)
- Professional presentation ready for showcase

---

## Limitations & Disclaimers

### Not Financial Advice
- This tool is for research and educational purposes
- Not investment recommendations
- Not a replacement for professional financial advice
- Users responsible for their own investment decisions

### Data Constraints
- Free API tiers have rate limits
- News coverage is limited (NewsAPI: 100 requests/day)
- Social sentiment is volume-only (not quality)
- Not real-time (slight delays possible)
- Not comprehensive (sampling of available data)

### What It's NOT
- ❌ Not a trading bot
- ❌ Not a prediction engine
- ❌ Not a recommendation system
- ❌ Not comprehensive financial analysis
- ❌ Not institutional-grade data

### What It IS
- ✅ Research synthesis tool
- ✅ Multi-source data aggregator
- ✅ Professional report generator
- ✅ Time-saving due diligence assistant
- ✅ Educational resource

---

## Future Enhancements (Potential V2)

- Portfolio tracking across multiple assets
- Historical accuracy scoring
- More data sources (if premium APIs added)
- Chat interface for Q&A about reports
- Email alerts for watchlist assets
- Comparison mode (compare 2+ assets)
- Custom indicator configuration
- Export to Excel/CSV
- Historical report archive

---

## Why This Project Matters

Investment research should be:
- **Systematic** (not ad-hoc)
- **Transparent** (not black box)
- **Accessible** (not only for experts)
- **Honest** (not overpromising)

InvestIQ embodies these principles while demonstrating modern web development, API integration, data synthesis, and professional design.

It's a practical tool that solves a real problem while showcasing technical and analytical capabilities.
