export interface Organization {
  id: string;
  name: string;
  industry: string;
  brand_voice: string | null;
  created_at: string;
}

export interface Simulation {
  id: string;
  title: string;
  status: 'pending' | 'running' | 'completed' | 'failed';
  risk_score: number | null;
  parsed_claims: ParsedClaim[];
  sentiment_trajectory: SentimentPoint[];
  scenarios: Scenario[];
  agent_count: number;
  created_at: string;
  completed_at: string | null;
}

export interface ParsedClaim {
  claim: string;
  sensitivity_score: number;
  controversy_potential: string;
  fact_checkability: number;
  trigger_keywords: string[];
}

export interface SentimentPoint {
  phase: string;
  avg_sentiment: number;
  reaction_count: number;
  negative_reactions: number;
}

export interface Scenario {
  id: string;
  scenario_name: string;
  scenario_type: string;
  probability: number;
  severity: 'low' | 'medium' | 'high' | 'critical';
  description: string;
  trigger_points: string[];
  key_narratives: string[];
  peak_time_hours: number;
  playbooks: Playbook[];
}

export interface Playbook {
  strategy_summary: string;
  response_timeline: TimelineItem[];
  key_messages: string[];
  spokesperson_recommendation: string;
  do_not_say: string[];
  success_metrics: string[];
}

export interface TimelineItem {
  time: string;
  actions: string[];
  channels: string[];
  sample_message: string;
  spokesperson: string;
}

export interface SimulationListItem {
  id: string;
  title: string;
  status: string;
  risk_score: number | null;
  created_at: string;
}
