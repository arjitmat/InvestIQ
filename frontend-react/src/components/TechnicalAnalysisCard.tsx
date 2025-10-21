import { TrendingUp, TrendingDown, Activity } from "lucide-react";
import { Card } from "./ui/card";
import { Badge } from "./ui/badge";
import { Progress } from "./ui/progress";
import { RSIGauge } from "./RSIGauge";

export function TechnicalAnalysisCard() {
  const technicalData = {
    rsi: 68.5,
    movingAverages: [
      {
        period: "20-day MA",
        price: 175.23,
        current: 178.45,
        trend: "up",
        signal: "Bullish",
      },
      {
        period: "50-day MA",
        price: 172.89,
        current: 178.45,
        trend: "up",
        signal: "Bullish",
      },
      {
        period: "200-day MA",
        price: 168.45,
        current: 178.45,
        trend: "up",
        signal: "Bullish",
      },
    ],
    volume: {
      current: 82500000,
      average: 65000000,
      percentage: 127,
    },
    overallSignal: "Bullish",
  };

  return (
    <Card className="p-6 rounded-[0.625rem] border-gray-200 dark:border-gray-800 bg-white dark:bg-[oklch(0.12_0.02_240)] shadow-lg transition-all duration-300 hover:shadow-xl">
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-xl flex items-center gap-2">
          <Activity className="h-5 w-5 text-[#00D9C0]" />
          Technical Analysis
        </h2>
        <Badge className="bg-green-500/10 text-green-500 hover:bg-green-500/20 border-green-500/20">
          HIGH CONFIDENCE
        </Badge>
      </div>

      {/* RSI Gauge */}
      <div className="mb-6">
        <RSIGauge value={technicalData.rsi} />
      </div>

      {/* Moving Averages */}
      <div className="mb-6">
        <h3 className="text-sm text-gray-500 mb-3">Moving Averages</h3>
        <div className="space-y-3">
          {technicalData.movingAverages.map((ma, index) => (
            <div
              key={index}
              className="flex items-center justify-between p-3 rounded-[0.625rem] bg-gray-50 dark:bg-[oklch(0.08_0.02_240)]"
            >
              <div className="flex items-center gap-3">
                <span className="text-sm">{ma.period}</span>
                <span className="text-xs text-gray-500">${ma.price}</span>
              </div>
              <div className="flex items-center gap-2">
                {ma.trend === "up" ? (
                  <TrendingUp className="h-4 w-4 text-green-500" />
                ) : (
                  <TrendingDown className="h-4 w-4 text-red-500" />
                )}
                <span
                  className={`text-sm ${
                    ma.signal === "Bullish" ? "text-green-500" : "text-red-500"
                  }`}
                >
                  {ma.signal}
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Volume Analysis */}
      <div className="mb-6">
        <h3 className="text-sm text-gray-500 mb-3">Volume Analysis</h3>
        <div className="p-3 rounded-[0.625rem] bg-gray-50 dark:bg-[oklch(0.08_0.02_240)]">
          <div className="flex justify-between mb-2">
            <span className="text-sm">Current Volume</span>
            <span className="text-sm">
              {(technicalData.volume.current / 1000000).toFixed(1)}M
            </span>
          </div>
          <Progress value={technicalData.volume.percentage} className="h-2" />
          <div className="flex justify-between mt-2">
            <span className="text-xs text-gray-500">
              Avg: {(technicalData.volume.average / 1000000).toFixed(1)}M
            </span>
            <span className="text-xs text-green-500">
              +{technicalData.volume.percentage - 100}% above average
            </span>
          </div>
        </div>
      </div>

      {/* Overall Signal */}
      <div className="flex justify-center">
        <Badge
          className={`text-lg px-6 py-2 ${
            technicalData.overallSignal === "Bullish"
              ? "bg-green-500 hover:bg-green-600 text-white"
              : technicalData.overallSignal === "Bearish"
              ? "bg-red-500 hover:bg-red-600 text-white"
              : "bg-gray-500 hover:bg-gray-600 text-white"
          }`}
        >
          Overall Signal: {technicalData.overallSignal}
        </Badge>
      </div>
    </Card>
  );
}
