import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";

export function GoogleTrendsChart() {
  // Mock 90-day Google Trends data
  const data = [
    { date: "Day 1", interest: 45 },
    { date: "Day 10", interest: 52 },
    { date: "Day 20", interest: 48 },
    { date: "Day 30", interest: 61 },
    { date: "Day 40", interest: 58 },
    { date: "Day 50", interest: 65 },
    { date: "Day 60", interest: 72 },
    { date: "Day 70", interest: 68 },
    { date: "Day 80", interest: 75 },
    { date: "Day 90", interest: 78 },
  ];

  return (
    <ResponsiveContainer width="100%" height={120}>
      <LineChart data={data}>
        <XAxis
          dataKey="date"
          tick={{ fontSize: 10 }}
          stroke="currentColor"
          className="text-gray-400"
          hide
        />
        <YAxis hide />
        <Tooltip
          contentStyle={{
            backgroundColor: "rgba(0, 0, 0, 0.8)",
            border: "none",
            borderRadius: "0.625rem",
            fontSize: "12px",
          }}
        />
        <Line
          type="monotone"
          dataKey="interest"
          stroke="#00D9C0"
          strokeWidth={2}
          dot={false}
          activeDot={{ r: 4 }}
        />
      </LineChart>
    </ResponsiveContainer>
  );
}
