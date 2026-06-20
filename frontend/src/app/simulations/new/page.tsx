'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { api } from '@/lib/api';
import { Organization } from '@/lib/types';

export default function NewSimulationPage() {
  const router = useRouter();
  const [organizations, setOrganizations] = useState<Organization[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const [formData, setFormData] = useState({
    organization_id: '',
    title: '',
    announcement_text: '',
    industry_context: '',
  });

  useEffect(() => {
    api.get<Organization[]>('/organizations').then(setOrganizations).catch(() => {});
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const res = await api.post<{ id: string }>('/simulations', formData);
      router.push(`/simulations/${res.id}`);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to start simulation');
      setLoading(false);
    }
  };

  return (
    <div className="max-w-3xl mx-auto px-4 py-12">
      <div className="mb-8">
        <h1 className="text-3xl font-bold mb-2">New Crisis Simulation</h1>
        <p className="text-gray-500">
          Paste your launch plan or announcement below. The AI will simulate how the internet reacts.
        </p>
      </div>

      <form onSubmit={handleSubmit} className="bg-white rounded-xl shadow-sm border p-8 space-y-6">
        {error && (
          <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
            {error}
          </div>
        )}

        <div>
          <label className="block text-sm font-medium mb-2">Organization</label>
          <select
            value={formData.organization_id}
            onChange={(e) => setFormData({ ...formData, organization_id: e.target.value })}
            className="w-full border rounded-lg p-3 focus:ring-2 focus:ring-indigo-500 outline-none"
            required
          >
            <option value="">Select an organization</option>
            {organizations.map((org) => (
              <option key={org.id} value={org.id}>
                {org.name} ({org.industry})
              </option>
            ))}
          </select>
          {organizations.length === 0 && (
            <p className="text-xs text-gray-400 mt-1">
              No organizations found. Please create one first.
            </p>
          )}
        </div>

        <div>
          <label className="block text-sm font-medium mb-2">Simulation Title</label>
          <input
            type="text"
            value={formData.title}
            onChange={(e) => setFormData({ ...formData, title: e.target.value })}
            className="w-full border rounded-lg p-3 focus:ring-2 focus:ring-indigo-500 outline-none"
            placeholder="e.g., Q3 Product Launch Announcement"
            required
          />
        </div>

        <div>
          <label className="block text-sm font-medium mb-2">Announcement / Launch Plan</label>
          <textarea
            value={formData.announcement_text}
            onChange={(e) => setFormData({ ...formData, announcement_text: e.target.value })}
            className="w-full border rounded-lg p-3 min-h-[200px] focus:ring-2 focus:ring-indigo-500 outline-none font-mono text-sm"
            placeholder="Paste the full text of your press release, tweet, or launch blog post here..."
            required
          />
        </div>

        <div>
          <label className="block text-sm font-medium mb-2">Industry Context (Optional)</label>
          <input
            type="text"
            value={formData.industry_context}
            onChange={(e) => setFormData({ ...formData, industry_context: e.target.value })}
            className="w-full border rounded-lg p-3 focus:ring-2 focus:ring-indigo-500 outline-none"
            placeholder="Any additional context about your market or competitors"
          />
        </div>

        <button
          type="submit"
          disabled={loading || !formData.organization_id}
          className="w-full bg-indigo-600 text-white py-3 rounded-lg font-medium hover:bg-indigo-700 disabled:opacity-50 transition"
        >
          {loading ? 'Starting Simulation...' : '🚀 Run Simulation'}
        </button>
      </form>
    </div>
  );
}
