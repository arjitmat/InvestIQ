import { Heart, TrendingUp, MessageSquare } from "lucide-react";
import { Card } from "./ui/card";
import { Badge } from "./ui/badge";
import { FearGreedGauge } from "./FearGreedGauge";
import { GoogleTrendsChart } from "./GoogleTrendsChart";

export function SentimentAnalysisCard() {
  const sentimentData = {
    fearGreedIndex: 62,
    redditMentions: {
      count: 1243,
      level: "High",
    },
    aggregatedScore: 45,
  };

  return (
    <Card className="p-6 rounded-[0.625rem] border-gray-200 dark:border-gray-800 bg-white dark:bg-[oklch(0.12_0.02_240)] shadow-lg transition-all duration-300 hover:shadow-xl">
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-xl flex items-center gap-2">
          <Heart className="h-5 w-5 text-[#00D9C0]" />
          Sentiment Analysis
        </h2>
        <Badge className="bg-yellow-500/10 text-yellow-500 hover:bg-yellow-500/20 border-yellow-500/20">
          MEDIUM CONFIDENCE
        </Badge>
      </div>

      {/* Fear & Greed Gauge */}
      <div className="mb-6">
        <FearGreedGauge value={sentimentData.fearGreedIndex} />
      </div>

      {/* Google Trends */}
      <div className="mb-6">
        <h3 className="text-sm text-gray-500 mb-3 flex items-center gap-2">
          <TrendingUp className="h-4 w-4" />
          Google Trends (90-day)
        </h3>
        <div className="p-3 rounded-[0.625rem] bg-gray-50 dark:bg-[oklch(0.08_0.02_240)]">
          <GoogleTrendsChart />
        </div>
      </div>

      {/* Reddit Mentions */}
      <div className="mb-6">
        <h3 className="text-sm text-gray-500 mb-3 flex items-center gap-2">
          <MessageSquare className="h-4 w-4" />
          Reddit Mentions
        </h3>
        <div className="flex items-center justify-between p-3 rounded-[0.625rem] bg-gray-50 dark:bg-[oklch(0.08_0.02_240)]">
          <div className="flex items-center gap-3">
            <div className="p-2 rounded-full bg-orange-500/10">
              <MessageSquare className="h-5 w-5 text-orange-500" />
            </div>
            <div>
              <div className="text-lg">{sentimentData.redditMentions.count}</div>
              <div className="text-xs text-gray-500">mentions this week</div>
            </div>
          </div>
          <Badge className="bg-orange-500/10 text-orange-500 hover:bg-orange-500/20 border-orange-500/20">
            {sentimentData.redditMentions.level} Volume
          </Badge>
        </div>
      </div>

      {/* Aggregated Sentiment Score */}
      <div>
        <h3 className="text-sm text-gray-500 mb-3">Aggregated Sentiment Score</h3>
        <div className="p-4 rounded-[0.625rem] bg-gray-50 dark:bg-[oklch(0.08_0.02_240)]">
          <div className="flex items-center justify-between mb-2">
            <span className="text-xs text-gray-500">Negative</span>
            <span className="text-xs text-gray-500">Positive</span>
          </div>
          <div className="relative h-3 bg-gradient-to-r from-red-500 via-gray-400 to-green-500 rounded-full overflow-hidden">
            <div
              className="absolute top-0 h-full w-1 bg-white dark:bg-gray-900 shadow-lg transition-all duration-500"
              style={{
                left: `${((sentimentData.aggregatedScore + 100) / 200) * 100}%`,
              }}
            ></div>
          </div>
          <div className="text-center mt-3">
            <span className="text-2xl">{sentimentData.aggregatedScore > 0 ? '+' : ''}{sentimentData.aggregatedScore}</span>
            <span className="text-sm text-gray-500 ml-2">/ 100</span>
          </div>
        </div>
      </div>
    </Card>
  );
}
