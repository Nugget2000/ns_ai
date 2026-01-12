## 2024-05-22 - Admin Dashboard UX Gaps
**Learning:** Admin interfaces often neglect "delight" and feedback. Synchronous-feeling actions without visual loading states create uncertainty, especially for critical actions like role changes.
**Action:** Always wrap async admin actions with specific loading indicators (spinners on the button pressed) and use non-blocking error notifications (toasts/inline) instead of alerts.
