---
title: InvestIQ
emoji: 📊
colorFrom: blue
colorTo: green
sdk: docker
pinned: false
license: mit
---

# InvestIQ - AI-Enhanced Investment Research Platform

> An educational investment research tool that aggregates real-time market data, technical analysis, sentiment indicators, and AI-powered insights into comprehensive reports.

## 🌐 Live Demo

**HuggingFace Space:** [Coming Soon]
**GitHub:** https://github.com/arjitmat/InvestIQ

## ⚠️ Important Disclaimer

**This is an EDUCATIONAL tool only. NOT financial advice.**
- Do not make investment decisions based solely on this tool
- Always consult licensed financial professionals
- Uses free-tier APIs with known limitations
- Past performance does not guarantee future results

## 🚀 Features

- **Real-time Market Data**: Price, volume, and technical indicators via yfinance
- **Technical Analysis**: RSI, Moving Averages, momentum indicators
- **Sentiment Aggregation**: News headlines, Reddit mentions, Google Trends
- **Fear & Greed Index**: Market-wide sentiment indicator
- **AI Insights**: Gemini-powered pattern recognition and cross-signal analysis
- **50+ Assets**: Stocks, Crypto, Indices, and Commodities
- **Beautiful UI**: Modern React interface with Tailwind CSS and Framer Motion
- **Dark Mode**: Full dark/light theme support

## 🛠️ Tech Stack

### Frontend
- **Framework:** React 18 + TypeScript
- **Build Tool:** Vite 7
- **Styling:** Tailwind CSS v4, shadcn/ui components
- **Animations:** Framer Motion
- **Charts:** Recharts
- **Deployment:** Vercel (serverless edge)

### Backend
- **Framework:** Python 3.11, FastAPI, Uvicorn
- **Data Sources:** yfinance, NewsAPI, Reddit API, Google Trends
- **AI:** Google Gemini 2.0 Flash
- **Caching:** In-memory with TTL
- **Deployment:** Render (free tier)

### Infrastructure
- **CI/CD:** GitHub Actions (auto-deploy on push)
- **CORS:** Configured for cross-origin requests
- **Environment:** Separate configs for dev/production

## 📦 Installation

### Prerequisites
- Python 3.11+
- Node.js 18+
- npm or yarn

### Backend Setup

1. Clone the repository:
```bash
git clone https://github.com/arjitmat/InvestIQ.git
cd InvestIQ
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install Python dependencies:
```bash
cd backend
pip install -r requirements.txt
```

4. Create `.env` file from template:
```bash
cp .env.example .env
```

5. Add your API keys to `.env`:
- Get NewsAPI key: https://newsapi.org/
- Get Reddit credentials: https://www.reddit.com/prefs/apps
- Get Gemini API key: https://makersuite.google.com/app/apikey

6. Run the backend:
```bash
python main.py
```
Backend will run on http://localhost:8000

### Frontend Setup

1. Navigate to frontend directory:
```bash
cd ../frontend-react
```

2. Install dependencies:
```bash
npm install
```

3. Run development server:
```bash
npm run dev
```
Frontend will run on http://localhost:5173

## 🎯 Usage

1. Open http://localhost:5173 in your browser
2. Select asset type (Stocks, Crypto, Indices, or Commodities)
3. Search for an asset by name or ticker
4. Click "Analyze Asset"
5. View comprehensive research report with:
   - Technical analysis (RSI, Moving Averages)
   - Sentiment analysis (News, Reddit, Market Sentiment)
   - AI-powered insights
   - Cross-signal analysis

## 📊 Available Assets

- **30 Stocks**: AAPL, MSFT, GOOGL, NVDA, TSLA, etc.
- **10 Cryptocurrencies**: BTC, ETH, SOL, BNB, etc.
- **5 Indices**: S&P 500, Nasdaq, Dow Jones, Russell 2000, FTSE 100
- **5 Commodities**: Gold, Silver, Crude Oil, Natural Gas, Copper

## 🔑 API Keys Required

- **NewsAPI** (Free tier: 100 requests/day)
- **Reddit API** (Free, rate limited)
- **Google Gemini AI** (Free tier: 60 requests/minute)

**No API key needed for:**
- yfinance (market data)
- Fear & Greed Index
- Google Trends (best-effort, may rate limit)

## 📈 Data Quality

| Data Source | Quality | Use Case |
|-------------|---------|----------|
| yfinance | ⭐⭐⭐⭐⭐ | Price data, technical analysis |
| Fear & Greed | ⭐⭐⭐⭐⭐ | Market sentiment |
| NewsAPI | ⭐⭐⭐ | Context only (headlines) |
| Reddit | ⭐⭐ | Volume/buzz detection |
| Google Trends | ⭐⭐ | Search interest (often rate-limited) |
| Gemini AI | ⭐⭐⭐ | Pattern insights (can be overconfident) |

## 🚧 Known Limitations

- Google Trends often hits rate limits (429 errors)
- Reddit API provides volume only, not sentiment analysis
- NewsAPI free tier limited to headlines only
- AI insights may occasionally fail JSON parsing
- Not suitable for live trading decisions

## 🚀 Deployment

### Current Production Setup (HuggingFace Spaces)

**Full-Stack Docker Deployment:**
- Frontend + Backend in single Docker container
- No cold starts, always ready
- Free tier with generous compute limits
- Built-in secrets management

### Deploy to HuggingFace Spaces

**1. Fork/Clone Repository**
```bash
git clone https://github.com/arjitmat/InvestIQ.git
cd InvestIQ
```

**2. Create HuggingFace Space**
- Go to https://huggingface.co/new-space
- Select "Docker" as SDK
- Name your space (e.g., "investiq")
- Select visibility (Public or Private)
- Create Space

**3. Add Environment Variables**
Go to Space Settings → Variables and Secrets, add:
- `NEWSAPI_KEY`: Your NewsAPI key
- `REDDIT_CLIENT_ID`: Your Reddit client ID
- `REDDIT_CLIENT_SECRET`: Your Reddit client secret
- `GEMINI_API_KEY`: Your Gemini API key

**4. Push to HuggingFace**
```bash
# Install HuggingFace CLI
pip install huggingface_hub

# Login to HuggingFace
huggingface-cli login

# Push to your space (replace YOUR_USERNAME and YOUR_SPACE_NAME)
git remote add hf https://huggingface.co/spaces/YOUR_USERNAME/YOUR_SPACE_NAME
git add .
git commit -m "Initial deployment to HuggingFace Spaces"
git push hf main
```

**5. Access Your Space**
Your app will be available at: `https://huggingface.co/spaces/YOUR_USERNAME/YOUR_SPACE_NAME`

### Alternative Deployment Options

**Docker (Local or Cloud)**
```bash
# Build the image
docker build -t investiq .

# Run with environment variables
docker run -p 7860:7860 \
  -e NEWSAPI_KEY=your_key \
  -e REDDIT_CLIENT_ID=your_id \
  -e REDDIT_CLIENT_SECRET=your_secret \
  -e GEMINI_API_KEY=your_key \
  investiq
```

**Railway / Render**
- Upload Dockerfile
- Configure environment variables
- Deploy (Railway: no cold starts, Render: 15-min cold starts on free tier)

## 📄 License

MIT License

## 👨‍💻 Author

**Arjit** - AI/ML Consultant & Full-Stack Developer

---

**Remember**: This tool is for educational purposes only. Always do your own research and consult financial professionals before making investment decisions.
