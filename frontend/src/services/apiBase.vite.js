// Vite/browser version: uses import.meta.env
let API_BASE = "http://localhost:8000";
if (typeof import.meta !== 'undefined' && import.meta.env && import.meta.env.VITE_REACT_APP_API_URL) {
  API_BASE = import.meta.env.VITE_REACT_APP_API_URL;
}
export default API_BASE;