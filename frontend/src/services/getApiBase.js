// Helper to get API base URL in both Vite (import.meta.env) and Jest (process.env)


// Returns API base from process.env or default
export default function getApiBase() {
  if (typeof process !== 'undefined' && process.env && process.env.REACT_APP_API_URL) {
    return process.env.REACT_APP_API_URL;
  }
  return "http://localhost:8000";
}
