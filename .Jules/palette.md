## 2024-05-21 - Async Button Feedback Pattern
**Learning:** Several key interaction points (Login, Admin actions) lacked visual feedback for async states, relying only on text changes or nothing at all. This creates uncertainty.
**Action:** Standardize on the `<Loader2 className="spinner" />` pattern next to text for all async buttons to provide consistent, accessible feedback.
