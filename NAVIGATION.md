# Navigation Guide - InvestIQ (For Non-Technical Users)

## Quick Start - Testing Locally

### 1. Install Dependencies
```bash
# Navigate to project folder
cd /Users/arjit/Documents/Professional/AI\ Consulting/AI\ Projects/InvestIQ

# Install Python packages
pip install -r requirements.txt
```

**What it does:** Installs all necessary Python libraries for the backend

### 2. Start Backend Server
```bash
# From project root
cd backend
python main.py
```

**Expected output:** `Uvicorn running on http://127.0.0.1:8000`
**What it does:** Starts the API server that handles data collection and analysis

### 3. Open Frontend
```bash
# Option 1: Double-click the file
# Navigate to: frontend/index.html and double-click

# Option 2: Open in browser directly
# File path: file:///Users/arjit/Documents/Professional/AI Consulting/AI Projects/InvestIQ/frontend/index.html
```

**What it does:** Opens the homepage in your web browser

### 4. Run Your First Analysis
1. Homepage will load with asset selection
2. Choose asset type from dropdown: **Stocks**
3. Enter ticker symbol: **AAPL**
4. Click **"Analyze"** button
5. Wait ~30 seconds (collecting data from 5 sources)
6. Report page loads with analysis
7. Click **"Download PDF"** to save report

---

## Testing Different Assets

### Stocks to Test
- **AAPL** - Apple Inc.
- **MSFT** - Microsoft
- **GOOGL** - Google (Alphabet)
- **TSLA** - Tesla
- **NVDA** - NVIDIA

### Cryptocurrency
- **BTC-USD** - Bitcoin
- **ETH-USD** - Ethereum
- **SOL-USD** - Solana

### Stock Indices
- **^GSPC** - S&P 500
- **^IXIC** - Nasdaq Composite
- **^DJI** - Dow Jones

### Commodities
- **GC=F** - Gold Futures
- **SI=F** - Silver Futures

---

## Troubleshooting Common Issues

### "Cannot connect to backend" or "API Connection Failed"
**Problem:** Backend server is not running
**Solution:**
```bash
cd backend
python main.py
```
Check console for any error messages. Backend should say "Uvicorn running on http://127.0.0.1:8000"

### "Asset not found" or "Invalid ticker"
**Problem:** Ticker symbol is incorrect
**Solution:**
- Use correct format: AAPL (not Apple)
- For crypto: BTC-USD (not BTC)
- For indices: ^GSPC (with caret symbol)
- Check symbol on Yahoo Finance first

### "Rate limit exceeded" or "Too many requests"
**Problem:** NewsAPI free tier limit hit (100/day)
**Solution:**
- Wait 24 hours for reset
- Or try different assets (limit is per request, not per asset)
- Analysis will still work, just news section may be limited

### "Module not found" errors
**Problem:** Python packages not installed
**Solution:**
```bash
pip install -r requirements.txt
```

### PDF download not working
**Problem:** PDF generation failed or browser blocked download
**Solution:**
- Check browser's download settings/permissions
- Try different browser
- Check backend console for error messages
- Verify WeasyPrint is installed

---

## Understanding Your Report

### Technical Analysis Section (🟢 HIGH CONFIDENCE)
- **What it shows:** RSI, Moving Averages, Volume trends
- **Data source:** Real price data from yfinance
- **Reliability:** Very high - calculated from actual market data
- **Use for:** Primary technical indicators, momentum assessment

### Market Sentiment Section (🟡 MEDIUM CONFIDENCE)
- **What it shows:** Fear & Greed Index, Google Trends
- **Data source:** Established metrics, search volume
- **Reliability:** Medium - directional signals
- **Use for:** Supporting context, retail interest gauge

### Social Signals Section (⚪ LOW CONFIDENCE - DIRECTIONAL)
- **What it shows:** Reddit mention volume
- **Data source:** r/wallstreetbets, r/stocks, r/CryptoCurrency
- **Reliability:** Low - volume only, not sentiment quality
- **Use for:** Attention spike detection, NOT investment decisions

### News Headlines Section (⚪ CONTEXT ONLY)
- **What it shows:** Recent news headlines
- **Data source:** NewsAPI (limited free tier)
- **Reliability:** Context only - not comprehensive
- **Use for:** Quick overview of recent events

---

## File Locations

### Generated Reports
- **Location:** `/reports_temp/` folder
- **Format:** PDF files
- **Note:** Old reports auto-deleted (keeps last 10)

### Logs & Debugging
- **Backend logs:** Console where you ran `python main.py`
- **Frontend errors:** Browser console (F12 → Console tab)

### Configuration
- **API keys:** `/backend/utils/config.py` (or `.env` file)
- **Asset lists:** `/backend/utils/config.py`

### Design Assets
- **Figma exports:** `/frontend/assets/`
- **Logo:** `/frontend/assets/logo.svg`

---

## Development Commands Reference

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Run Backend (Development)
```bash
cd backend
python main.py
```

### Check API Documentation
While backend is running, visit:
```
http://localhost:8000/docs
```
This shows FastAPI's interactive API documentation

### Stop Backend
Press `Ctrl+C` in the terminal where backend is running

---

## API Rate Limits & Quotas

| Service | Free Tier Limit | What Happens When Hit |
|---------|----------------|----------------------|
| NewsAPI | 100 requests/day | News section shows limited data |
| Reddit | Generous (no concern) | Unlikely to hit |
| yfinance | No official limit | Use responsibly |
| Google Trends | No hard limit | Use responsibly |
| Fear & Greed | No limit | Always available |

---

## Need Help?

### Check These First:
1. Is backend running? (Check terminal)
2. Is ticker symbol correct? (Check Yahoo Finance)
3. Any error messages in browser console? (F12)
4. Any error messages in backend console?

### Common Fixes:
- Restart backend server
- Clear browser cache
- Check internet connection
- Verify API keys are set correctly
- Try a different ticker symbol

---

## Future Deployment

### When Deployed to Railway:
- Backend URL will change from `localhost:8000` to Railway URL
- Frontend needs to update API endpoint in `main.js`
- Environment variables set in Railway dashboard
- No need to run backend manually - auto-starts on Railway

### Accessing Deployed Version:
1. Visit Railway-provided URL
2. No installation needed
3. Works from any device with internet
4. Same functionality as local version
