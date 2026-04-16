---
name: create-feature-verification
description: "Use when implementing or updating a feature and verifying it before marking it done: confirm backend lint/build checks and frontend compile/build checks."
---

# Create Feature With Verification

This skill captures the workflow for implementing a change and verifying it with both backend and frontend checks before declaring it complete.

## When to use

- The task involves code changes in `backend/` and/or `frontend/`
- You need an explicit completion definition that includes verification steps
- You want the agent to validate the implementation by running backend lint/build and frontend compile/build

## Workflow

1. Review the user request and identify affected areas.
   - If the change touches `backend/`, plan backend edits and verification.
   - If the change touches `frontend/`, plan frontend edits and verification.
   - If both areas are affected, perform both validation steps.

2. Create or update the required files.
   - Use repository conventions and existing directory structure.
   - Keep backend and frontend changes separated when appropriate.

3. Verify the backend.
   - Prefer `cd backend && ruff check .` as a first pass.
   - If the backend change includes Python code, also ensure Python syntax/compile validity.
   - If tests are available for the affected backend area, mention them and run the relevant subset.

4. Verify the frontend.
   - Prefer `cd frontend && npm run build` to confirm TypeScript and bundling.
   - If the frontend uses a local dev build step or compile command, use that instead.
   - If there are frontend lint or test commands relevant to the change, mention them.

5. Confirm completion.
   - Describe what changed and why.
   - Report the verification commands run and their results.
   - If either backend or frontend validation failed, do not mark the feature done.

## Decision points

- If `backend/` is untouched, skip backend verification.
- If `frontend/` is untouched, skip frontend verification.
- If the request is ambiguous, ask whether the feature requires backend, frontend, or both.
- If the repo has a dedicated CI command, prefer it after the local checks.

## Quality checklist

- [ ] Backend changes are implemented following repository structure.
- [ ] Backend code passes `ruff` or equivalent lint checks.
- [ ] Backend code is syntactically valid.
- [ ] Frontend changes are implemented following project conventions.
- [ ] Frontend compile/build succeeds (`npm run build` or equivalent).
- [ ] The final summary clearly states the commands used for verification.

## Example prompts

- "Implement this feature and verify it before calling it done: run backend ruff checks and frontend npm build."
- "Add the requested backend API and make sure the frontend still compiles."
- "Update the feature and confirm with both backend linting and frontend build verification."
