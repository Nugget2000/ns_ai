## 2024-05-22 - Login Loading State & Decorative Icons
**Learning:** Even small visual cues like a spinner significantly improve perceived performance and trust during authentication. Decorative SVGs used alongside text must be hidden from screen readers (`aria-hidden="true"`) to prevent "image, image" announcements that clutter the auditory experience.
**Action:** Always pair async action buttons with a visual loading indicator (spinner) and ensure purely decorative icons are explicitly hidden from assistive technology.
