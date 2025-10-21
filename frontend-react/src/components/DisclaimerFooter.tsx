import { AlertTriangle, Download } from "lucide-react";
import { Button } from "./ui/button";
import { Alert, AlertDescription } from "./ui/alert";

export function DisclaimerFooter() {
  const handleDownloadPDF = () => {
    alert("PDF download functionality would be implemented here");
  };

  return (
    <div className="space-y-4">
      {/* Disclaimer */}
      <Alert className="border-2 border-orange-500/30 bg-orange-50 dark:bg-orange-950/20 rounded-[0.625rem]">
        <AlertTriangle className="h-5 w-5 text-orange-600 dark:text-orange-400" />
        <AlertDescription className="ml-2">
          <strong className="text-orange-900 dark:text-orange-300">
            ⚠️ Educational Tool Only - Not Financial Advice
          </strong>
          <p className="mt-2 text-sm text-orange-800 dark:text-orange-400">
            This analysis is provided for educational and informational purposes only. 
            It should not be considered as financial, investment, or trading advice. 
            This is a portfolio project demonstrating data synthesis from various public APIs. 
            Always conduct your own research and consult with qualified financial advisors before making investment decisions.
          </p>
          <p className="mt-2 text-sm text-orange-800 dark:text-orange-400">
            Past performance does not guarantee future results. All investments carry risk, 
            including the potential loss of principal.
          </p>
        </AlertDescription>
      </Alert>

      {/* Download Button */}
      <div className="flex justify-center">
        <Button
          onClick={handleDownloadPDF}
          className="bg-[#00D9C0] hover:bg-[#00C0AA] text-gray-900 rounded-[0.625rem] gap-2 px-8 py-6 text-lg"
        >
          <Download className="h-5 w-5" />
          Download PDF Report
        </Button>
      </div>

      {/* Footer */}
      <div className="text-center text-sm text-gray-500 pt-4">
        <p>ResearchIQ - Investment Research Platform</p>
        <p className="mt-1">© 2025 Portfolio Project. For demonstration purposes only.</p>
      </div>
    </div>
  );
}
