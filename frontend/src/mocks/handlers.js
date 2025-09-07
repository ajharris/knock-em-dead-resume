
import { http, HttpResponse } from 'msw';

export const handlers = [
  http.post('/extract_keywords', () => {
    console.log('MSW: /extract_keywords handler called');
    return HttpResponse.json({
      keywords: [
        "python", "sql", "data visualization", "tableau", "power bi", "aws", "communication skills"
      ]
    }, { status: 200 });
  })
];
