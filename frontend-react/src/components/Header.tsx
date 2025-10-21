import { TrendingUp, RefreshCw } from "lucide-react";
import { Button } from "./ui/button";

export function Header() {
  const assetData = {
    name: "Apple Inc.",
    ticker: "AAPL",
    price: 178.45,
    change: 2.34,
    changePercent: 1.33,
    lastUpdated: "2 minutes ago",
  };

  const isPositive = assetData.change >= 0;

  return (
    <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
      <div>
        <div className="flex items-center gap-3">
          <div className="p-2 rounded-[0.625rem] bg-[oklch(0.95_0.01_180)] dark:bg-[oklch(0.15_0.02_240)]">
            <TrendingUp className="h-6 w-6 text-[#00D9C0]" />
          </div>
          <div>
            <h1 className="text-2xl sm:text-3xl">
              {assetData.name}{" "}
              <span className="text-gray-500">({assetData.ticker})</span>
            </h1>
          </div>
        </div>

        <div className="mt-3 flex items-baseline gap-3">
          <span className="text-3xl sm:text-4xl">${assetData.price}</span>
          <span
            className={`text-lg ${
              isPositive ? "text-green-500" : "text-red-500"
            }`}
          >
            {isPositive ? "+" : ""}
            {assetData.change} ({isPositive ? "+" : ""}
            {assetData.changePercent}%)
          </span>
        </div>

        <p className="mt-2 text-sm text-gray-500">
          Last updated {assetData.lastUpdated}
        </p>
      </div>

      <div>
        <Button className="bg-[#00D9C0] hover:bg-[#00C0AA] text-gray-900 rounded-[0.625rem] gap-2">
          <RefreshCw className="h-4 w-4" />
          Analyze Another Asset
        </Button>
      </div>
    </div>
  );
}
