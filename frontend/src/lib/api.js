const DEFAULT_API_BASE = 'http://localhost:8000/api';

export const API_BASE = import.meta.env.VITE_API_URL || DEFAULT_API_BASE;

export async function requestJson(path, options = {}) {
  const response = await fetch(`${API_BASE}${path}`, {
    headers: {
      'Content-Type': 'application/json',
      ...(options.headers || {}),
    },
    ...options,
  });

  const contentType = response.headers.get('content-type') || '';
  const payload = contentType.includes('application/json') ? await response.json() : { message: await response.text() };

  if (!response.ok) {
    throw new Error(payload.message || payload.detail || 'Request failed');
  }

  return payload;
}
