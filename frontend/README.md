
# Knock 'Em Dead Resume Builder Frontend

This is the React frontend for the Knock 'Em Dead Resume Builder, built with Vite.

## Local Development

1. Install dependencies:
	```bash
	npm install
	```
2. Create a `.env` file (already present) for local API URL:
	```env
	REACT_APP_API_URL=http://localhost:8000
	```
3. Start the dev server:
	```bash
	npm run dev
	```

## Production Build

To build for production:

```bash
npm run build
```

The output will be in the `dist/` folder.

## Environment Variables

- `.env` (development):
  - `REACT_APP_API_URL=http://localhost:8000`
- `.env.production` (production):
  - `REACT_APP_API_URL=https://your-backend.example.com`

## Deploying to GitHub Pages

This project is configured to deploy the production build to GitHub Pages using the `gh-pages` branch.

### Manual Deploy

1. Build the app:
	```bash
	npm run build
	```
2. Deploy:
	```bash
	npm run deploy
	```

### Automatic Deploy (CI/CD)

On every push to `main`, GitHub Actions will:
- Install dependencies
- Run tests
- Build the frontend with `.env.production` (API URL from repo secrets)
- Deploy to GitHub Pages (`gh-pages` branch)

See `.github/workflows/deploy.yml` for details.

## API Base URL Switching

The frontend uses `process.env.REACT_APP_API_URL` to determine the backend API base URL. This is set via environment files or CI secrets.

## Testing

Run unit tests with:

```bash
npm test
```

Tests include checks for correct API base URL switching between dev and prod.
