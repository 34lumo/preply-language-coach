# Language Coach

Post-lesson analytics for language tutors: feed it the transcripts of a student's lessons and it shows how the student is actually progressing (vocabulary, talk time, errors, confidence, CEFR estimate) on a dashboard behind a scroll landing page.

## What it is

Built for the Preply Hackathon 2026. Preply gave us Deepgram transcripts of real lessons for two students; the idea was to turn that raw data into something a tutor could read in two minutes after a class, instead of relying on gut feeling about whether the student is improving.

The app has two preset stories you can open from the "Import conversation" screen: Student 1, who improves across sessions, and Student 2, who has plateaued. Each one runs the full pipeline and renders twelve metrics with explanations.

## How it works

- `run.py` reads a lesson folder of Deepgram JSON files (per-word timestamps, speaker diarization, sentiment, topics) and computes the countable metrics: talk ratio, new words versus the previous session, active recall of last session's vocabulary, filler pressure by topic, conversational agency, sentiment arc, topic expansion.
- The same transcript then goes to Claude (`claude-sonnet-4-6`) for the things you cannot count: top errors with a fix, self-repairs, code-switching, grammar "gray zones" the student avoids, a CEFR estimate with reasoning and a short session summary.
- `_api.py` is a FastAPI app that exposes the presets, runs the pipeline on demand and caches each result as JSON so the dashboard loads fast on repeat visits. If `DATABASE_URL` is set it also stores every analyzed session in PostgreSQL (`db.py`); without it, history is simply disabled.
- `api/index.py` and `main.py` wrap the API so Vercel can run it as a serverless function under `/api`.
- `frontend/` is a Vite + React dashboard: a landing page with a scroll-driven image sequence (`public/frames`), then the twelve metric cards built with ECharts, Framer Motion and a gauge component.

Audio input exists but is not wired end to end: `scripts/record.py` records a WAV and `scripts/transcribe_rich.py` sends it to Deepgram, and the `/live/*` endpoints in the API are placeholders.

## Stack

Python 3.10+, FastAPI, Deepgram SDK, Anthropic SDK, psycopg2. Frontend: Vite, React 19, TypeScript, Tailwind CSS v4, Framer Motion, ECharts. Deployed on Vercel.

## Run it

Backend (needs `DEEPGRAM_API_KEY` and `ANTHROPIC_API_KEY`; `DATABASE_URL` is optional):

```bash
pip install -r requirements.txt
DEEPGRAM_API_KEY=... ANTHROPIC_API_KEY=... uvicorn _api:app --reload --port 8000
```

On Windows, copy `start.bat.example` to `start.bat`, fill in the keys and run it.

Frontend:

```bash
cd frontend
npm install --legacy-peer-deps
npm run dev
```

Open http://localhost:5173. The dev server proxies `/api` to the backend on port 8000. `npm run build` produces `frontend/dist`, which is what Vercel serves (see `vercel.json`).

Pipeline only, from the terminal:

```bash
python run.py preply "Student-1/lesson-1" "Student-1/lesson-3"
```

## Project layout

```
run.py                 pipeline: Deepgram JSON -> metrics -> Claude analysis
_api.py                FastAPI app (presets, analysis, cache, history)
main.py, api/index.py  entrypoints that mount the API under /api for Vercel
db.py                  optional PostgreSQL persistence
requirements.txt       Python dependencies
start.bat.example      env var template for Windows
vercel.json            build command and API rewrite for Vercel
Student-1/, Student-2/ Deepgram transcripts of the sample lessons (one JSON per segment)
scripts/               standalone experiments from the hackathon: earlier metric
                       prototypes, audio recording and transcription, a DB check
frontend/              Vite + React dashboard and landing page
```

## Team

- Luis Molina Salvador ([34lumo](https://github.com/34lumo))
- Mateo Perez ([mpchachi](https://github.com/mpchachi))
