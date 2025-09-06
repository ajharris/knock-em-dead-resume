import { rest } from 'msw';

export const handlers = [
  rest.post('/extract_keywords', (req, res, ctx) => {
    return res(
      ctx.status(200),
      ctx.json({ keywords: [
        "python", "sql", "data visualization", "tableau", "power bi", "aws", "communication skills"
      ] })
    );
  })
];
