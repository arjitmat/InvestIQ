export function FearGreedGauge({ value }: { value: number }) {
  const getLabel = () => {
    if (value <= 25) return "Extreme Fear";
    if (value <= 45) return "Fear";
    if (value <= 55) return "Neutral";
    if (value <= 75) return "Greed";
    return "Extreme Greed";
  };

  const getColor = () => {
    if (value <= 25) return "#ef4444"; // red
    if (value <= 45) return "#f97316"; // orange
    if (value <= 55) return "#6b7280"; // gray
    if (value <= 75) return "#84cc16"; // light green
    return "#22c55e"; // green
  };

  // SVG dimensions
  const radius = 100;
  const strokeWidth = 20;
  const centerX = 140;
  const centerY = 140;

  // Segments: [start%, end%] for each zone
  const segments = [
    { start: 0, end: 25, color: "#ef4444" }, // Extreme Fear
    { start: 25, end: 45, color: "#f97316" }, // Fear
    { start: 45, end: 55, color: "#6b7280" }, // Neutral
    { start: 55, end: 75, color: "#84cc16" }, // Greed
    { start: 75, end: 100, color: "#22c55e" }, // Extreme Greed
  ];

  // Calculate rotation angle (0 at left, 180 at right)
  const needleRotation = -90 + (value / 100) * 180;

  return (
    <div className="flex flex-col items-center">
      <h3 className="text-sm text-gray-500 dark:text-gray-400 mb-4">Fear & Greed Index</h3>
      <div className="relative w-[280px] h-[180px]">
        <svg width="280" height="140" viewBox="0 0 280 140" className="overflow-visible">
          {/* Background arc */}
          <path
            d={`M ${centerX - radius} ${centerY} A ${radius} ${radius} 0 0 1 ${centerX + radius} ${centerY}`}
            fill="none"
            stroke="currentColor"
            strokeWidth={strokeWidth}
            strokeLinecap="round"
            className="text-gray-200 dark:text-gray-700"
          />

          {/* Colored segments */}
          {segments.map((segment, index) => {
            const startAngle = -180 + (segment.start / 100) * 180;
            const endAngle = -180 + (segment.end / 100) * 180;
            const largeArcFlag = (segment.end - segment.start) > 50 ? 1 : 0;

            const startX = centerX + radius * Math.cos((startAngle * Math.PI) / 180);
            const startY = centerY + radius * Math.sin((startAngle * Math.PI) / 180);
            const endX = centerX + radius * Math.cos((endAngle * Math.PI) / 180);
            const endY = centerY + radius * Math.sin((endAngle * Math.PI) / 180);

            return (
              <path
                key={index}
                d={`M ${startX} ${startY} A ${radius} ${radius} 0 ${largeArcFlag} 1 ${endX} ${endY}`}
                fill="none"
                stroke={segment.color}
                strokeWidth={strokeWidth}
                strokeLinecap="round"
                opacity="0.4"
              />
            );
          })}

          {/* Needle */}
          <g transform={`rotate(${needleRotation} ${centerX} ${centerY})`}>
            <line
              x1={centerX}
              y1={centerY}
              x2={centerX}
              y2={centerY - radius + 10}
              stroke={getColor()}
              strokeWidth="3"
              strokeLinecap="round"
            />
            <circle cx={centerX} cy={centerY} r="8" fill={getColor()} />
          </g>
        </svg>

        <div className="absolute left-1/2 -translate-x-1/2 flex flex-col items-center" style={{ top: '70px' }}>
          <span className="text-4xl">{value}</span>
          <span className="text-sm text-gray-500 dark:text-gray-400 mt-1">out of 100</span>
        </div>
      </div>

      <div className="mt-1">
        <span
          className="text-lg"
          style={{ color: getColor() }}
        >
          {getLabel()}
        </span>
      </div>

      <div className="mt-3 flex flex-wrap justify-center gap-2 text-xs text-gray-500 dark:text-gray-400">
        <div className="flex items-center gap-1">
          <div className="w-3 h-3 rounded-full bg-red-500/40"></div>
          <span>0-25</span>
        </div>
        <div className="flex items-center gap-1">
          <div className="w-3 h-3 rounded-full bg-orange-500/40"></div>
          <span>25-45</span>
        </div>
        <div className="flex items-center gap-1">
          <div className="w-3 h-3 rounded-full bg-gray-500/40"></div>
          <span>45-55</span>
        </div>
        <div className="flex items-center gap-1">
          <div className="w-3 h-3 rounded-full bg-lime-500/40"></div>
          <span>55-75</span>
        </div>
        <div className="flex items-center gap-1">
          <div className="w-3 h-3 rounded-full bg-green-500/40"></div>
          <span>75-100</span>
        </div>
      </div>
    </div>
  );
}
