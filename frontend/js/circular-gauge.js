/**
 * ResearchIQ - Circular Gauge Component (Figma Design)
 * Matches exact Figma specifications with zone indicators
 */

/**
 * Create RSI gauge with zone indicators (Figma design)
 */
function createRSIGauge(value) {
    const container = document.createElement('div');
    container.className = 'flex flex-col items-center';

    const radius = 70;
    const strokeWidth = 12;
    const center = 90;
    const circumference = 2 * Math.PI * radius;
    const progress = (value / 100) * circumference;

    // Determine color and zone
    let color, zoneLabel, zoneColor;
    if (value <= 30) {
        color = '#22c55e'; // green - oversold
        zoneLabel = 'Oversold';
        zoneColor = 'text-green-500';
    } else if (value >= 70) {
        color = '#ef4444'; // red - overbought
        zoneLabel = 'Overbought';
        zoneColor = 'text-red-500';
    } else {
        color = '#6b7280'; // gray - neutral
        zoneLabel = 'Neutral';
        zoneColor = 'text-gray-500';
    }

    container.innerHTML = `
        <div class="relative">
            <svg width="180" height="180" class="transform -rotate-90">
                <!-- Background circle -->
                <circle
                    cx="${center}"
                    cy="${center}"
                    r="${radius}"
                    fill="none"
                    stroke="currentColor"
                    stroke-width="${strokeWidth}"
                    class="text-gray-200 dark:text-gray-700"
                />
                <!-- Oversold zone (0-30) - green background -->
                <circle
                    cx="${center}"
                    cy="${center}"
                    r="${radius}"
                    fill="none"
                    stroke="#22c55e"
                    stroke-width="${strokeWidth}"
                    stroke-dasharray="${circumference * 0.3} ${circumference * 0.7}"
                    stroke-dashoffset="0"
                    opacity="0.3"
                />
                <!-- Overbought zone (70-100) - red background -->
                <circle
                    cx="${center}"
                    cy="${center}"
                    r="${radius}"
                    fill="none"
                    stroke="#ef4444"
                    stroke-width="${strokeWidth}"
                    stroke-dasharray="${circumference * 0.3} ${circumference * 0.7}"
                    stroke-dashoffset="${-circumference * 0.7}"
                    opacity="0.3"
                />
                <!-- Progress circle -->
                <circle
                    cx="${center}"
                    cy="${center}"
                    r="${radius}"
                    fill="none"
                    stroke="${color}"
                    stroke-width="${strokeWidth}"
                    stroke-dasharray="${progress} ${circumference - progress}"
                    stroke-linecap="round"
                    class="transition-all duration-500"
                />
            </svg>
            <div class="absolute inset-0 flex flex-col items-center justify-center">
                <span class="text-3xl font-bold">${value.toFixed(1)}</span>
                <span class="text-xs text-gray-500 mt-1">RSI</span>
            </div>
        </div>
        <div class="mt-3 text-center">
            <span class="text-sm ${zoneColor}">${zoneLabel}</span>
        </div>
        <div class="mt-2 flex gap-3 text-xs text-gray-500">
            <div class="flex items-center gap-1">
                <div class="w-3 h-3 rounded-full bg-green-500/30"></div>
                <span>0-30: Oversold</span>
            </div>
            <div class="flex items-center gap-1">
                <div class="w-3 h-3 rounded-full bg-gray-500/30"></div>
                <span>30-70: Neutral</span>
            </div>
            <div class="flex items-center gap-1">
                <div class="w-3 h-3 rounded-full bg-red-500/30"></div>
                <span>70-100: Overbought</span>
            </div>
        </div>
    `;

    return container;
}

/**
 * Create Fear & Greed gauge (Figma design)
 */
function createFearGreedGauge(value) {
    const container = document.createElement('div');
    container.className = 'flex flex-col items-center';

    const radius = 70;
    const strokeWidth = 12;
    const center = 90;
    const circumference = 2 * Math.PI * radius;
    const progress = (value / 100) * circumference;

    // Determine color and label
    let color, label;
    if (value >= 75) {
        color = '#22c55e'; // Extreme Greed - green
        label = 'Extreme Greed';
    } else if (value >= 55) {
        color = '#84cc16'; // Greed - light green
        label = 'Greed';
    } else if (value >= 45) {
        color = '#f59e0b'; // Neutral - yellow
        label = 'Neutral';
    } else if (value >= 25) {
        color = '#f97316'; // Fear - orange
        label = 'Fear';
    } else {
        color = '#ef4444'; // Extreme Fear - red
        label = 'Extreme Fear';
    }

    container.innerHTML = `
        <div class="relative">
            <svg width="180" height="180" class="transform -rotate-90">
                <!-- Background circle -->
                <circle
                    cx="${center}"
                    cy="${center}"
                    r="${radius}"
                    fill="none"
                    stroke="currentColor"
                    stroke-width="${strokeWidth}"
                    class="text-gray-200 dark:text-gray-700"
                />
                <!-- Progress circle -->
                <circle
                    cx="${center}"
                    cy="${center}"
                    r="${radius}"
                    fill="none"
                    stroke="${color}"
                    stroke-width="${strokeWidth}"
                    stroke-dasharray="${progress} ${circumference - progress}"
                    stroke-linecap="round"
                    class="transition-all duration-500"
                />
            </svg>
            <div class="absolute inset-0 flex flex-col items-center justify-center">
                <span class="text-3xl font-bold">${value}</span>
                <span class="text-xs text-gray-500 mt-1">Fear & Greed</span>
            </div>
        </div>
        <div class="mt-3 text-center">
            <span class="text-sm" style="color: ${color}">${label}</span>
        </div>
    `;

    return container;
}

/**
 * Update an existing circular gauge
 * @param {HTMLElement} container - Gauge container element
 * @param {number} newValue - New value (0-100)
 */
function updateCircularGauge(container, newValue) {
    const valueElement = container.querySelector('.circular-gauge-value');
    const circle = container.querySelector('.circular-gauge-fill');

    if (!valueElement || !circle) return;

    const radius = 70;
    const circumference = 2 * Math.PI * radius;
    const offset = circumference - (newValue / 100) * circumference;

    // Animate value change
    valueElement.textContent = Math.round(newValue);
    circle.style.strokeDashoffset = offset;
}
