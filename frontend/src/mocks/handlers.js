
import { http, HttpResponse } from 'msw';

export const handlers = [
  http.post('/extract_keywords', () => {
    console.log('MSW: /extract_keywords handler called (relative)');
    return HttpResponse.json({
      keywords: [
        "python", "sql", "data visualization", "tableau", "power bi", "aws", "communication skills"
      ]
    }, { status: 200 });
  }),
  http.post('http://localhost:8000/extract_keywords', () => {
    console.log('MSW: /extract_keywords handler called (absolute)');
    return HttpResponse.json({
      keywords: [
        "python", "sql", "data visualization", "tableau", "power bi", "aws", "communication skills"
      ]
    }, { status: 200 });
  }),
  http.post('/profile/1/job-preferences', () => {
    return HttpResponse.json({
      relocate: "no",
      willing_to_travel: "no",
      job_title_1: "Engineer",
      job_title_2: "",
      job_title_3: "",
      desired_industry_segment: "",
      career_change: "no"
    }, { status: 200 });
  })
];
