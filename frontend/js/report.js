/**
 * ResearchIQ - Report Page JavaScript
 * Renders analysis data from backend
 */

// DOM Elements
const themeToggle = document.getElementById('themeToggle');
const sunIcon = document.getElementById('sunIcon');
const moonIcon = document.getElementById('moonIcon');

// State
let isDark = false;
let reportData = null;

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    initializeTheme();
    loadReportData();
});

// Theme Management
function initializeTheme() {
    const savedTheme = localStorage.getItem('theme');
    isDark = savedTheme === 'dark';

    if (isDark) {
        document.documentElement.classList.add('dark');
        sunIcon.classList.remove('hidden');
        moonIcon.classList.add('hidden');
    }

    themeToggle.addEventListener('click', toggleTheme);
}

function toggleTheme() {
    isDark = !isDark;

    if (isDark) {
        document.documentElement.classList.add('dark');
        sunIcon.classList.remove('hidden');
        moonIcon.classList.add('hidden');
        localStorage.setItem('theme', 'dark');
    } else {
        document.documentElement.classList.remove('dark');
        sunIcon.classList.add('hidden');
        moonIcon.classList.remove('hidden');
        localStorage.setItem('theme', 'light');
    }
}

// Load Report Data
function loadReportData() {
    const savedData = localStorage.getItem('reportData');

    if (!savedData) {
        alert('No report data found. Redirecting to homepage...');
        window.location.href = 'index.html';
        return;
    }

    try {
        reportData = JSON.parse(savedData);
        renderReport(reportData.report);
    } catch (error) {
        console.error('Error parsing report data:', error);
        alert('Error loading report. Please try again.');
        window.location.href = 'index.html';
    }
}

// Render Report
function renderReport(report) {
    if (!report) return;

    // Header
    renderHeader(report.metadata);

    // Technical Analysis
    renderTechnical(report.technical_analysis);

    // Sentiment Analysis
    renderSentiment(report.sentiment_analysis);

    // News Headlines
    renderNews(report.news_headlines);

    // AI Insights
    if (report.ai_insights && report.ai_insights.status === 'available') {
        renderAIInsights(report.ai_insights);
    }

    // Summary
    renderSummary(report.summary);
}

// Render Header
function renderHeader(metadata) {
    document.getElementById('assetName').textContent =
        `${metadata.company_name} (${metadata.ticker})`;

    document.getElementById('currentPrice').textContent =
        `$${metadata.current_price.toFixed(2)}`;

    const priceChangeEl = document.getElementById('priceChange');
    const change = metadata.price_change_percent;
    priceChangeEl.textContent = `${change >= 0 ? '+' : ''}${change.toFixed(2)}%`;
    priceChangeEl.style.color = change >= 0 ? '#10b981' : '#ef4444';

    document.getElementById('timestamp').textContent =
        `Last updated: ${metadata.timestamp}`;
}

// Render Technical Analysis
function renderTechnical(technical) {
    if (!technical || technical.confidence === 'UNAVAILABLE') {
        return;
    }

    // RSI - Using Figma Circular Gauge with Zones
    const rsi = technical.rsi;
    if (rsi) {
        const rsiGaugeContainer = document.getElementById('rsiGauge');
        const gauge = createRSIGauge(rsi.value);
        rsiGaugeContainer.innerHTML = '';
        rsiGaugeContainer.appendChild(gauge);
        // Note: rsiSignal is now part of the gauge component
    }

    // Moving Averages
    const ma = technical.moving_averages;
    if (ma && ma.values) {
        document.getElementById('ma20').textContent =
            ma.values.MA_20 ? `$${ma.values.MA_20.toFixed(2)}` : 'N/A';
        document.getElementById('ma50').textContent =
            ma.values.MA_50 ? `$${ma.values.MA_50.toFixed(2)}` : 'N/A';
        document.getElementById('ma200').textContent =
            ma.values.MA_200 ? `$${ma.values.MA_200.toFixed(2)}` : 'N/A';
    }

    // Volume
    if (technical.volume) {
        document.getElementById('volumeStatus').textContent = technical.volume.status;
    }

    // Overall Signal
    document.getElementById('technicalSignal').textContent =
        technical.overall_signal || 'neutral';
}

// Render Sentiment Analysis
function renderSentiment(sentiment) {
    if (!sentiment) return;

    // Fear & Greed Index - Using Figma Circular Gauge
    const marketSentiment = sentiment.market_sentiment;
    if (marketSentiment && marketSentiment.data && marketSentiment.data.value) {
        const fgValue = marketSentiment.data.value;
        const fgGaugeContainer = document.getElementById('fearGreedGauge');
        const gauge = createFearGreedGauge(fgValue);
        fgGaugeContainer.innerHTML = '';
        fgGaugeContainer.appendChild(gauge);
        // Note: fearGreedLabel is now part of the gauge component
    }

    // Google Trends
    const retailInterest = sentiment.retail_interest;
    if (retailInterest && retailInterest.data && retailInterest.data.interest_level) {
        document.getElementById('trendsLevel').textContent =
            retailInterest.data.interest_level;
    }

    // Reddit Mentions
    const socialSignals = sentiment.social_signals;
    if (socialSignals && socialSignals.data && socialSignals.data.total_mentions !== undefined) {
        document.getElementById('redditMentions').textContent =
            socialSignals.data.total_mentions;
        document.getElementById('redditBaseline').textContent =
            socialSignals.data.vs_baseline || 'average';
    }

    // Overall Sentiment
    const overallSentiment = sentiment.overall_sentiment;
    if (overallSentiment && overallSentiment.assessment) {
        document.getElementById('overallSentiment').textContent =
            overallSentiment.assessment;
    }
}

// Render News Headlines
function renderNews(news) {
    const newsContainer = document.getElementById('newsHeadlines');

    if (!news || news.status === 'limited' || !news.headlines || news.headlines.length === 0) {
        newsContainer.innerHTML = '<p class="text-sm text-muted">News data not available or limited by API constraints.</p>';
        return;
    }

    newsContainer.innerHTML = news.headlines.map(article => `
        <div class="p-3 rounded-lg" style="background-color: var(--secondary); border: 1px solid var(--border);">
            <h4 class="font-medium mb-1">${article.title}</h4>
            <div class="flex justify-between items-center">
                <span class="text-sm text-muted">${article.source}</span>
                <span class="text-xs text-muted">${formatDate(article.published_at)}</span>
            </div>
        </div>
    `).join('');
}

// Render AI Insights
function renderAIInsights(aiInsights) {
    // Technical Insight
    if (aiInsights.technical_insight) {
        const technicalInsightEl = document.getElementById('aiTechnicalInsight');
        document.getElementById('aiTechnicalText').textContent = aiInsights.technical_insight;
        technicalInsightEl.classList.remove('hidden');
    }

    // News Sentiment
    if (aiInsights.news_sentiment) {
        const newsSentiment = aiInsights.news_sentiment;
        const newsSentimentEl = document.getElementById('aiNewsSentiment');

        document.getElementById('aiNewsSentimentValue').textContent = newsSentiment.sentiment || '-';
        document.getElementById('aiNewsThemes').textContent =
            (newsSentiment.key_themes || []).join(', ') || '-';

        if (newsSentiment.notable_event) {
            document.getElementById('aiNewsEvent').textContent = newsSentiment.notable_event;
        }

        newsSentimentEl.classList.remove('hidden');
    }

    // Cross-Signal Analysis
    if (aiInsights.cross_signal_analysis && aiInsights.cross_signal_analysis.length > 0) {
        const crossSignalEl = document.getElementById('aiCrossSignal');
        const insightsContainer = document.getElementById('aiCrossSignalInsights');

        insightsContainer.innerHTML = aiInsights.cross_signal_analysis.map((insight, index) => `
            <div class="flex items-start gap-2 p-3 rounded-lg" style="background-color: rgba(255, 255, 255, 0.5); border: 1px solid rgba(139, 92, 246, 0.2);">
                <span class="text-accent font-bold">${index + 1}.</span>
                <p class="text-sm">${insight}</p>
            </div>
        `).join('');

        crossSignalEl.classList.remove('hidden');
    }
}

// Render Summary
function renderSummary(summary) {
    document.getElementById('summaryText').textContent = summary || 'No summary available.';
}

// Utility Functions
function formatDate(dateString) {
    if (!dateString) return 'Unknown';

    try {
        const date = new Date(dateString);
        const now = new Date();
        const diffMs = now - date;
        const diffHours = Math.floor(diffMs / (1000 * 60 * 60));
        const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24));

        if (diffHours < 24) {
            return `${diffHours}h ago`;
        } else if (diffDays < 7) {
            return `${diffDays}d ago`;
        } else {
            return date.toLocaleDateString();
        }
    } catch (error) {
        return dateString;
    }
}

// PDF Download (Placeholder)
function downloadPDF() {
    alert('PDF download feature coming soon! For now, you can use your browser\'s print function (Ctrl/Cmd + P) to save as PDF.');
    // Future: Call backend /generate-pdf endpoint
}
