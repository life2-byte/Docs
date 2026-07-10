# Submission — DocsApp (Ajaia AI-Native Full Stack Developer Assignment)

## Live Product URL
https://docs-81gt.onrender.com
*(free-tier hosting — first load may take 30–60s to wake up)*

## Test Credentials
| Username | Password   |
|----------|------------|
| alice    | alice123   |
| bob      | bob123     |
| charlie  | charlie123 |

New accounts can also be created directly from the login page's signup form.

## Walkthrough Video
[ADD VIDEO LINK HERE]

## What's Included in This Submission

- **Source code** — full Django project (`documents/` app + `docsapp/` project)
- **README.md** — setup, run instructions, tech stack, data model diagram
- **ARCHITECTURE.md** — what was prioritized, what was cut, and why
- **AI_WORKFLOW.md** — AI tools used, what sped things up, what was rejected/changed,
  and how correctness was verified
- **SUBMISSION.md** — this file
- **documents/tests.py** — 14 automated tests (model, access control, edit, sharing, upload)

## What's Working

- Document creation, renaming, and rich-text editing (bold, italic, underline,
  headings, bulleted/numbered lists, text/background color, inline image embed)
- Auto-save on edit (debounced), with a visible "Saved" indicator
- File upload for `.txt` and `.md` files, converted into new editable documents
- Sharing: owners can grant access to other registered users; dashboard clearly
  separates "My Documents" from "Shared With Me"
- Access control enforced server-side (non-owners cannot edit or re-share;
  unrelated users cannot view a document at all)
- Persistence via Neon Postgres — confirmed to survive refreshes and redeploys
- Manual signup/login (seeded users also provided)
- Live deployment on Render, automated test suite passing

## What's Incomplete / Out of Scope (by design)

- File upload does not support `.docx` or `.pdf` — only `.txt`/`.md`, clearly
  stated in the UI and README
- Sharing is binary access only (no view-only vs. edit permission levels)
- No real-time collaborative editing (single active editor per document)
- No table support in the rich-text editor

## What I'd Build Next (With Another 2–4 Hours)

- Granular sharing permissions (view-only vs. edit)
- Document version history
- Real-time collaboration indicators (WebSockets/Django Channels)
- Export to PDF/Markdown
