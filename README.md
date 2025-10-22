# InvestIQ - AI-Enhanced Investment Research Platform

> An educational investment research tool that aggregates real-time market data, technical analysis, sentiment indicators, and AI-powered insights into comprehensive reports.

## 🌐 Live Demo

**Frontend:** https://invest-iq-wheat.vercel.app
**Backend API:** https://investiq-backend.onrender.com
**GitHub:** https://github.com/arjitmat/InvestIQ

> **Note:** Backend is hosted on Render's free tier, which has a 15-minute inactivity sleep. First request after inactivity may take 30-45 seconds to wake up.

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

### Current Production Setup

**Frontend (Vercel):**
- Auto-deploys from `main` branch
- Environment variables configured in Vercel dashboard
- Instant cold starts, global CDN distribution
- Free tier, serverless edge deployment

**Backend (Render):**
- Deployed via `render.yaml` (infrastructure as code)
- Auto-deploys from `main` branch
- Environment variables configured in Render dashboard
- Free tier with 15-minute cold start after inactivity

### Deployment Instructions

**1. Fork/Clone Repository**
```bash
git clone https://github.com/arjitmat/InvestIQ.git
cd InvestIQ
```

**2. Deploy Frontend to Vercel**
- Go to https://vercel.com/new
- Import your GitHub repository
- Set Root Directory: `frontend-react`
- Add environment variable:
  - `VITE_API_URL`: Your backend URL (e.g., `https://your-backend.onrender.com`)
- Click Deploy

**3. Deploy Backend to Render**
- Go to https://render.com/
- Create new Blueprint instance
- Connect your GitHub repository
- Render will detect `render.yaml` and configure automatically
- Add environment variables in Render dashboard:
  - `NEWSAPI_KEY`
  - `REDDIT_CLIENT_ID`
  - `REDDIT_CLIENT_SECRET`
  - `GEMINI_API_KEY`
- Click Deploy

**4. Update Frontend Environment Variable**
- In Vercel dashboard, update `VITE_API_URL` to point to your Render backend URL
- Redeploy frontend

### Alternative Deployment Options

**Vercel (Full Stack - Not Recommended)**
- Frontend works perfectly
- Backend hits 50MB serverless function limit due to pandas/numpy dependencies
- Better to use Render or similar for Python backend

**Railway**
- Good alternative to Render
- $5 free credit per month
- No forced sleep after inactivity
- Follow similar process as Render

**Docker**
- Dockerfile and docker-compose.yml can be added for containerized deployment
- Suitable for AWS, GCP, Azure deployments

## 📄 License

MIT License

## 👨‍💻 Author

**Arjit** - AI/ML Consultant & Full-Stack Developer

---

**Remember**: This tool is for educational purposes only. Always do your own research and consult financial professionals before making investment decisions.
