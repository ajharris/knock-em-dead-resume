import API_BASE from '../services/apiBase';

describe('API_BASE', () => {
  it('should use localhost for development', () => {
    process.env.REACT_APP_API_URL = '';
    jest.resetModules();
    const apiBase = require('../services/apiBase').default;
    expect(apiBase).toBe('http://localhost:8000');
  });

  it('should use REACT_APP_API_URL if set', () => {
    process.env.REACT_APP_API_URL = 'https://prod.example.com';
    jest.resetModules();
    const apiBase = require('../services/apiBase').default;
    expect(apiBase).toBe('https://prod.example.com');
  });
});
