// Test API_BASE helper for both default and env override
describe('API_BASE', () => {
  afterEach(() => {
    delete process.env.REACT_APP_API_URL;
    jest.resetModules();
  });

  it('should use localhost for development', () => {
    const apiBase = require('../services/apiBase').default;
    expect(apiBase).toBe('http://localhost:8000');
  });

  it('should use REACT_APP_API_URL if set', () => {
    process.env.REACT_APP_API_URL = 'https://prod.example.com';
    const apiBase = require('../services/apiBase').default;
    expect(apiBase).toBe('https://prod.example.com');
  });
});
