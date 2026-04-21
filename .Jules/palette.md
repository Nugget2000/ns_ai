## 2024-05-21 - Async Button Feedback Pattern
**Learning:** Several key interaction points (Login, Admin actions) lacked visual feedback for async states, relying only on text changes or nothing at all. This creates uncertainty.
**Action:** Standardize on the `<Loader2 className="spinner" />` pattern next to text for all async buttons to provide consistent, accessible feedback.

## 2024-05-22 - Granular Async Button Feedback
**Learning:** List item actions (like table rows) require isolated loading states so users know *which* item is processing, rather than relying on a global spinner or silent failure/success. Disabling the specific action buttons dynamically avoids duplicate clicks in flight.
**Action:** Always maintain a granular async state (e.g., `updatingId`) when managing lists with individual action buttons, and apply `aria-busy` and `.spinner` feedback directly to the triggered button.

## 2023-10-27 - [SessionDetailModal Accessibility Improvements]
**Learning:** Adding accessibility to a custom modal is essential. We must implement base accessibility primitives including `role='dialog'`, `aria-modal='true'`, an `aria-labelledby` linking to the title, an `aria-label` on the close button, and an `Escape` key event listener for keyboard closure to allow proper use by screen readers and keyboard navigation.
**Action:** When creating new modals, always use semantic ARIA roles and labels, and provide `Escape` key to close functionality.
## 2024-03-24 - explicit ARIA states and keyboard shortcut tooltips in custom chat interfaces
**Learning:** Custom chat interfaces often miss critical UX/accessibility features that standard form elements provide automatically. Adding `aria-label`, `aria-busy`, and `title` attributes (for keyboard shortcut hints like "Press Enter to send") drastically improves usability for screen reader and keyboard-only users by providing explicit state feedback and discovering shortcuts.
**Action:** Always include explicit ARIA labels, `aria-busy` states on loading buttons, and keyboard shortcut hints via `title` attributes on custom input components to ensure a fully accessible and intuitive interaction.
