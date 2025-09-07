
# Knock 'Em Dead Resume

An AI-powered resume builder based on Martin Yate’s Knock ’Em Dead formula. It finds job ads, extracts key skills, and helps craft tailored, achievement-driven resumes optimized for each role, with ATS-friendly formatting and AI coaching for stronger career impact.

---

## Project Structure

- **backend/**: FastAPI app, SQLAlchemy models, OpenAI integration, and backend tests
- **frontend/**: React app, MSW for API mocking, Jest/Testing Library for frontend tests

---

## Features
- AI-powered resume generation and optimization
- Extracts key skills from job ads
- ATS-friendly formatting
- Achievement-driven resume suggestions
- AI coaching for career impact

---

## Setup & Installation

### 1. Clone the repository
```bash
git clone https://github.com/ajharris/knock-em-dead-resume.git
cd knock-em-dead-resume
```

### 2. Backend Setup
```bash
cd backend
# (Recommended) Create a virtual environment
python3 -m venv .venv
source .venv/bin/activate
pip install -r ../requirements.txt
# Run backend tests
pytest
```

### 3. Frontend Setup
```bash
cd ../frontend
npm install
# Run frontend tests
npm test
# Start the frontend (Vite)

```

---

## Running All Tests
From the project root:
```bash
./test_all.sh
```
This will run both backend and frontend tests.

---

## Usage

1. Start the backend API (see backend/app/main.py for FastAPI entrypoint)
2. Start the frontend (Vite dev server)
3. Open your browser to the provided local address (default: http://localhost:3000)

---

## Technologies Used
- FastAPI, SQLAlchemy, Alembic (backend)
- React, Vite, MSW, Jest, Testing Library (frontend)
- OpenAI API (AI/ML integration)

---

## Contributing
Contributions are welcome! Please open issues or submit pull requests for improvements and bug fixes.

---

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
