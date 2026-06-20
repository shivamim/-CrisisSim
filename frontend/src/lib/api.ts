const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
const API_PREFIX = '/api/v1';

export const api = {
  async get<T>(path: string): Promise<T> {
    const response = await fetch(`${API_BASE}${API_PREFIX}${path}`);
    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'Unknown error' }));
      throw new Error(error.detail || `API Error: ${response.status}`);
    }
    return response.json();
  },

  async post<T>(path: string, body: unknown): Promise<T> {
    const response = await fetch(`${API_BASE}${API_PREFIX}${path}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    });
    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'Unknown error' }));
      throw new Error(error.detail || `API Error: ${response.status}`);
    }
    return response.json();
  },
};
