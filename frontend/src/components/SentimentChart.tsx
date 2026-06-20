'use client';

import {
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip,
  ResponsiveContainer, ReferenceLine,
} from 'recharts';
import { SentimentPoint } from '@/lib/types';

export function SentimentChart({ data }: { data: SentimentPoint[] }) {
  if (!data || data.length === 0) {
    return (
      <div className="flex items-center justify-center h-64 text-gray-400">
        No sentiment data available
      </div>
    );
  }

  return (
    <ResponsiveContainer width="100%" height={250}>
      <LineChart data={data} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
        <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
        <XAxis dataKey="phase" stroke="#9ca3af" />
        <YAxis domain={[-10, 10]} stroke="#9ca3af" />
        <Tooltip
          contentStyle={{ borderRadius: '8px', border: '1px solid #e5e7eb' }}
          formatter={(value: number) => [value.toFixed(2), 'Sentiment']}
        />
        <ReferenceLine y={0} stroke="#d1d5db" strokeDasharray="3 3" />
        <Line
          type="monotone"
          dataKey="avg_sentiment"
          stroke="#6366f1"
          strokeWidth={2}
          dot={{ fill: '#6366f1', r: 4 }}
          activeDot={{ r: 6 }}
        />
      </LineChart>
    </ResponsiveContainer>
  );
}
