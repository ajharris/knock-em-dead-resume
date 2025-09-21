
import axios from 'axios';
let API_BASE;
if (typeof window !== 'undefined') {
  import('./apiBase').then(mod => { API_BASE = mod.default; });
} else {
  API_BASE = require('./apiBase').default;
}

export async function deleteResume(id, token) {
  return axios.delete(`${API_BASE}/resumes/${id}`, {
    headers: { Authorization: `Bearer ${token}` }
  });
}

export async function updateResume(id, data, token) {
  return axios.put(`${API_BASE}/resumes/${id}`, data, {
    headers: { Authorization: `Bearer ${token}` }
  });
}

export async function duplicateResume(resume, token) {
  // Remove id, set new title
  const newTitle = resume.title + ' (Copy)';
  const data = { title: newTitle, content: resume.content };
  return axios.post(`${API_BASE}/resumes`, data, {
    headers: { Authorization: `Bearer ${token}` }
  });
}

export async function renameResume(id, newTitle, token) {
  return axios.put(`${API_BASE}/resumes/${id}`, { title: newTitle }, {
    headers: { Authorization: `Bearer ${token}` }
  });
}
