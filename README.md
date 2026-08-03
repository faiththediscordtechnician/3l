# 3L Academic Hub

A personal, private academic management app for law school. Manage readings, notes, todos, and deadlines across your 5 classes for the first semester. Built with N64-inspired retro gaming aesthetics, rich text editing, and gamification rewards.

## Features

- **Class Management**: Organize your 5 classes as separate "games"
- **Reading Tracker**: Track assigned readings with status, pages, and time
- **Rich Text Editor**: Write notes with formatting (bold, italic, underline, highlights, fonts) on a ruled paper aesthetic
- **CanLII Integration**: Search Canadian case law directly in the app
- **Todo Lists**: Manage tasks per class with deadlines
- **Calendar View**: See all deadlines across classes
- **Gamification**: Earn rewards for milestones (100 words = star, etc.)
- **Autosave**: Everything saves automatically every few seconds
- **Export**: Save notes as PDF or Markdown
- **Windowed UI**: Retro windowed interface with draggable, closeable windows
- **Multi-device Access**: Simple password login to access from multiple computers

## Tech Stack

- **Backend**: FastAPI (Python)
- **Frontend**: React with Vite
- **Database**: PostgreSQL (deployed on Railway)
- **Deployment**: Railway

## Setup

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Update .env with your database URL
uvicorn main:app --reload
```

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

### Database Setup

Create a PostgreSQL database and update the `DATABASE_URL` in backend/.env.

```bash
# From backend directory
python
from models import Base
from database import engine
Base.metadata.create_all(bind=engine)
```

## Environment Variables

### Backend (.env)
- `DATABASE_URL`: PostgreSQL connection string
- `SECRET_KEY`: JWT secret key
- `CANLII_API_KEY`: Optional CanLII API key (if not provided, uses public search)

### Frontend (.env)
- `VITE_API_URL`: Backend API URL (default: http://localhost:8000)

## Development

- Backend runs on http://localhost:8000
- Frontend runs on http://localhost:5173
- API documentation at http://localhost:8000/docs

## Deployment on Railway

1. Push to GitHub
2. Connect repository to Railway
3. Add PostgreSQL database service
4. Set environment variables
5. Deploy!

Production URL: https://3l-production.up.railway.app
Internal Railway URL: 3l.railway.internal

## Styling

Uses a warm pastel color palette:
- **Alabaster Grey** (#d8e2dcff): Console background
- **Powder Petal** (#ffe5d9ff): Light UI elements
- **Pastel Pink** (#ffcad4ff): Interactive buttons
- **Cherry Blossom** (#f4acb7ff): Accents and hover states
- **Dusty Mauve** (#9d8189ff): Text and borders

## License

Personal use only - not for commercial use.
