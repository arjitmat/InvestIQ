import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { AnimatedBackground } from '../components/AnimatedBackground';
import { ThemeToggle } from '../components/ThemeToggle';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const AVAILABLE_ASSETS = {
  stocks: [
    // Top 30 by Market Cap
    { ticker: 'AAPL', name: 'Apple Inc.' },
    { ticker: 'MSFT', name: 'Microsoft Corporation' },
    { ticker: 'GOOGL', name: 'Alphabet Inc. (Google)' },
    { ticker: 'AMZN', name: 'Amazon.com Inc.' },
    { ticker: 'NVDA', name: 'NVIDIA Corporation' },
    { ticker: 'META', name: 'Meta Platforms Inc.' },
    { ticker: 'TSLA', name: 'Tesla Inc.' },
    { ticker: 'BRK-B', name: 'Berkshire Hathaway Inc.' },
    { ticker: 'LLY', name: 'Eli Lilly and Company' },
    { ticker: 'V', name: 'Visa Inc.' },
    { ticker: 'UNH', name: 'UnitedHealth Group Inc.' },
    { ticker: 'XOM', name: 'Exxon Mobil Corporation' },
    { ticker: 'JPM', name: 'JPMorgan Chase & Co.' },
    { ticker: 'MA', name: 'Mastercard Inc.' },
    { ticker: 'JNJ', name: 'Johnson & Johnson' },
    { ticker: 'PG', name: 'Procter & Gamble Co.' },
    { ticker: 'AVGO', name: 'Broadcom Inc.' },
    { ticker: 'HD', name: 'The Home Depot Inc.' },
    { ticker: 'CVX', name: 'Chevron Corporation' },
    { ticker: 'MRK', name: 'Merck & Co. Inc.' },
    { ticker: 'COST', name: 'Costco Wholesale Corporation' },
    { ticker: 'ABBV', name: 'AbbVie Inc.' },
    { ticker: 'PEP', name: 'PepsiCo Inc.' },
    { ticker: 'KO', name: 'The Coca-Cola Company' },
    { ticker: 'WMT', name: 'Walmart Inc.' },
    { ticker: 'BAC', name: 'Bank of America Corp.' },
    { ticker: 'ORCL', name: 'Oracle Corporation' },
    { ticker: 'NFLX', name: 'Netflix Inc.' },
    { ticker: 'DIS', name: 'The Walt Disney Company' },
    { ticker: 'AMD', name: 'Advanced Micro Devices Inc.' },
  ],
  crypto: [
    // Top 10 by Market Cap
    { ticker: 'BTC-USD', name: 'Bitcoin' },
    { ticker: 'ETH-USD', name: 'Ethereum' },
    { ticker: 'USDT-USD', name: 'Tether' },
    { ticker: 'BNB-USD', name: 'Binance Coin' },
    { ticker: 'SOL-USD', name: 'Solana' },
    { ticker: 'USDC-USD', name: 'USD Coin' },
    { ticker: 'XRP-USD', name: 'Ripple' },
    { ticker: 'DOGE-USD', name: 'Dogecoin' },
    { ticker: 'ADA-USD', name: 'Cardano' },
    { ticker: 'AVAX-USD', name: 'Avalanche' },
  ],
  indices: [
    // Major Global Indices
    { ticker: '^GSPC', name: 'S&P 500' },
    { ticker: '^DJI', name: 'Dow Jones Industrial Average' },
    { ticker: '^IXIC', name: 'Nasdaq Composite' },
    { ticker: '^RUT', name: 'Russell 2000' },
    { ticker: '^FTSE', name: 'FTSE 100 (UK)' },
  ],
  commodities: [
    // Key Commodities
    { ticker: 'GC=F', name: 'Gold Futures' },
    { ticker: 'SI=F', name: 'Silver Futures' },
    { ticker: 'CL=F', name: 'Crude Oil Futures' },
    { ticker: 'NG=F', name: 'Natural Gas Futures' },
    { ticker: 'HG=F', name: 'Copper Futures' },
  ],
};

export default function Homepage() {
  const [isDark, setIsDark] = useState(() => {
    // Load theme from localStorage on initial render
    const savedTheme = localStorage.getItem('theme');
    return savedTheme === 'dark';
  });
  const [ticker, setTicker] = useState('');
  const [assetType, setAssetType] = useState<'stocks' | 'crypto' | 'indices' | 'commodities'>('stocks');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [searchQuery, setSearchQuery] = useState('');
  const [showDropdown, setShowDropdown] = useState(false);
  const navigate = useNavigate();

  // Filter assets based on search query
  const filteredAssets = AVAILABLE_ASSETS[assetType].filter(asset =>
    asset.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
    asset.ticker.toLowerCase().includes(searchQuery.toLowerCase())
  );

  // Apply dark mode class to document and save to localStorage
  useEffect(() => {
    if (isDark) {
      document.documentElement.classList.add('dark');
      localStorage.setItem('theme', 'dark');
    } else {
      document.documentElement.classList.remove('dark');
      localStorage.setItem('theme', 'light');
    }
  }, [isDark]);

  // Reset search and ticker when asset type changes
  useEffect(() => {
    setSearchQuery('');
    setTicker('');
    setShowDropdown(false);
  }, [assetType]);

  // Close dropdown when clicking outside
  useEffect(() => {
    const handleClickOutside = () => setShowDropdown(false);
    if (showDropdown) {
      document.addEventListener('click', handleClickOutside);
      return () => document.removeEventListener('click', handleClickOutside);
    }
  }, [showDropdown]);

  const handleAnalyze = async () => {
    if (!ticker.trim()) {
      setError('Please select an asset from the dropdown');
      return;
    }

    setLoading(true);
    setError('');

    try {
      const response = await fetch(`${API_BASE_URL}/analyze`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          ticker: ticker.toUpperCase(),
          asset_type: assetType
        })
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Analysis failed');
      }

      const data = await response.json();
      localStorage.setItem('reportData', JSON.stringify(data));
      navigate('/report');
    } catch (err: any) {
      setError(err.message || 'Failed to analyze asset. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className={`min-h-screen relative overflow-hidden transition-colors duration-500 ${
      isDark ? 'bg-[#0A1F44]' : 'bg-[#FAFBFC]'
    }`}>
      {/* Theme Toggle */}
      <ThemeToggle isDark={isDark} setIsDark={setIsDark} />

      {/* Animated Background */}
      <AnimatedBackground isDark={isDark} />

      {/* Hero Content */}
      <div className="relative z-10 max-w-7xl mx-auto px-6 lg:px-8">
        <div className="flex flex-col items-center justify-center min-h-screen text-center py-20">
          <div className="max-w-4xl space-y-8">
            {/* Main Headline */}
            <h1 className={`text-5xl sm:text-6xl lg:text-7xl tracking-tight transition-colors duration-500 font-bold ${
              isDark ? 'text-white' : 'text-[#0A1F44]'
            }`}>
              Investment Research,
              <br />
              <span className="text-[#00D9C0]">Automated</span>
            </h1>

            {/* Subheadline */}
            <p className={`text-xl sm:text-2xl max-w-2xl mx-auto opacity-90 transition-colors duration-500 ${
              isDark ? 'text-gray-300' : 'text-[#2D3748]'
            }`}>
              Professional due diligence in under 60 seconds
            </p>

            {/* Asset Selector Card */}
            <div className={`mt-12 p-8 rounded-2xl shadow-2xl transition-colors duration-500 ${
              isDark ? 'bg-[#1a2f54]/80' : 'bg-white/80'
            } backdrop-blur-sm`}>
              <h2 className={`text-2xl font-semibold mb-6 ${isDark ? 'text-white' : 'text-[#0A1F44]'}`}>
                Select Asset to Analyze
              </h2>

              {/* Asset Type Tabs */}
              <div className="flex flex-wrap gap-2 mb-6 justify-center">
                {(['stocks', 'crypto', 'indices', 'commodities'] as const).map((type) => (
                  <button
                    key={type}
                    onClick={() => setAssetType(type)}
                    className={`px-6 py-3 rounded-lg font-medium transition-all duration-200 ${
                      assetType === type
                        ? 'bg-[#00D9C0] text-white shadow-lg shadow-[#00D9C0]/30'
                        : isDark
                        ? 'bg-[#2D3748] text-gray-300 hover:bg-[#374151]'
                        : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                    }`}
                  >
                    {type.charAt(0).toUpperCase() + type.slice(1)}
                  </button>
                ))}
              </div>

              {/* Ticker Dropdown */}
              <div className="mb-6 relative" onClick={(e) => e.stopPropagation()}>
                <input
                  type="text"
                  value={searchQuery}
                  onChange={(e) => {
                    setSearchQuery(e.target.value);
                    setShowDropdown(true);
                    setError('');
                  }}
                  onFocus={() => setShowDropdown(true)}
                  placeholder="Search by name or ticker..."
                  className={`w-full px-6 py-4 rounded-lg text-lg transition-colors duration-200 ${
                    isDark
                      ? 'bg-[#2D3748] text-white placeholder-gray-400'
                      : 'bg-gray-100 text-gray-900 placeholder-gray-500'
                  } focus:outline-none focus:ring-2 focus:ring-[#00D9C0]`}
                />

                {/* Dropdown List */}
                {showDropdown && filteredAssets.length > 0 && (
                  <div className={`absolute z-50 w-full mt-2 rounded-lg shadow-xl max-h-64 overflow-y-auto ${
                    isDark ? 'bg-[#2D3748] border border-gray-700' : 'bg-white border border-gray-200'
                  }`}>
                    {filteredAssets.map((asset) => (
                      <button
                        key={asset.ticker}
                        type="button"
                        onClick={(e) => {
                          e.stopPropagation();
                          setTicker(asset.ticker);
                          setSearchQuery(`${asset.name} (${asset.ticker})`);
                          setShowDropdown(false);
                        }}
                        className={`w-full px-6 py-3 text-left hover:bg-[#00D9C0] hover:text-white transition-colors duration-150 ${
                          isDark ? 'text-white' : 'text-gray-900'
                        } first:rounded-t-lg last:rounded-b-lg`}
                      >
                        <div className="flex justify-between items-center">
                          <span className="font-medium">{asset.name}</span>
                          <span className={`text-sm ${isDark ? 'text-gray-400' : 'text-gray-500'}`}>
                            {asset.ticker}
                          </span>
                        </div>
                      </button>
                    ))}
                  </div>
                )}

                {ticker && (
                  <p className={`text-sm mt-2 ${isDark ? 'text-gray-400' : 'text-gray-600'}`}>
                    Selected: {ticker}
                  </p>
                )}
              </div>

              {/* Analyze Button */}
              <button
                onClick={handleAnalyze}
                disabled={loading}
                className="w-full bg-[#00D9C0] hover:bg-[#00c4ad] text-white py-4 rounded-lg font-semibold text-lg transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed shadow-lg hover:shadow-xl hover:-translate-y-0.5"
              >
                {loading ? 'Analyzing...' : 'Analyze Asset'}
              </button>

              {/* Error Message */}
              {error && (
                <div className="mt-4 p-4 bg-red-500/10 border border-red-500/50 rounded-lg text-red-500 text-sm">
                  {error}
                </div>
              )}
            </div>

            {/* Disclaimer */}
            <p className={`text-sm mt-8 ${isDark ? 'text-gray-400' : 'text-gray-600'}`}>
              ⚠️ Educational tool only. Not financial advice. Consult licensed professionals for investment decisions.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
