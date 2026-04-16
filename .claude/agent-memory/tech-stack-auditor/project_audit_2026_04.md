---
name: Dependency Audit April 2026
description: First full tech stack audit findings — versions, deprecated APIs, and security issues found in April 2026
type: project
---

Audit performed 2026-04-15. Key findings:

**Why:** Routine first audit of the full stack to establish a baseline.
**How to apply:** Use as baseline for future audits; cross-reference these findings before suggesting changes.

## Confirmed current/good
- React 19.2.1 — current
- react-router-dom 7.9.6 — current
- Vite 7.2.4 — current
- TypeScript 5.9.3 — current
- @vitejs/plugin-react 5.1.1 — current
- eslint 9.39.1 — current
- FastAPI with [standard] — current
- google-genai (new SDK) — used correctly in main services (emanuel.py, scraper.py)
- Workload Identity Federation for GitHub Actions — correct pattern
- google-cloud_run_v2_service in Terraform — current resource type
- Node 22-alpine frontend Docker base image — current LTS

## Issues found

### Critical
- **VITE_AUTH_PASSWORD baked into Docker image as ENV**: A static password is passed via ARG→ENV and baked into the image layer. Anyone with image pull access can extract it with `docker inspect`. The variable doesn't appear to be used in current frontend code but is still passed. Should be removed entirely or moved to a runtime secret if needed.

### High
- **firebase SDK 10.7.1** (frontend): As of April 2026, Firebase JS SDK is at 11.x. v10→v11 is a drop-in upgrade with tree-shaking improvements and Firestore v4 client. Pin: `firebase@^11.0.0`.
- **Dual Gemini SDK conflict**: Both `google-generativeai` (old SDK) and `google-genai` (new SDK) are listed in requirements.txt. Main services use `google-genai` correctly. `count_tokens.py` and `list_models.py` still use the old `google.generativeai` import style. The old `google-generativeai` package should be removed from requirements.txt.
- **`datetime.utcnow()` deprecated** (Python 3.12+): Used in `auth.py` (2x), `user_service.py` (3x). Deprecated since Python 3.12. Replace with `datetime.now(timezone.utc)`.
- **Pydantic v1-style `.dict()` calls**: `user_service.py` calls `user.dict()` and `updates.dict(exclude_unset=True)`. These are Pydantic v1 APIs. Pydantic v2 (which ships with current FastAPI) uses `.model_dump()`. Will emit deprecation warnings.

### Medium
- **Terraform google provider pinned to ~> 5.0**: hashicorp/google is at 6.x as of April 2026. v6 includes Cloud Run v2 improvements, Firestore enhancements. Should update to `~> 6.0`.
- **`http-proxy-middleware` 2.0.6** (frontend): v3.x is the current stable release (released mid-2024) with breaking API changes to match `express` v5. Currently on v2. Since the project uses Express v4, v2 is compatible — upgrade to v3 when Express is also upgraded, or check if v3 is compatible with Express v4 (it is).
- **`google-auth-library` 9.4.1**: Current is 9.x series (9.14+ as of April 2026). Patch/minor upgrade within the same major.
- **`_log_file_store_contents` method called but never defined** in `scraper.py` line 570 — will throw `AttributeError` at runtime when `run()` is called.
- **Backend Python version mismatch**: CLAUDE.md states Python 3.11, but `backend/Dockerfile` uses `python:3.13-slim`. Either the docs are wrong or there's a version inconsistency. Should be aligned.
- **No `<StrictMode>` wrapper** in `frontend/src/main.tsx` — React 19's StrictMode catches additional hook issues; it was removed at some point.

### Low
- **`express` 4.18.2**: Express v5 was released stable in 2024. v4→v5 has breaking changes but is well-documented. Low priority as v4 still receives security patches.
- **CI/CD deploys to `europe-north1`** but CLAUDE.md says `europe-north2`. The workflow env var `REGION: europe-north1` conflicts with the stated deployment region. May be intentional but worth verifying.
