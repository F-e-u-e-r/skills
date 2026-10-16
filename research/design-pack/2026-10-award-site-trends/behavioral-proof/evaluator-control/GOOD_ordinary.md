# Design review — internal B2B SaaS settings page (team billing + notification preferences)

Reviewing the proposed visual approach against the design doctrine.

Concrete problems:
- The full-viewport animated WebGL hero is decorative spectacle behind a utilitarian form; it adds GPU cost and distraction with no compositional purpose on a settings page. ANTISLOP-2008 gates such devices to an explicitly agency / Awwwards / experimental brief; an internal billing + notification settings page is ordinary product UI and does not meet that gate.
- Laying the setting groups out as a horizontal / spatial room-to-room scroll fights the task: users scan and edit discrete fields; spatial scroll hides controls and breaks find-in-page, keyboard order, and deep-linking.
- The forced dark-only theme removes user/system preference and is not implied by any palette heuristic; COLOR-1001 is about a disciplined accent on a chosen field, not a mandated dark mode.
- ~700ms ease-in-out cinematic motion on every toggle and tab exceeds the motion budget; control feedback should be short (~150–200ms). Long motion on a settings control degrades perceived responsiveness.
- The frosted-glass blur panels floating over the hero are decorative glass; STRUCT-1009 says avoid blur/glass, and it harms text contrast over a busy animated background.
- None of these devices communicate state or serve a composition — they are spectacle imported into ordinary product UI, which the doctrine explicitly says are "never defaults for ordinary product or app UI."

The accessibility / performance floor (reduced-motion, contrast, keyboard operability) is actively harmed by this approach. This is an ordinary internal tool; it should use a restrained, conventional settings layout.

CONTEXT-FIT: NOT-OK
