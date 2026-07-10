# AI Workflow Note — DocsApp

## Which AI Tools I Used

Claude (Anthropic), used conversationally throughout the build — planning the
schema, generating Django views/models/templates, and debugging errors.

## Where AI Materially Sped Up My Work

- **Boilerplate generation.** Models, views, URL wiring, and the initial Quill.js
  editor integration were scaffolded by AI in minutes rather than the 30–45
  minutes it would normally take to write and cross-check by hand. This bought
  back time for testing and deployment.
- **Frontend styling.** I described the visual direction (dark theme, navy
  background, amber accent, card-based dashboard) once and got three
  consistent, polished templates (login, dashboard, editor) instead of manually
  writing CSS from scratch.
- **Test suite authoring.** A 14-case Django test suite covering model
  creation, access control (owner/shared/unauthorized), edit permissions, and
  file upload validation was generated quickly, which meant I had actual test
  coverage instead of skipping tests under time pressure — a common casualty
  in take-home assignments.
- **Error triage.** Stack traces (NoReverseMatch, template path mismatches,
  a syntax typo in `ALLOWED_HOSTS`) were diagnosed and fixed fast by pasting the
  traceback directly rather than manually tracing through each file.

## What AI-Generated Output I Changed or Rejected

- **Save endpoint mismatch.** The generated view initially read saved content
  via `request.POST`, but the editor's JS was sending `JSON.stringify(...)` in
  the request body. This meant saves silently no-op'd — the UI showed "Saved"
  but nothing actually persisted. I caught this by manually testing the save
  flow (type → refresh → content gone), traced it to the content-type
  mismatch, and had the view switched to parse `json.loads(request.body)`
  instead of trusting the first version.
- **Non-owner edit path.** The first version of `edit_document` didn't
  distinguish "can view" from "can edit" on POST — a shared (non-owner) user
  could technically hit the save endpoint. I added an explicit `is_owner` check
  returning 403 before any write happens, and added a test
  (`test_non_owner_cannot_edit_document`) specifically to lock this in.
- **Requirements file.** Rather than accept a blind `pip freeze` (which would
  have dumped every package on the system, including unrelated global
  installs), I asked for a hand-picked list of only the packages this project
  actually imports.
- **Scope suggestions I declined.** AI suggested optional additions (PDF/DOCX
  upload parsing, table support in the editor, Google OAuth) at various
  points. I explicitly turned these down given the assignment's own guidance
  to prioritize depth over breadth and given the time remaining — these are
  called out as conscious cuts in the architecture note rather than silently
  dropped.

## How I Verified Correctness, UX Quality, and Implementation Reliability

- **Manual end-to-end testing** of the full flow after every major change:
  login as alice → create document → format text → save → refresh (confirm
  persistence) → share with bob → log in as bob → confirm read-only access →
  log in as an unrelated third seeded user → confirm the document is
  correctly inaccessible.
- **Automated tests** (`python manage.py test documents`, 14 passing) covering
  the access-control matrix specifically, since that's the part most likely to
  have a silent security bug (e.g., a non-owner being able to write).
- **Live deployment smoke test** on Render after each deploy — logging in with
  seeded accounts and re-running the sharing flow against the real Postgres
  (Neon) instance, not just local SQLite/dev settings, to catch environment-
  specific issues (which is exactly how the `ALLOWED_HOSTS` syntax error and a
  template path mismatch were caught).

I used AI extensively for generation and drafting, but every save/access-control
decision was manually tested against the actual running app before being
considered "done" — the bugs listed above were only caught because I ran the
real flow, not because the code looked correct on paper.
