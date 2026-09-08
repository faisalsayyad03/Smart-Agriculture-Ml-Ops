const DEFAULT_API_BASE = '/api';

export const API_BASE = import.meta.env.VITE_API_URL || DEFAULT_API_BASE;

export async function requestJson(path, options = {}) {
  let response;
  try {
    response = await fetch(`${API_BASE}${path}`, {
      headers: {
        'Content-Type': 'application/json',
        ...(options.headers || {}),
      },
      ...options,
    });
  } catch {
    throw new Error(`Prediction server unavailable at ${API_BASE}. Start the FastAPI backend and try again.`);
  }

  const contentType = response.headers.get('content-type') || '';
  const payload = contentType.includes('application/json') ? await response.json() : { message: await response.text() };

  if (!response.ok) {
    throw new Error(payload.message || payload.detail || 'Request failed');
  }

  return payload;
}
