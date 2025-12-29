## 2025-05-21 - Login Page UX Polish
**Learning:** Adding `role="alert"` to dynamically rendered error containers is a critical but often overlooked accessibility pattern. Screen readers often miss error messages that appear without focus management or ARIA roles.
**Action:** Always add `role="alert"` to error message containers that appear after a user action.
