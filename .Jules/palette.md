# Palette's Journal

## 2025-02-18 - Accessibility of Dynamic Error Messages
**Learning:** Dynamic error messages in this app (like in login forms) were implemented as simple divs, making them invisible to screen readers when they appear.
**Action:** Always wrap dynamic error feedback in `role="alert"` with `aria-live="polite"` to ensure assistive technology announces the error immediately.
