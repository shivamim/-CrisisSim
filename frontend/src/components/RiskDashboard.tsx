'use client';

import { Simulation } from '@/lib/types';
import { SentimentChart } from './SentimentChart';
import { getRiskColor, getRiskLabel } from '@/lib/utils';

export function RiskDashboard({ simulation }: { simulation: Simulation }) {
  const riskScore = simulation.risk_score ?? 0;

  return (
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
      {/* Risk Score */}
      <div className="bg-white rounded-xl shadow-sm border p-6">
        <h3 className="text-sm font-medium text-gray-500 mb-4">Overall Risk Score</h3>
        <div className="flex items-center justify-center">
          <div className="relative w-40 h-40">
            <svg className="w-full h-full -rotate-90">
              <circle cx="80" cy="80" r="70" fill="none" stroke="#e5e7eb" strokeWidth="10" />
              <circle
                cx="80"
                cy="80"
                r="70"
                fill="none"
                stroke="currentColor"
                strokeWidth="10"
                strokeDasharray={`${(riskScore / 100) * 440} 440`}
                className={getRiskColor(riskScore)}
                strokeLinecap="round"
              />
            </svg>
            <div className="absolute inset-0 flex flex-col items-center justify-center">
              <span className={`text-4xl font-bold ${getRiskColor(riskScore)}`}>{riskScore}</span>
              <span className="text-xs text-gray-500">/ 100</span>
            </div>
          </div>
        </div>
        <p className={`text-center mt-4 font-medium ${getRiskColor(riskScore)}`}>
          {getRiskLabel(riskScore)}
        </p>
      </div>

      {/* Sentiment Chart */}
      <div className="bg-white rounded-xl shadow-sm border p-6 lg:col-span-2">
        <h3 className="text-sm font-medium text-gray-500 mb-4">Sentiment Trajectory</h3>
        <SentimentChart data={simulation.sentiment_trajectory || []} />
      </div>

      {/* Stats */}
      <div className="bg-white rounded-xl shadow-sm border p-6">
        <h3 className="text-sm font-medium text-gray-500 mb-4">Simulation Stats</h3>
        <div className="space-y-3">
          <div className="flex justify-between">
            <span className="text-gray-600">Agents Simulated</span>
            <span className="font-medium">{simulation.agent_count || 0}</span>
          </div>
          <div className="flex justify-between">
            <span className="text-gray-600">Scenarios Generated</span>
            <span className="font-medium">{simulation.scenarios?.length || 0}</span>
          </div>
          <div className="flex justify-between">
            <span className="text-gray-600">Parsed Claims</span>
            <span className="font-medium">{simulation.parsed_claims?.length || 0}</span>
          </div>
        </div>
      </div>

      {/* Parsed Claims */}
      {simulation.parsed_claims && simulation.parsed_claims.length > 0 && (
        <div className="bg-white rounded-xl shadow-sm border p-6 lg:col-span-2">
          <h3 className="text-sm font-medium text-gray-500 mb-4">Parsed Claims & Sensitivity</h3>
          <div className="space-y-3">
            {simulation.parsed_claims.map((claim, i) => (
              <div key={i} className="flex items-start gap-3">
                <div
                  className={`flex-shrink-0 w-2 h-2 rounded-full mt-2 ${
                    claim.sensitivity_score > 0.7
                      ? 'bg-red-500'
                      : claim.sensitivity_score > 0.4
                      ? 'bg-yellow-500'
                      : 'bg-green-500'
                  }`}
                />
                <div className="flex-1">
                  <p className="text-sm">{claim.claim}</p>
                  <p className="text-xs text-gray-400 mt-1">
                    Sensitivity: {Math.round((claim.sensitivity_score || 0) * 100)}%
                    {claim.controversy_potential && ` | ${claim.controversy_potential}`}
                  </p>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
