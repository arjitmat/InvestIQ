export function RSIGauge({ value }: { value: number }) {
  const radius = 70;
  const strokeWidth = 12;
  const center = 90;
  const circumference = 2 * Math.PI * radius;
  const progress = (value / 100) * circumference;

  // Determine color based on RSI value
  const getColor = () => {
    if (value <= 30) return "#22c55e"; // green - oversold
    if (value >= 70) return "#ef4444"; // red - overbought
    return "#6b7280"; // gray - neutral
  };

  const getZoneLabel = () => {
    if (value <= 30) return "Oversold";
    if (value >= 70) return "Overbought";
    return "Neutral";
  };

  return (
    <div className="flex flex-col items-center">
      <div className="relative">
        <svg width="180" height="180" className="transform -rotate-90">
          {/* Background circle */}
          <circle
            cx={center}
            cy={center}
            r={radius}
            fill="none"
            stroke="currentColor"
            strokeWidth={strokeWidth}
            className="text-gray-200 dark:text-gray-700"
          />
          {/* Oversold zone (0-30) - green */}
          <circle
            cx={center}
            cy={center}
            r={radius}
            fill="none"
            stroke="#22c55e"
            strokeWidth={strokeWidth}
            strokeDasharray={`${circumference * 0.3} ${circumference * 0.7}`}
            strokeDashoffset={0}
            opacity={0.3}
          />
          {/* Overbought zone (70-100) - red */}
          <circle
            cx={center}
            cy={center}
            r={radius}
            fill="none"
            stroke="#ef4444"
            strokeWidth={strokeWidth}
            strokeDasharray={`${circumference * 0.3} ${circumference * 0.7}`}
            strokeDashoffset={-circumference * 0.7}
            opacity={0.3}
          />
          {/* Progress circle */}
          <circle
            cx={center}
            cy={center}
            r={radius}
            fill="none"
            stroke={getColor()}
            strokeWidth={strokeWidth}
            strokeDasharray={`${progress} ${circumference - progress}`}
            strokeLinecap="round"
            className="transition-all duration-500"
          />
        </svg>
        <div className="absolute inset-0 flex flex-col items-center justify-center">
          <span className="text-3xl">{value.toFixed(1)}</span>
          <span className="text-xs text-gray-500 dark:text-gray-400 mt-1">RSI</span>
        </div>
      </div>
      <div className="mt-3 text-center">
        <span
          className={`text-sm ${
            value <= 30
              ? "text-green-500"
              : value >= 70
              ? "text-red-500"
              : "text-gray-500 dark:text-gray-400"
          }`}
        >
          {getZoneLabel()}
        </span>
      </div>
      <div className="mt-2 flex gap-3 text-xs text-gray-500 dark:text-gray-400">
        <div className="flex items-center gap-1">
          <div className="w-3 h-3 rounded-full bg-green-500/30"></div>
          <span>0-30: Oversold</span>
        </div>
        <div className="flex items-center gap-1">
          <div className="w-3 h-3 rounded-full bg-gray-500/30"></div>
          <span>30-70: Neutral</span>
        </div>
        <div className="flex items-center gap-1">
          <div className="w-3 h-3 rounded-full bg-red-500/30"></div>
          <span>70-100: Overbought</span>
        </div>
      </div>
    </div>
  );
}
