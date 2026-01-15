## 2024-05-22 - Granular Loading States in Lists
**Learning:** Using global loading states for actions in lists (like tables) provides poor feedback. Users don't know which item is updating.
**Action:** Implement granular loading states (e.g., `actionLoading[id]`) to show spinners on specific buttons while keeping the rest of the UI interactive but protected from race conditions.
