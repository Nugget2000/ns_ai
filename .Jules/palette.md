## 2026-01-16 - Granular Loading States in Admin Tables
**Learning:** Users managing lists (like admin tables) often perform actions on specific items. Global loading states block the entire UI, while lack of feedback leaves users uncertain. Granular loading states (per-row or per-button) provide immediate feedback without disrupting the workflow.
**Action:** Always implement `isUpdating` or `loadingId` state for list actions, disabling only the relevant item's controls and showing a spinner.
