import { clsx, type ClassValue } from 'clsx';
import { twMerge } from 'tailwind-merge';

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function getRiskColor(score: number | null): string {
  if (score === null) return 'text-gray-400';
  if (score < 30) return 'text-green-600';
  if (score < 60) return 'text-yellow-600';
  if (score < 80) return 'text-orange-600';
  return 'text-red-600';
}

export function getRiskBg(score: number | null): string {
  if (score === null) return 'bg-gray-400';
  if (score < 30) return 'bg-green-500';
  if (score < 60) return 'bg-yellow-500';
  if (score < 80) return 'bg-orange-500';
  return 'bg-red-500';
}

export function getRiskLabel(score: number | null): string {
  if (score === null) return 'No Data';
  if (score < 30) return 'Low Risk';
  if (score < 60) return 'Medium Risk';
  if (score < 80) return 'High Risk';
  return 'Critical Risk';
}

export function getSeverityColor(severity: string): string {
  switch (severity) {
    case 'low': return 'bg-green-100 text-green-800';
    case 'medium': return 'bg-yellow-100 text-yellow-800';
    case 'high': return 'bg-orange-100 text-orange-800';
    case 'critical': return 'bg-red-100 text-red-800';
    default: return 'bg-gray-100 text-gray-800';
  }
}
