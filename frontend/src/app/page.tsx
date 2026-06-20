'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { api } from '@/lib/api';
import { SimulationListItem, Organization } from '@/lib/types';
import { getRiskColor } from '@/lib/utils';

export default function HomePage() {
  const [simulations, setSimulations] = useState<SimulationListItem[]>([]);
  const [organizations, setOrganizations] = useState<Organization[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [sims, orgs] = await Promise.all([
          api.get<SimulationListItem[]>('/simulations?limit=10').catch(() => []),
          api.get<Organization[]>('/organizations').catch(() => []),
        ]);
        setSimulations(sims);
        setOrganizations(orgs);
      } catch {
        // Silent fail
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  return (
    <div>
      {/* Hero */}
      <div className="bg-gradient-to-br from-gray-900 via-gray-900 to-indigo-900 text-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
          <h1 className="text-4xl md:text-5xl font-bold mb-4">
            Simulate Crises <span className="text-indigo-400">Before</span> They Happen
          </h1>
          <p className="text-lg md:text-xl text-gray-300 mb-8 max-w-2xl">
            Upload your launch plan. Our multi-agent AI simulates how Twitter, Reddit, TikTok, and
            journalists will react. Get crisis scenarios and response playbooks in minutes.
          </p>
          <div className="flex gap-4 flex-wrap">
            <Link
              href="/simulations/new"
              className="bg-indigo-600 hover:bg-indigo-700 px-6 py-3 rounded-lg font-medium transition"
            >
              Run Simulation →
            </Link>
            <Link
              href="/organizations/new"
              className="border border-gray-600 hover:border-gray-400 px-6 py-3 rounded-lg font-medium transition"
            >
              Setup Organization
            </Link>
          </div>
        </div>
      </div>

      {/* Recent Simulations */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-2xl font-bold">Recent Simulations</h2>
          {organizations.length === 0 && !loading && (
            <span className="text-sm text-gray-500">
              Create an organization to get started
            </span>
          )}
        </div>

        {loading ? (
          <div className="text-center py-12 text-gray-400">Loading...</div>
        ) : simulations.length === 0 ? (
          <div className="text-center py-12 bg-gray-50 rounded-xl border border-dashed">
            <p className="text-gray-500 mb-4">No simulations yet</p>
            <Link
              href="/simulations/new"
              className="text-indigo-600 font-medium hover:text-indigo-700"
            >
              Run your first simulation →
            </Link>
          </div>
        ) : (
          <div className="grid gap-4">
