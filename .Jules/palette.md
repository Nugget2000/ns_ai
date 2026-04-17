## 2024-05-21 - Async Button Feedback Pattern
**Learning:** Several key interaction points (Login, Admin actions) lacked visual feedback for async states, relying only on text changes or nothing at all. This creates uncertainty.
**Action:** Standardize on the `<Loader2 className="spinner" />` pattern next to text for all async buttons to provide consistent, accessible feedback.

## 2024-05-22 - Granular Async Button Feedback
**Learning:** List item actions (like table rows) require isolated loading states so users know *which* item is processing, rather than relying on a global spinner or silent failure/success. Disabling the specific action buttons dynamically avoids duplicate clicks in flight.
**Action:** Always maintain a granular async state (e.g., `updatingId`) when managing lists with individual action buttons, and apply `aria-busy` and `.spinner` feedback directly to the triggered button.
