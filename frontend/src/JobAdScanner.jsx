import React, { useState } from 'react';
import axios from 'axios';

const JobAdScanner = () => {
  const [jobAdFile, setJobAdFile] = useState(null);
  const [resumeFile, setResumeFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [result, setResult] = useState(null);

  const handleFileChange = (e, setter) => {
    setter(e.target.files[0]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setResult(null);
    if (!jobAdFile || !resumeFile) {
      setError('Please upload both a job ad and a resume.');
      return;
    }
    setLoading(true);
    const formData = new FormData();
    formData.append('job_ad', jobAdFile);
    formData.append('resume', resumeFile);
    try {
      const res = await axios.post('/flask/api/scan_resume', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      setResult(res.data);
    } catch (err) {
      setError(err.response?.data?.error || 'Upload failed.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-6 max-w-5xl mx-auto">
      <h1 className="text-2xl font-bold mb-4">Job Ad Scanner</h1>
      <form onSubmit={handleSubmit} className="flex flex-col gap-4 bg-white p-4 rounded shadow">
        <div>
          <label htmlFor="job-ad-upload" className="block font-semibold mb-1">Job Ad (PDF or text):</label>
          <input id="job-ad-upload" type="file" accept=".pdf,.txt" onChange={e => handleFileChange(e, setJobAdFile)} className="border p-2 rounded w-full" />
        </div>
        <div>
          <label htmlFor="resume-upload" className="block font-semibold mb-1">Resume (PDF or DOCX):</label>
          <input id="resume-upload" type="file" accept=".pdf,.docx" onChange={e => handleFileChange(e, setResumeFile)} className="border p-2 rounded w-full" />
        </div>
        <button type="submit" className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700" disabled={loading}>
          {loading ? 'Scanning...' : 'Scan Resume'}
        </button>
        {error && <div className="text-red-600 font-semibold">{error}</div>}
      </form>
      {result && (
        <div className="mt-8 grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="bg-gray-50 p-4 rounded shadow overflow-auto max-h-96">
            <h2 className="font-bold mb-2">Job Ad Text</h2>
            <pre className="whitespace-pre-wrap text-sm">{result.job_ad_text}</pre>
          </div>
          <div className="bg-gray-50 p-4 rounded shadow overflow-auto max-h-96">
            <h2 className="font-bold mb-2">Resume Text</h2>
            <pre className="whitespace-pre-wrap text-sm">{result.resume_text}</pre>
          </div>
          <div className="md:col-span-2 bg-white p-4 rounded shadow mt-4">
            <h2 className="font-bold mb-2">Results</h2>
            <div className="mb-2">
              <span className="font-semibold">Strengths (Matches):</span>
              <span className="ml-2 text-green-700">{result.matches.join(', ') || 'None'}</span>
            </div>
            <div className="mb-2">
              <span className="font-semibold">Gaps (Missing):</span>
              <span className="ml-2 text-red-700">{result.gaps.join(', ') || 'None'}</span>
            </div>
            <div>
              <span className="font-semibold">Coverage:</span>
              <span className="ml-2">{result.summary.coverage}</span>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default JobAdScanner;
