## 2024-05-22 - Admin Table Actions
**Learning:** Admin interfaces with row-level actions often lack granular loading states, causing user uncertainty and potential double-submissions.
**Action:** When implementing list-based actions, always track the specific `itemId` (and action type) in the loading state, and use this to show a spinner on the specific trigger element while disabling others.
