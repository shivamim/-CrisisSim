'use client';

import { useState, useEffect } from 'react';
import { useParams } from 'next/navigation';
import { api } from '@/lib/api';
import { Simulation } from '@/lib/types';
import { RiskDashboard } from '@/components/RiskDashboard';
import { ScenarioCard } from '@/components/ScenarioCard';

export default function SimulationDetailPage() {
  const params = useParams();
  const id = params.id as string;
  const [simulation, setSimulation] = useState<Simulation | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!id) return;
    
    let interval: Node.js.Timeout;
    
    const fetchSim = async () => {
      try {
        const data = await api.get<Simulation>(`/simulations/${id}`);
        setSimulation(data);
        
        if (data.status === 'running' || data.status === 'pending') {
          interval = setTimeout(fetchSim, 5000); // Poll every 5 seconds
        } else {
          setLoading(false);
        }
      } catch (err) {
        setLoading(false);
      }
    };
    
    fetchSim();
    
    return () => clearInterval(interval);
  }, [id]);

  if (loading || !simulation) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[60vh]">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600 mb-4"></div>
        <p className="text-gray-500">
          {simulation?.status === 'running' ? 'Agents are reacting...' : 'Loading simulation...'}
        </p>
        <p className="text-gray-400 text-sm mt-2">This may take 2-3 minutes.</p>
      </div>
    );
  }

  if (simulation.status === 'failed') {
    return (
      <div className="max-w-4xl mx-auto px-4 py-12 text-center">
        <div className="bg-red-50 border border-red-200 rounded-xl p-8">
          <h1 className="text-2xl font-bold text-red-700 mb-2">Simulation Failed</h1>
          <p className="text-red-600">There was an error running this simulation.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto px-4 py-8 space-y-8">
      <div>
        <h1 className="text-3xl font-bold">{simulation.title}</h1>
        <p className="text-gray-500">Simulation Results</p>
      </div>
      
      <RiskDashboard simulation={simulation} />
      
      <div>
        <h2 className="text-2xl font-bold mb-4">Crisis Scenarios</h2>
        <div className="grid gap-6">
          {simulation.scenarios.map((scenario) => (
            <ScenarioCard key={scenario.id} scenario={scenario} />
          ))}
        </div>
      </div>
    </div>
  );
}
