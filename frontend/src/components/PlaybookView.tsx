'use client';

import { Playbook } from '@/lib/types';

export function PlaybookView({ playbook }: { playbook: Playbook }) {
  return (
    <div className="space-y-6">
      {/* Strategy Summary */}
      <div>
        <h4 className="text-sm font-medium text-gray-500 mb-2">Strategy Summary</h4>
        <p className="text-sm text-gray-700">{playbook.strategy_summary}</p>
      </div>

      {/* Response Timeline */}
      {playbook.response_timeline && playbook.response_timeline.length > 0 && (
        <div>
          <h4 className="text-sm font-medium text-gray-500 mb-3">Response Timeline</h4>
          <div className="space-y-4">
            {playbook.response_timeline.map((item, i) => (
              <div key={i} className="border-l-2 border-indigo-200 pl-4 relative">
                <div className="absolute -left-1.5 top-1 w-3 h-3 rounded-full bg-indigo-500" />
                <p className="text-sm font-medium text-indigo-900">{item.time}</p>
                {item.actions &&
                  item.actions.map((action, j) => (
                    <p key={j} className="text-sm text-gray-600 mt-1">
                      • {action}
                    </p>
                  ))}
                {item.channels && item.channels.length > 0 && (
                  <div className="flex gap-1 mt-2 flex-wrap">
                    {item.channels.map((channel, j) => (
                      <span
                        key={j}
                        className="text-xs bg-blue-50 text-blue-700 px-2 py-0.5 rounded"
                      >
                        {channel}
                      </span>
                    ))}
                  </div>
                )}
                {item.sample_message && (
                  <p className="text-xs text-gray-500 italic mt-2">
                    &ldquo;{item.sample_message}&rdquo;
                  </p>
                )}
                {item.spokesperson && (
                  <p className="text-xs text-gray-400 mt-1">
                    Spokesperson: {item.spokesperson}
                  </p>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Key Messages */}
      {playbook.key_messages && playbook.key_messages.length > 0 && (
        <div>
          <h4 className="text-sm font-medium text-gray-500 mb-2">Key Messages</h4>
          <ul className="space-y-1">
            {playbook.key_messages.map((msg, i) => (
              <li key={i} className="text-sm text-gray-700 flex items-start gap-2">
                <span className="text-green-500 mt-0.5">✓</span>
                <span>{msg}</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Spokesperson */}
      {playbook.spokesperson_recommendation && (
        <div>
          <h4 className="text-sm font-medium text-gray-500 mb-2">
            Spokesperson Recommendation
          </h4>
          <p className="text-sm text-gray-700">{playbook.spokesperson_recommendation}</p>
        </div>
      )}

      {/* Do Not Say */}
      {playbook.do_not_say && playbook.do_not_say.length > 0 && (
        <div>
          <h4 className="text-sm font-medium text-red-500 mb-2">⚠ Do NOT Say</h4>
          <ul className="space-y-1">
            {playbook.do_not_say.map((msg, i) => (
              <li
                key={i}
                className="text-sm text-red-700 bg-red-50 px-3 py-1.5 rounded flex items-start gap-2"
              >
                <span className="text-red-500 mt-0.5">✗</span>
                <span>{msg}</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Success Metrics */}
      {playbook.success_metrics && playbook.success_metrics.length > 0 && (
        <div>
          <h4 className="text-sm font-medium text-gray-500 mb-2">Success Metrics</h4>
          <ul className="space-y-1">
            {playbook.success_metrics.map((metric, i) => (
              <li key={i} className="text-sm text-gray-700 flex items-start gap-2">
                <span className="text-indigo-500 mt-0.5">📊</span>
                <span>{metric}</span>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
