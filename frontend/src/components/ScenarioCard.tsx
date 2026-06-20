'use client';

import { useState } from 'react';
import { Scenario } from '@/lib/types';
import { PlaybookView } from './PlaybookView';
import { getSeverityColor } from '@/lib/utils';

export function ScenarioCard({ scenario }: { scenario: Scenario }) {
  const [expanded, setExpanded] = useState(false);
  const severityColors = getSeverityColor(scenario.severity);

  return (
    <div className="bg-white rounded-xl shadow-sm border overflow-hidden">
      <div className="p-6">
        <div className="flex items-start justify-between mb-4">
          <div>
            <h3 className="text-lg font-semibold">{scenario.scenario_name}</h3>
            <span className="inline-block mt-1 text-xs bg-gray-100 text-gray-600 px-2 py-1 rounded">
              {scenario.scenario_type}
            </span>
          </div>
          <span className={`text-xs px-2 py-1 rounded font-medium ${severityColors}`}>
            {scenario.severity}
          </span>
        </div>

        <p className="text-gray-600 text-sm mb-4">{scenario.description}</p>

        {/* Probability bar */}
        <div className="mb-4">
          <div className="flex justify-between text-xs text-gray-500 mb-1">
            <span>Probability</span>
            <span>{Math.round((scenario.probability || 0) * 100)}%</span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div
              className="bg-indigo-600 h-2 rounded-full transition-all"
              style={{ width: `${(scenario.probability || 0) * 100}%` }}
            />
          </div>
        </div>

        {/* Details */}
        <div className="grid grid-cols-2 gap-4 text-sm">
          <div>
            <p className="text-gray-400 mb-1">Peak Time</p>
            <p className="font-medium">{scenario.peak_time_hours ?? 'N/A'} hours</p>
          </div>
          <div>
            <p className="text-gray-400 mb-1">Narratives</p>
            <div className="flex flex-wrap gap-1">
              {(scenario.key_narratives || [])
                .slice(0, 3)
                .map((n, i) => (
                  <span
                    key={i}
                    className="text-xs bg-purple-50 text-purple-700 px-2 py-0.5 rounded"
                  >
                    {n.length > 30 ? n.substring(0, 30) + '...' : n}
                  </span>
                ))}
            </div>
          </div>
        </div>

        {scenario.trigger_points && scenario.trigger_points.length > 0 && (
          <div className="mt-4">
            <p className="text-gray-400 text-sm mb-2">Trigger Points</p>
            <div className="flex flex-wrap gap-2">
              {scenario.trigger_points.map((trigger, i) => (
                <span
                  key={i}
                  className="text-xs bg-red-50 text-red-700 px-2 py-1 rounded"
                >
                  {trigger}
                </span>
              ))}
            </div>
          </div>
        )}

        {scenario.playbooks && scenario.playbooks.length > 0 && (
          <button
            onClick={() => setExpanded(!expanded)}
            className="mt-4 text-indigo-600 text-sm font-medium hover:text-indigo-700 transition"
          >
            {expanded ? '▼ Hide Playbook' : '▶ View Response Playbook'}
          </button>
        )}
      </div>

      {expanded && scenario.playbooks && scenario.playbooks.length > 0 && (
        <div className="border-t bg-gray-50 p-6">
          <PlaybookView playbook={scenario.playbooks[0]} />
        </div>
      )}
    </div>
  );
}
