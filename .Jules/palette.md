## 2024-12-28 - Login Page UX & Code Health
**Learning:** React 19 + Vite 6 + ESLint 9 is a strict combination. Specifically, `eslint-plugin-react-hooks` flags floating promises in `useEffect` (requiring `void` operator) and `react-refresh` forbids exporting non-components from files with components.
**Action:** When fixing lint errors in this stack, explicitly mark promises as void in effects (`void asyncFn()`) and split hooks/utils into separate files from components or suppress the specific refresh warning if refactoring is out of scope.

**Learning:** Accessibility "micro-wins" are high impact. Adding `role="alert"` and `aria-live` to error messages makes a silent UI state change immediately apparent to screen readers with minimal code.
**Action:** Always check dynamic error messages for `role="alert"`.
