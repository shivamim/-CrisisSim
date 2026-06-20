'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { api } from '@/lib/api';

const INDUSTRIES = [
  { value: 'tech', label: 'Technology' },
  { value: 'fintech', label: 'Fintech' },
  { value: 'food', label: 'Food & Beverage' },
  { value: 'healthcare', label: 'Healthcare' },
  { value: 'retail', label: 'Retail' },
  { value: 'media', label: 'Media & Entertainment' },
  { value: 'education', label: 'Education' },
  { value: 'other', label: 'Other' },
];

export function OrganizationForm() {
  const router = useRouter();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const [formData, setFormData] = useState({
    name: '',
    industry: 'tech',
    brand_voice: '',
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      await api.post<{ id: string }>('/organizations', formData);
      router.push('/simulations/new');
      router.refresh();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to create organization');
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      {error && (
        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
          {error}
        </div>
      )}

      <div>
        <label className="block text-sm font-medium mb-2">Organization Name</label>
        <input
          type="text"
          value={formData.name}
          onChange={(e) => setFormData({ ...formData, name: e.target.value })}
          className="w-full border rounded-lg p-3 focus:ring-2 focus:ring-indigo-500 focus:border-transparent outline-none"
          placeholder="e.g., Acme Corp"
          required
        />
      </div>

      <div>
        <label className="block text-sm font-medium mb-2">Industry</label>
        <select
          value={formData.industry}
          onChange={(e) => setFormData({ ...formData, industry: e.target.value })}
          className="w-full border rounded-lg p-3 focus:ring-2 focus:ring-indigo-500 focus:border-transparent outline-none"
        >
          {INDUSTRIES.map((ind) => (
            <option key={ind.value} value={ind.value}>
              {ind.label}
            </option>
          ))}
        </select>
      </div>

      <div>
        <label className="block text-sm font-medium mb-2">Brand Voice (Optional)</label>
        <textarea
          value={formData.brand_voice}
          onChange={(e) => setFormData({ ...formData, brand_voice: e.target.value })}
          className="w-full border rounded-lg p-3 min-h-[100px] focus:ring-2 focus:ring-indigo-500 focus:border-transparent outline-none"
          placeholder="Describe how your brand typically communicates (e.g., 'Professional, transparent, data-driven')"
        />
      </div>

      <button
        type="submit"
        disabled={loading}
        className="w-full bg-indigo-600 text-white py-3 rounded-lg font-medium hover:bg-indigo-700 disabled:opacity-50 transition"
      >
        {loading ? 'Creating...' : 'Create Organization'}
      </button>
    </form>
  );
}
