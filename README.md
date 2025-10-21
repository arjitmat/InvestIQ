# InvestIQ - AI-Enhanced Investment Research Platform

> An educational investment research tool that aggregates real-time market data, technical analysis, sentiment indicators, and AI-powered insights into comprehensive reports.

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
- React 18 + TypeScript
- Vite
- Tailwind CSS v4
- Framer Motion (animations)
- React Router

### Backend
- Python 3.13
- FastAPI
- yfinance (market data)
- NewsAPI (headlines)
- Reddit API (social sentiment)
- Google Trends (search interest)
- Google Gemini AI (insights)

## 📦 Installation

### Prerequisites
- Python 3.11+
- Node.js 18+
- npm or yarn

### Backend Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/InvestIQ.git
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

This app can be deployed to Railway, Vercel, or similar platforms.

### Railway Deployment
1. Push code to GitHub
2. Connect Railway to your GitHub repo
3. Add environment variables in Railway dashboard
4. Railway will auto-deploy on push

## 📄 License

MIT License

## 👨‍💻 Author

**Arjit** - AI/ML Consultant & Full-Stack Developer

---

**Remember**: This tool is for educational purposes only. Always do your own research and consult financial professionals before making investment decisions.
