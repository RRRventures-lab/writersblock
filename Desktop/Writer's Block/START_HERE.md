# Writer's Block - Quick Start Guide

## ✅ Backend is Ready!

Your complete Backend API is installed and ready to use.

### Start the Backend (Terminal 1)

```bash
cd "/Users/gabrielrothschild/Desktop/Writer's Block/backend"
source venv/bin/activate
uvicorn main:app --reload
```

You should see:
```
Uvicorn running on http://127.0.0.1:8000
```

### Start the Frontend (Terminal 2)

```bash
cd "/Users/gabrielrothschild/Desktop/Writer's Block"
npm install
npm run dev
```

You should see:
```
local: http://localhost:5173
```

### Access the Application

- **Frontend**: http://localhost:5173
- **API Documentation**: http://127.0.0.1:8000/docs
- **API Health Check**: http://127.0.0.1:8000/health

## What's Working

✅ FastAPI backend with 30+ endpoints
✅ SQLite database (auto-initialized)
✅ Song management (CRUD)
✅ Lyrics, chords, and melody management
✅ AI suggestions (rhymes, chord progressions, lyrics)
✅ Audio file handling
✅ Interactive API documentation

## Test the API

Once the backend is running, visit:
**http://127.0.0.1:8000/docs**

This gives you an interactive explorer where you can:
- Create a song
- Get rhyme suggestions
- Get chord suggestions
- Upload audio files
- And more!

## Environment Configuration

If you need to change settings, edit:
`/Users/gabrielrothschild/Desktop/Writer's Block/backend/.env`

Common settings:
- `API_PORT=8000` - Change backend port
- `DEBUG=true` - Debug mode
- `OPENAI_API_KEY=...` - Add OpenAI integration (optional)

## Troubleshooting

**Backend won't start?**
- Make sure port 8000 is free: `lsof -i :8000`
- Check Python is Python 3.13: `python3 --version`

**Frontend won't start?**
- Make sure port 5173 is free: `lsof -i :5173`
- Run `npm install` first

**CORS errors?**
- Both servers need to be running
- Backend on 127.0.0.1:8000
- Frontend on localhost:5173

## What's Been Created

- **Backend**: Complete FastAPI application with all features
- **Database**: SQLite with 6 tables (auto-created)
- **Virtual Environment**: Python 3.13 with all dependencies
- **Configuration**: .env file ready to use
- **Documentation**: Full API docs at /docs endpoint

## Next Steps

1. Start both servers ↑
2. Open http://localhost:5173
3. Create your first song
4. Enjoy your songwriting studio! 🎵

---

**Questions?** Check the API docs at http://127.0.0.1:8000/docs
