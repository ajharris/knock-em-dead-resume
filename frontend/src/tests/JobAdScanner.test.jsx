import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import JobAdScanner from '../JobAdScanner';
import axios from 'axios';

jest.mock('axios');

describe('JobAdScanner', () => {
  it('renders upload form and handles missing files', async () => {
    render(<JobAdScanner />);
    fireEvent.click(screen.getByText(/Scan Resume/i));
    expect(await screen.findByText(/Please upload both a job ad and a resume/i)).toBeInTheDocument();
  });

  it('uploads files and displays results', async () => {
    axios.post.mockResolvedValueOnce({
      data: {
        job_ad_text: 'Job ad text',
        resume_text: 'Resume text',
        matches: ['python', 'sql'],
        gaps: ['aws'],
        summary: { coverage: '2/3' },
      },
    });
    render(<JobAdScanner />);
    const jobAdInput = screen.getByLabelText(/Job Ad/i);
    const resumeInput = screen.getByLabelText(/Resume/i);
    fireEvent.change(jobAdInput, { target: { files: [new File(['job'], 'job.pdf', { type: 'application/pdf' })] } });
    fireEvent.change(resumeInput, { target: { files: [new File(['resume'], 'resume.docx', { type: 'application/vnd.openxmlformats-officedocument.wordprocessingml.document' })] } });
    fireEvent.click(screen.getByText(/Scan Resume/i));
  expect(await screen.findByRole('heading', { name: /Job Ad Text/i })).toBeInTheDocument();
  expect(screen.getByRole('heading', { name: /Resume Text/i })).toBeInTheDocument();
    expect(screen.getByText(/Strengths/i)).toBeInTheDocument();
    expect(screen.getByText(/python, sql/i)).toBeInTheDocument();
    expect(screen.getByText(/aws/i)).toBeInTheDocument();
    expect(screen.getByText(/2\/3/)).toBeInTheDocument();
  });
});
