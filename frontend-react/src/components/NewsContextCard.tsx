import { Newspaper, ExternalLink } from "lucide-react";
import { Card } from "./ui/card";
import { Badge } from "./ui/badge";

export function NewsContextCard() {
  const newsData = [
    {
      headline: "Apple announces record-breaking iPhone sales in Q4, exceeding analyst expectations",
      source: "Bloomberg",
      timeAgo: "2 hours ago",
      url: "#",
    },
    {
      headline: "New M3 MacBook Pro production ramping up ahead of holiday season",
      source: "Reuters",
      timeAgo: "5 hours ago",
      url: "#",
    },
    {
      headline: "Apple Vision Pro pre-orders surge as developer interest grows significantly",
      source: "TechCrunch",
      timeAgo: "8 hours ago",
      url: "#",
    },
    {
      headline: "EU regulators approve Apple's latest App Store policy changes following negotiations",
      source: "Financial Times",
      timeAgo: "12 hours ago",
      url: "#",
    },
    {
      headline: "Apple expands services revenue with new subscription bundles in emerging markets",
      source: "WSJ",
      timeAgo: "1 day ago",
      url: "#",
    },
    {
      headline: "Analysts raise Apple price target citing strong services growth and ecosystem lock-in",
      source: "CNBC",
      timeAgo: "1 day ago",
      url: "#",
    },
    {
      headline: "Apple suppliers report increased orders for next-generation components",
      source: "Nikkei Asia",
      timeAgo: "2 days ago",
      url: "#",
    },
  ];

  return (
    <Card className="p-6 rounded-[0.625rem] border-gray-200 dark:border-gray-800 bg-white dark:bg-[oklch(0.12_0.02_240)] shadow-lg transition-all duration-300 hover:shadow-xl">
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-xl flex items-center gap-2">
          <Newspaper className="h-5 w-5 text-[#00D9C0]" />
          News Context
        </h2>
        <Badge className="bg-blue-500/10 text-blue-500 hover:bg-blue-500/20 border-blue-500/20">
          CONTEXT ONLY
        </Badge>
      </div>

      <div className="space-y-3">
        {newsData.map((news, index) => (
          <a
            key={index}
            href={news.url}
            className="block p-4 rounded-[0.625rem] bg-gray-50 dark:bg-[oklch(0.08_0.02_240)] hover:bg-gray-100 dark:hover:bg-[oklch(0.1_0.02_240)] transition-colors duration-200 group"
          >
            <div className="flex items-start justify-between gap-3">
              <div className="flex-1">
                <h3 className="line-clamp-2 mb-2 group-hover:text-[#00D9C0] transition-colors">
                  {news.headline}
                </h3>
                <div className="flex items-center gap-3 text-sm text-gray-500">
                  <span>{news.source}</span>
                  <span>•</span>
                  <span>{news.timeAgo}</span>
                </div>
              </div>
              <ExternalLink className="h-4 w-4 text-gray-400 group-hover:text-[#00D9C0] transition-colors flex-shrink-0 mt-1" />
            </div>
          </a>
        ))}
      </div>

      <div className="mt-4 p-3 rounded-[0.625rem] bg-blue-50 dark:bg-blue-950/20 border border-blue-200 dark:border-blue-900/30">
        <p className="text-sm text-blue-700 dark:text-blue-400">
          <strong>Note:</strong> Limited to recent headlines from NewsAPI. News sentiment is not factored into technical analysis.
        </p>
      </div>
    </Card>
  );
}
