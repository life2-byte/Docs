# Architecture Note — DocsApp

## What I Prioritized

Given the 4–6 hour timebox, I made these deliberate calls early on:

1. **Server-rendered Django templates over a separate React frontend.**
   A split frontend/backend setup would have cost 30–45 extra minutes on CORS, API
   serialization, and two deployment targets — with no real benefit for this scope.
   Django templates + Quill.js (via CDN) got a working rich-text editor in front of
   reviewers faster, which mattered more than showcasing a modern SPA stack.

2. **Postgres (Neon) over SQLite from the start.**
   SQLite is fine for local dev, but most free hosts (Render included) use an
   ephemeral filesystem — a SQLite file would reset on every redeploy or restart.
   Since persistence is an explicit grading criterion, I paid the small extra setup
   cost of Neon upfront rather than risk losing documents mid-review.

3. **Two models instead of a complex permission system.**
   `Document` (with an `owner` FK) and `SharedAccess` (a join table between
   `Document` and `User`) is the minimum structure that satisfies "owner vs
   shared" access control. I explicitly did not build role-based permissions
   (viewer/editor/admin) — the assignment allows this ("does not need to be
   enterprise-grade"), and adding granular roles would have eaten into time
   better spent on deployment and testing.

4. **Access control enforced at the view layer, not just the UI.**
   Every document view checks `is_owner` or a matching `SharedAccess` row
   server-side before rendering or accepting edits. A non-owner POST to the
   edit endpoint is rejected with a 403, not just hidden in the UI. This was a
   deliberate choice — hiding a button is not access control.

5. **Seeded users + lightweight signup over OAuth.**
   The assignment explicitly permits "seeded accounts, mocked auth, or a
   lightweight login flow." Google OAuth would have added real setup overhead
   (console config, redirect URIs, consent screens) for zero product value in
   this scope, so I used Django's built-in `User` model with three seeded
   accounts (alice/bob/charlie) plus a simple manual signup form.

## What I Deliberately Cut

- **File upload limited to `.txt` and `.md`.** Parsing `.docx` or `.pdf` reliably
  (preserving structure, not just raw text) is a nontrivial side quest. Given the
  assignment's own guidance ("prioritize depth in a few important areas over
  shallow coverage everywhere"), I kept upload simple and documented the
  limitation clearly in the UI and README rather than half-supporting more
  formats.
- **No granular sharing permissions** (view-only vs. edit) — binary access only.
- **No real-time collaboration** — single editor at a time, last write wins on
  save. Real collaborative editing (OT/CRDT) is a multi-day problem on its own.
- **No table support in the editor** — Quill's core doesn't include tables
  without a heavier plugin (`quill-better-table`), and it wasn't worth the
  integration risk for the time remaining.

## Data Model

```
User (Django built-in)
  ├── owner FK on Document        → one owner, many owned documents
  └── shared_with FK on SharedAccess → many-to-many share relationship

Document: id, title, content (HTML), owner, created_at, updated_at
SharedAccess: id, document FK, shared_with FK, granted_at
  (unique_together on document + shared_with — prevents duplicate shares)
```

## What I'd Build Next (2–4 more hours)

- Granular view/edit permissions on shares
- Document version history (simple snapshot table would go a long way)
- WebSocket-based presence/live-cursor indicators
- Export to PDF/Markdown
