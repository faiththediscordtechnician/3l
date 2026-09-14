# Quick Notes

A fast MVP note-taking app with persistent auto-save storage.

## Features

- ✨ Create, edit, and delete notes
- 📌 Pin important notes
- 💾 Auto-save every 1 second (with debouncing)
- 🔄 Sync with backend every 30 seconds
- 🎨 Beautiful N64-inspired pastel aesthetic
- ⚡ Lightning-fast and responsive

## Tech Stack

- **Frontend**: React 18 + Vite
- **Backend**: FastAPI + SQLAlchemy
- **Database**: PostgreSQL (production) / SQLite (development)
- **Styling**: Custom CSS with Press Start 2P and VT323 fonts

## Development

### Prerequisites

- Node.js 18+
- Python 3.11+
- Docker & Docker Compose (optional)

### Local Setup

```bash
# Install backend dependencies
cd backend
pip install -r requirements.txt

# Install frontend dependencies
cd ../frontend
npm install

# Start backend (in backend directory)
uvicorn main:app --reload

# Start frontend (in frontend directory, new terminal)
npm run dev
```

### Docker Development

```bash
docker-compose up
```

- Backend: http://localhost:8000
- Frontend: http://localhost:5173
- Database: PostgreSQL at localhost:5432

### Production Build

```bash
docker build -t quick-notes .
docker run -p 8080:8080 quick-notes
```

Access at http://localhost:8080

## Environment Variables

- `DATABASE_URL`: PostgreSQL connection string (default: sqlite:///./notes.db)
- `VITE_API_URL`: API base URL (default: /api)

## Architecture

Single unified Docker container with:
- Uvicorn serving FastAPI backend on port 8000
- Nginx serving React frontend on port 8080
- Nginx proxying `/api/*` to backend
- Supervisor managing both services

Notes are synced to backend every 30 seconds and whenever content changes.
