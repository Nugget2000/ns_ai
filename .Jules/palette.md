## 2026-01-21 - Granular Loading States in Admin Tables
**Learning:** When adding loading states to tables with row-specific actions (like "Approve" user), it's critical to track the specific ID being acted upon. Using a global `loading` state disables all rows, which is bad UX. Using local state `{ uid: string, role: string }` allows granular disabling and spinner display on the exact button clicked while preventing race conditions on the same item.
**Action:** Always use an identifier-based state for async list actions, not a boolean.
