// Runtime API URL with safe fallback for development.
// If VITE_API_URL points to the Docker service name `backend` but the frontend
// is served from the host (localhost), replace `backend` with `localhost`.
const envUrl = import.meta.env.VITE_API_URL ?? '';
let computedUrl = envUrl;

try {
	if (typeof window !== 'undefined' && envUrl.includes('backend')) {
		// Only replace when the browser hostname is localhost (dev scenario)
		if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
			computedUrl = envUrl.replace('backend', 'localhost');
		}
	}
} catch (e) {
	// ignore
}

export const API_URL = computedUrl || 'http://localhost:8000';
