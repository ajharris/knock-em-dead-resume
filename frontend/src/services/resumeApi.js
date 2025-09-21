
import axios from 'axios';
import API_BASE from './apiBase';

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
