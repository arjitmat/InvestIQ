/**
 * ResearchIQ - Homepage JavaScript
 * Handles theme toggle, asset selection, and analysis requests
 */

// Configuration
const API_BASE_URL = 'http://localhost:8000';

// Asset suggestions by type
const ASSET_HINTS = {
    stocks: 'Popular: AAPL, MSFT, GOOGL, AMZN, TSLA, NVDA',
    crypto: 'Popular: BTC-USD, ETH-USD, SOL-USD, BNB-USD',
    indices: 'Popular: ^GSPC (S&P 500), ^IXIC (Nasdaq), ^DJI (Dow)',
    commodities: 'Use exact symbols: GC=F (Gold), SI=F (Silver)'
};

// DOM Elements
const themeToggle = document.getElementById('themeToggle');
const sunIcon = document.getElementById('sunIcon');
const moonIcon = document.getElementById('moonIcon');
const assetTypeTabs = document.querySelectorAll('.tab[data-type]');
const tickerInput = document.getElementById('tickerInput');
const tickerHint = document.getElementById('tickerHint');
const analyzeBtn = document.getElementById('analyzeBtn');
const loadingState = document.getElementById('loadingState');
const progressBar = document.getElementById('progressBar');
const loadingMessage = document.getElementById('loadingMessage');
const errorState = document.getElementById('errorState');
const errorMessage = document.getElementById('errorMessage');

// State
let currentAssetType = 'stocks';
let isDark = false;
let animatedBg = null;

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    initializeTheme();
    setupEventListeners();
    initializeAnimatedBackground();
});

// Theme Management
function initializeTheme() {
    // Check for saved theme preference or default to light
    const savedTheme = localStorage.getItem('theme');
    isDark = savedTheme === 'dark';

    if (isDark) {
        document.documentElement.classList.add('dark');
        sunIcon.classList.remove('hidden');
        moonIcon.classList.add('hidden');
    }
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

    // Update animated background theme
    if (animatedBg) {
        animatedBg.setTheme(isDark);
    }
}

// Animated Background Initialization
function initializeAnimatedBackground() {
    const bgContainer = document.getElementById('animated-bg');
    if (bgContainer && window.AnimatedBackground) {
        animatedBg = new AnimatedBackground(bgContainer, isDark);
    }
}

// Event Listeners
function setupEventListeners() {
    // Theme toggle
    themeToggle.addEventListener('click', toggleTheme);

    // Asset type tabs
    assetTypeTabs.forEach(tab => {
        tab.addEventListener('click', () => handleAssetTypeChange(tab));
    });

    // Ticker input - Enter key to analyze
    tickerInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            analyzeAsset();
        }
    });

    // Ticker input - Clear error on typing
    tickerInput.addEventListener('input', () => {
        hideError();
    });

    // Analyze button
    analyzeBtn.addEventListener('click', analyzeAsset);
}

// Asset Type Selection
function handleAssetTypeChange(selectedTab) {
    // Update active state
    assetTypeTabs.forEach(tab => tab.classList.remove('active'));
    selectedTab.classList.add('active');

    // Update current asset type
    currentAssetType = selectedTab.dataset.type;

    // Update hint text
    tickerHint.textContent = ASSET_HINTS[currentAssetType];

    // Clear input and error
    tickerInput.value = '';
    hideError();
}

// Analysis
async function analyzeAsset() {
    const ticker = tickerInput.value.trim().toUpperCase();

    // Validation
    if (!ticker) {
        showError('Please enter a ticker symbol');
        return;
    }

    // Show loading state
    showLoading();

    try {
        // Simulate progress for better UX
        startProgressSimulation();

        // Call backend API
        const response = await fetch(`${API_BASE_URL}/analyze`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                ticker: ticker,
                asset_type: currentAssetType
            })
        });

        // Stop progress simulation
        stopProgressSimulation();

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Analysis failed');
        }

        const data = await response.json();

        // Complete progress
        setProgress(100);

        // Wait a moment to show completion
        await new Promise(resolve => setTimeout(resolve, 500));

        // Save data and redirect to report page
        localStorage.setItem('reportData', JSON.stringify(data));
        window.location.href = 'report.html';

    } catch (error) {
        console.error('Analysis error:', error);
        hideLoading();
        showError(error.message || 'Failed to analyze asset. Please try again.');
    }
}

// Loading States
let progressInterval;

function showLoading() {
    hideError();
    analyzeBtn.disabled = true;
    analyzeBtn.style.opacity = '0.5';
    loadingState.classList.remove('hidden');
    setProgress(0);
}

function hideLoading() {
    analyzeBtn.disabled = false;
    analyzeBtn.style.opacity = '1';
    loadingState.classList.add('hidden');
    setProgress(0);
}

function startProgressSimulation() {
    let progress = 0;
    const messages = [
        'Collecting data from 5 sources...',
        'Analyzing technical indicators...',
        'Processing sentiment data...',
        'Generating AI insights...',
        'Compiling report...'
    ];
    let messageIndex = 0;

    progressInterval = setInterval(() => {
        progress += Math.random() * 15;
        if (progress > 90) progress = 90; // Cap at 90% until real completion

        setProgress(progress);

        // Update message every 20% progress
        const newMessageIndex = Math.floor(progress / 20);
        if (newMessageIndex !== messageIndex && newMessageIndex < messages.length) {
            messageIndex = newMessageIndex;
            loadingMessage.textContent = messages[messageIndex];
        }
    }, 800);
}

function stopProgressSimulation() {
    if (progressInterval) {
        clearInterval(progressInterval);
        progressInterval = null;
    }
}

function setProgress(value) {
    progressBar.style.width = `${value}%`;
}

// Error Handling
function showError(message) {
    errorMessage.textContent = message;
    errorState.classList.remove('hidden');
}

function hideError() {
    errorState.classList.add('hidden');
}
