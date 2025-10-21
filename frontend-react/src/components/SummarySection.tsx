import { Lightbulb, Database } from "lucide-react";
import { Card } from "./ui/card";

export function SummarySection() {
  const insights = [
    "Strong bullish technical indicators across all major moving averages (20, 50, and 200-day)",
    "RSI at 68.5 suggests approaching overbought territory but still within acceptable range",
    "Trading volume 27% above average indicates strong investor interest and participation",
    "Sentiment indicators show moderate greed (62/100) on Fear & Greed Index, suggesting positive market psychology",
    "Google Trends data shows increasing search interest over the past 90 days, correlating with price appreciation",
  ];

  const dataSources = [
    { name: "yfinance", description: "Price & Technical Data" },
    { name: "NewsAPI", description: "News Headlines" },
    { name: "Reddit API", description: "Social Sentiment" },
    { name: "Google Trends", description: "Search Interest" },
    { name: "Fear & Greed Index", description: "Market Sentiment" },
  ];

  return (
    <Card className="p-6 rounded-[0.625rem] border-gray-200 dark:border-gray-800 bg-white dark:bg-[oklch(0.12_0.02_240)] shadow-lg">
      {/* Key Insights */}
      <div className="mb-6">
        <h2 className="text-xl flex items-center gap-2 mb-4">
          <Lightbulb className="h-5 w-5 text-[#00D9C0]" />
          Key Insights
        </h2>
        <ul className="space-y-3">
          {insights.map((insight, index) => (
            <li key={index} className="flex items-start gap-3">
              <span className="text-[#00D9C0] mt-1">•</span>
              <span className="text-sm text-gray-700 dark:text-gray-300">
                {insight}
              </span>
            </li>
          ))}
        </ul>
      </div>

      {/* Data Sources */}
      <div>
        <h3 className="text-sm text-gray-500 flex items-center gap-2 mb-3">
          <Database className="h-4 w-4" />
          Data Sources
        </h3>
        <div className="flex flex-wrap gap-2">
          {dataSources.map((source, index) => (
            <div
              key={index}
              className="px-3 py-2 rounded-[0.625rem] bg-gray-100 dark:bg-[oklch(0.08_0.02_240)] border border-gray-200 dark:border-gray-700"
            >
              <div className="text-sm">{source.name}</div>
              <div className="text-xs text-gray-500">{source.description}</div>
            </div>
          ))}
        </div>
      </div>
    </Card>
  );
}
