# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

NS AI is an AI-powered web application for analyzing Type 1 diabetes management data from Nightscout and Loop. It features multiple AI personas (Emanuel, Hanna, Cora, Benny) backed by Google Gemini 2.5 Flash with RAG via Gemini file search stores.

## Development Commands

### Frontend (React + TypeScript + Vite)
```bash
cd frontend
npm install
npm run dev      # Dev server on port 5173, proxies /api/* to localhost:8000
npm run build    # tsc -b && vite build
npm run lint     # ESLint
```

### Backend (FastAPI + Python 3.11)
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000
# Or with auto-reload:
uvicorn app.main:app --reload --port 8000
```

### Docker (full stack)
```bash
./build-and-push.sh   # Build and push to Google Artifact Registry (europe-north2)
```

### Infrastructure
```bash
cd terraform
terraform init && terraform plan && terraform apply
```

## Architecture

### Stack
- **Frontend**: React 19, TypeScript, Vite, react-router-dom v7, Firebase SDK
- **Backend**: FastAPI, Pydantic, Firebase Admin SDK, google-generativeai
- **Database**: Firestore (GCP project `ns-ai-project`)
- **Auth**: Firebase Auth (Google OAuth) + JWT verification on backend
- **AI**: Google Gemini 2.5 Flash with file search stores for RAG
- **Deployment**: Google Cloud Run (europe-north2), GitHub Actions CI/CD

### Request Flow
1. React SPA authenticates via Firebase Auth (Google OAuth)
2. Frontend calls `backend/` API routes with `Authorization: Bearer <firebase_jwt>` header
3. Backend (`app/core/auth.py`) verifies JWT via Firebase Admin SDK and enforces role-based access (pending/user/admin)
4. Chat requests stream NDJSON responses: lines typed as `prompt`, `content`, `usage`, or `error`

### Key Backend Services (`backend/app/services/`)
- `gemini.py` — Gemini API client; streams responses using file search stores for context
- `scraper.py` — Crawls Nightscout/Loop docs and creates/updates Gemini file search stores
- `firebase.py` — Firestore CRUD, visitor counter, prompt storage
- `user_service.py` — User role management

### Key Backend Routes (`backend/app/api/routes.py`)
- `POST /emanuel` — Streams Emanuel chat (authenticated, role ≥ user)
- `GET /emanuel/file-store-info` — RAG store metadata
- `POST /scrape` — Trigger doc scraper to refresh Gemini file store
- `GET /health`, `GET /version`, `GET /page-load`

### Frontend API Client
All backend calls go through `frontend/src/api.ts`, which attaches the Firebase auth token. Chat responses are consumed as streaming NDJSON.

### Production BFF
In production, `frontend/server.js` (Express) serves the built SPA and proxies API requests to the Cloud Run backend, injecting OIDC tokens for service-to-service auth.

## Environment Variables

**Backend** (`.env` or Secret Manager in production):
- `GEMINI_API_KEY` — Google Gemini API key
- `ENABLE_CLOUD_LOGGING` — Enable GCP Cloud Logging (default: `true`)
- `GOOGLE_APPLICATION_CREDENTIALS` — Path to service account JSON

**Frontend** (`frontend/.env`):
- `VITE_API_BASE_URL` — Backend URL (default: `http://localhost:8000`)
- `VITE_FIREBASE_*` — Firebase project config (API key, auth domain, project ID, etc.)

## CI/CD

`.github/workflows/deploy.yml` triggers on push to `main`:
1. Authenticates to GCP via Workload Identity Federation
2. Builds and pushes backend + frontend Docker images to Artifact Registry
3. Deploys both to Cloud Run, pulling secrets from Google Secret Manager
