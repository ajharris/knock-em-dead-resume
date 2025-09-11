import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { deleteResume, duplicateResume, renameResume } from './services/resumeApi';


function MyResumesDashboard({ token, onView, onEdit }) {
  const [resumes, setResumes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [renamingId, setRenamingId] = useState(null);
  const [renameValue, setRenameValue] = useState('');

  const fetchResumes = () => {
    setLoading(true);
    axios.get('/resumes', {
      headers: { Authorization: `Bearer ${token}` }
    })
      .then(res => {
        setResumes(res.data);
        setLoading(false);
      })
      .catch(err => {
        setError('Failed to load resumes');
        setLoading(false);
      });
  };

  useEffect(() => {
    fetchResumes();
    // eslint-disable-next-line
  }, [token]);

  const handleDelete = async (resume) => {
    if (!window.confirm('Delete this resume?')) return;
    await deleteResume(resume.id, token);
    fetchResumes();
  };

  const handleDuplicate = async (resume) => {
    await duplicateResume(resume, token);
    fetchResumes();
  };

  const handleRename = async (resume) => {
    setRenamingId(resume.id);
    setRenameValue(resume.title);
  };

  const handleRenameSubmit = async (resume) => {
    await renameResume(resume.id, renameValue, token);
    setRenamingId(null);
    fetchResumes();
  };

  if (loading) return <div>Loading...</div>;
  if (error) return <div>{error}</div>;

  return (
    <div>
      <h2>My Resumes</h2>
      <table>
        <thead>
          <tr>
            <th>Title</th>
            <th>Last Updated</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {resumes.map(resume => (
            <tr key={resume.id}>
              <td>
                {renamingId === resume.id ? (
                  <>
                    <input value={renameValue} onChange={e => setRenameValue(e.target.value)} />
                    <button onClick={() => handleRenameSubmit(resume)}>Save</button>
                    <button onClick={() => setRenamingId(null)}>Cancel</button>
                  </>
                ) : (
                  resume.title
                )}
              </td>
              <td>{new Date(resume.updated_at).toLocaleString()}</td>
              <td>
                <button onClick={() => onView(resume)}>View</button>
                <button onClick={() => onEdit(resume)}>Edit</button>
                <button onClick={() => handleDelete(resume)}>Delete</button>
                <button onClick={() => handleDuplicate(resume)}>Duplicate</button>
                <button onClick={() => handleRename(resume)}>Rename</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default MyResumesDashboard;
