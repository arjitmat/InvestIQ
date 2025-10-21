import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { ThemeToggle } from '../components/ThemeToggle';
import { RSIGauge } from '../components/RSIGauge';
import { FearGreedGauge } from '../components/FearGreedGauge';

export default function ReportPage() {
  const [isDark, setIsDark] = useState(() => {
    // Load theme from localStorage on initial render
    const savedTheme = localStorage.getItem('theme');
    return savedTheme === 'dark';
  });
  const [reportData, setReportData] = useState<any>(null);
  const navigate = useNavigate();

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

  useEffect(() => {
    const savedData = localStorage.getItem('reportData');
    if (!savedData) {
      navigate('/');
      return;
    }

    try {
      const data = JSON.parse(savedData);
      setReportData(data);
    } catch (error) {
      console.error('Error parsing report data:', error);
      navigate('/');
    }
  }, [navigate]);

  if (!reportData) {
    return <div className="min-h-screen flex items-center justify-center">Loading...</div>;
  }

  const { report } = reportData;
  const metadata = report.metadata;
  const technical = report.technical_analysis;
  const sentiment = report.sentiment_analysis;
  const news = report.news_headlines;
  const aiInsights = report.ai_insights;

  return (
    <div className={`min-h-screen transition-colors duration-500 ${
      isDark ? 'dark bg-[#0A1F44]' : 'bg-[#FAFBFC]'
    }`}>
      {/* Theme Toggle */}
      <ThemeToggle isDark={isDark} setIsDark={setIsDark} />

      <div className="max-w-7xl mx-auto px-6 py-8">
        {/* Header */}
        <div className="flex flex-col md:flex-row justify-between items-start md:items-center mb-8 gap-4">
          <div>
            <h1 className={`text-3xl font-bold mb-2 ${isDark ? 'text-white' : 'text-[#0A1F44]'}`}>
              {metadata.company_name} ({metadata.ticker})
            </h1>
            <div className="flex items-center gap-4">
              <p className={`text-2xl font-semibold ${isDark ? 'text-white' : 'text-[#0A1F44]'}`}>
                ${metadata.current_price.toFixed(2)}
              </p>
              <p className={`text-lg ${metadata.price_change_percent >= 0 ? 'text-green-500' : 'text-red-500'}`}>
                {metadata.price_change_percent >= 0 ? '+' : ''}{metadata.price_change_percent.toFixed(2)}%
              </p>
            </div>
            <p className={`text-sm mt-1 ${isDark ? 'text-gray-400' : 'text-gray-600'}`}>
              Last updated: {metadata.timestamp}
            </p>
          </div>
          <div className="flex gap-3">
            <button
              onClick={() => navigate('/')}
              className={`px-6 py-3 rounded-lg font-medium transition-all duration-200 ${
                isDark
                  ? 'bg-[#2D3748] text-white hover:bg-[#374151]'
                  : 'bg-white text-[#0A1F44] hover:bg-gray-100'
              } shadow-md`}
            >
              ← New Analysis
            </button>
            <button
              onClick={() => window.print()}
              className="px-6 py-3 bg-[#00D9C0] hover:bg-[#00c4ad] text-white rounded-lg font-medium transition-all duration-200 shadow-md"
            >
              Download PDF
            </button>
          </div>
        </div>

        {/* Analysis Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
          {/* Technical Analysis Card */}
          <div className={`p-6 rounded-2xl shadow-lg transition-all duration-300 hover:shadow-xl ${
            isDark ? 'bg-[#1a2f54]/80' : 'bg-white'
          }`}>
            <div className="flex justify-between items-center mb-4">
              <h2 className={`text-xl font-semibold ${isDark ? 'text-white' : 'text-[#0A1F44]'}`}>
                Technical Analysis
              </h2>
              <span className="px-3 py-1 bg-green-500 text-white text-sm font-medium rounded-full">
                HIGH Confidence
              </span>
            </div>

            {/* RSI Gauge */}
            {technical?.rsi && (
              <div className="mb-6">
                <h3 className={`font-medium mb-3 text-center ${isDark ? 'text-white' : 'text-[#0A1F44]'}`}>
                  RSI (14-day)
                </h3>
                <RSIGauge value={technical.rsi.value} />
              </div>
            )}

            {/* Moving Averages */}
            {technical?.moving_averages?.values && (
              <div className="mb-6">
                <h3 className={`font-medium mb-3 ${isDark ? 'text-white' : 'text-[#0A1F44]'}`}>
                  Moving Averages
                </h3>
                <div className="space-y-2">
                  <div className="flex justify-between">
                    <span className={isDark ? 'text-gray-400' : 'text-gray-600'}>20-day MA</span>
                    <span className={`font-medium ${isDark ? 'text-white' : 'text-[#0A1F44]'}`}>
                      ${technical.moving_averages.values.MA_20?.toFixed(2) || 'N/A'}
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span className={isDark ? 'text-gray-400' : 'text-gray-600'}>50-day MA</span>
                    <span className={`font-medium ${isDark ? 'text-white' : 'text-[#0A1F44]'}`}>
                      ${technical.moving_averages.values.MA_50?.toFixed(2) || 'N/A'}
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span className={isDark ? 'text-gray-400' : 'text-gray-600'}>200-day MA</span>
                    <span className={`font-medium ${isDark ? 'text-white' : 'text-[#0A1F44]'}`}>
                      ${technical.moving_averages.values.MA_200?.toFixed(2) || 'N/A'}
                    </span>
                  </div>
                </div>
              </div>
            )}

            {/* Overall Signal */}
            <div className={`p-3 rounded-lg ${isDark ? 'bg-[#2D3748]' : 'bg-gray-100'}`}>
              <div className="flex justify-between items-center">
                <span className={`font-medium ${isDark ? 'text-white' : 'text-[#0A1F44]'}`}>
                  Overall Signal
                </span>
                <span className={`font-bold ${isDark ? 'text-[#00D9C0]' : 'text-[#00D9C0]'}`}>
                  {technical?.overall_signal || 'neutral'}
                </span>
              </div>
            </div>

            {/* AI Technical Insight */}
            {aiInsights?.status === 'available' && aiInsights.technical_insight && (
              <div className="mt-4 p-3 rounded-lg bg-purple-500/10 border border-purple-500/30">
                <div className="flex items-start gap-2">
                  <span className="px-2 py-1 bg-purple-500 text-white text-xs font-medium rounded">AI</span>
                  <p className={`text-sm ${isDark ? 'text-gray-300' : 'text-gray-700'}`}>
                    {aiInsights.technical_insight}
                  </p>
                </div>
              </div>
            )}
          </div>

          {/* Sentiment Analysis Card */}
          <div className={`p-6 rounded-2xl shadow-lg transition-all duration-300 hover:shadow-xl ${
            isDark ? 'bg-[#1a2f54]/80' : 'bg-white'
          }`}>
            <div className="flex justify-between items-center mb-4">
              <h2 className={`text-xl font-semibold ${isDark ? 'text-white' : 'text-[#0A1F44]'}`}>
                Sentiment Analysis
              </h2>
              <span className="px-3 py-1 bg-yellow-500 text-white text-sm font-medium rounded-full">
                MEDIUM Confidence
              </span>
            </div>

            {/* Fear & Greed Gauge */}
            {sentiment?.market_sentiment?.data?.value !== undefined && (
              <div className="mb-6">
                <h3 className={`font-medium mb-3 text-center ${isDark ? 'text-white' : 'text-[#0A1F44]'}`}>
                  Market Sentiment
                </h3>
                <FearGreedGauge value={sentiment.market_sentiment.data.value} />
                <p className={`text-xs text-center mt-2 ${isDark ? 'text-gray-500' : 'text-gray-500'}`}>
                  Overall stock market indicator (same for all assets)
                </p>
              </div>
            )}

            {/* Other Sentiment Metrics */}
            <div className="space-y-4">
              {sentiment?.retail_interest?.data && (
                <div className="flex justify-between items-center">
                  <span className={isDark ? 'text-gray-400' : 'text-gray-600'}>Search Interest</span>
                  <span className={`font-medium ${isDark ? 'text-white' : 'text-[#0A1F44]'}`}>
                    {sentiment.retail_interest.data.interest_level}
                  </span>
                </div>
              )}
              {sentiment?.social_signals?.data && (
                <div className="flex justify-between items-center">
                  <span className={isDark ? 'text-gray-400' : 'text-gray-600'}>Reddit Mentions</span>
                  <span className={`font-medium ${isDark ? 'text-white' : 'text-[#0A1F44]'}`}>
                    {sentiment.social_signals.data.total_mentions} ({sentiment.social_signals.data.vs_baseline})
                  </span>
                </div>
              )}
            </div>

            {/* Overall Sentiment */}
            {sentiment?.overall_sentiment && (
              <div className={`mt-6 p-3 rounded-lg ${isDark ? 'bg-[#2D3748]' : 'bg-gray-100'}`}>
                <div className="flex justify-between items-center">
                  <span className={`font-medium ${isDark ? 'text-white' : 'text-[#0A1F44]'}`}>
                    Overall Sentiment
                  </span>
                  <span className={`font-bold ${isDark ? 'text-[#00D9C0]' : 'text-[#00D9C0]'}`}>
                    {sentiment.overall_sentiment.assessment}
                  </span>
                </div>
              </div>
            )}
          </div>
        </div>

        {/* News Context Card */}
        {news && news.headlines && news.headlines.length > 0 && (
          <div className={`p-6 rounded-2xl shadow-lg mb-6 ${isDark ? 'bg-[#1a2f54]/80' : 'bg-white'}`}>
            <div className="flex justify-between items-center mb-4">
              <h2 className={`text-xl font-semibold ${isDark ? 'text-white' : 'text-[#0A1F44]'}`}>
                News Context
              </h2>
              <span className="px-3 py-1 bg-blue-500 text-white text-sm font-medium rounded-full">
                CONTEXT ONLY
              </span>
            </div>

            {/* AI News Sentiment */}
            {aiInsights?.status === 'available' && aiInsights.news_sentiment && (
              <div className="mb-4 p-3 rounded-lg bg-purple-500/10 border border-purple-500/30">
                <div className="flex items-start gap-2 mb-2">
                  <span className="px-2 py-1 bg-purple-500 text-white text-xs font-medium rounded">AI</span>
                  <div className="flex-1">
                    <div className="flex gap-2 mb-1">
                      <span className={`text-sm font-medium ${isDark ? 'text-gray-300' : 'text-gray-700'}`}>
                        Sentiment:
                      </span>
                      <span className={`text-sm ${isDark ? 'text-gray-400' : 'text-gray-600'}`}>
                        {aiInsights.news_sentiment.sentiment}
                      </span>
                    </div>
                    {aiInsights.news_sentiment.key_themes && (
                      <div className="flex gap-2">
                        <span className={`text-sm font-medium ${isDark ? 'text-gray-300' : 'text-gray-700'}`}>
                          Themes:
                        </span>
                        <span className={`text-sm ${isDark ? 'text-gray-400' : 'text-gray-600'}`}>
                          {aiInsights.news_sentiment.key_themes.join(', ')}
                        </span>
                      </div>
                    )}
                  </div>
                </div>
              </div>
            )}

            {/* Headlines */}
            <div className="space-y-3">
              {news.headlines.map((article: any, index: number) => (
                <div key={index} className={`p-3 rounded-lg ${
                  isDark ? 'bg-[#2D3748]' : 'bg-gray-50'
                } border ${isDark ? 'border-gray-700' : 'border-gray-200'}`}>
                  <h4 className={`font-medium mb-1 ${isDark ? 'text-white' : 'text-[#0A1F44]'}`}>
                    {article.title}
                  </h4>
                  <div className="flex justify-between items-center">
                    <span className={`text-sm ${isDark ? 'text-gray-400' : 'text-gray-600'}`}>
                      {article.source}
                    </span>
                    <span className={`text-xs ${isDark ? 'text-gray-500' : 'text-gray-500'}`}>
                      {new Date(article.published_at).toLocaleDateString()}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* AI Cross-Signal Analysis */}
        {aiInsights?.status === 'available' && aiInsights.cross_signal_analysis && aiInsights.cross_signal_analysis.length > 0 && (
          <div className="p-6 rounded-2xl shadow-lg mb-6 bg-gradient-to-br from-purple-500/10 to-cyan-500/10 border border-purple-500/20">
            <div className="flex justify-between items-center mb-4">
              <h2 className={`text-xl font-semibold ${isDark ? 'text-white' : 'text-[#0A1F44]'}`}>
                AI Cross-Signal Analysis
              </h2>
              <span className="px-3 py-1 bg-purple-500 text-white text-sm font-medium rounded-full">
                AI-POWERED
              </span>
            </div>
            <div className="space-y-2">
              {aiInsights.cross_signal_analysis.map((insight: string, index: number) => (
                <div key={index} className={`flex items-start gap-2 p-3 rounded-lg ${
                  isDark ? 'bg-white/5' : 'bg-white/50'
                } border border-purple-500/20`}>
                  <span className="text-purple-500 font-bold">{index + 1}.</span>
                  <p className={`text-sm ${isDark ? 'text-gray-300' : 'text-gray-700'}`}>
                    {insight}
                  </p>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Summary Section */}
        <div className={`p-6 rounded-2xl shadow-lg mb-6 ${isDark ? 'bg-[#1a2f54]/80' : 'bg-white'}`}>
          <h2 className={`text-xl font-semibold mb-4 ${isDark ? 'text-white' : 'text-[#0A1F44]'}`}>
            Summary
          </h2>
          <p className={`mb-4 ${isDark ? 'text-gray-300' : 'text-gray-700'}`}>
            {report.summary}
          </p>
          <div className="flex flex-wrap gap-2">
            <span className={`text-xs px-2 py-1 rounded ${isDark ? 'bg-[#2D3748]' : 'bg-gray-100'}`}>
              yfinance
            </span>
            <span className={`text-xs px-2 py-1 rounded ${isDark ? 'bg-[#2D3748]' : 'bg-gray-100'}`}>
              NewsAPI
            </span>
            <span className={`text-xs px-2 py-1 rounded ${isDark ? 'bg-[#2D3748]' : 'bg-gray-100'}`}>
              Reddit
            </span>
            <span className={`text-xs px-2 py-1 rounded ${isDark ? 'bg-[#2D3748]' : 'bg-gray-100'}`}>
              Google Trends
            </span>
            <span className={`text-xs px-2 py-1 rounded ${isDark ? 'bg-[#2D3748]' : 'bg-gray-100'}`}>
              Fear & Greed
            </span>
            <span className="text-xs px-2 py-1 rounded bg-purple-500/20 text-purple-500">
              Gemini AI
            </span>
          </div>
        </div>

        {/* Disclaimer Footer */}
        <div className="p-6 rounded-2xl bg-red-500/10 border border-red-500/20">
          <h3 className="font-semibold mb-3 text-red-500">⚠️ Important Disclaimer</h3>
          <div className={`space-y-2 text-sm ${isDark ? 'text-gray-400' : 'text-gray-600'}`}>
            <p><strong>Educational Purpose Only:</strong> ResearchIQ is an educational research tool. This is NOT financial advice.</p>
            <p><strong>Data Limitations:</strong> Uses free public APIs with known constraints.</p>
            <p><strong>Not Suitable for Investment Decisions:</strong> Consult licensed financial professionals.</p>
          </div>
        </div>
      </div>
    </div>
  );
}
