<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:0f0f14,50:1b1b23,100:f5a623&height=180&section=header&text=DocsApp&fontSize=65&fontColor=ffffff&fontAlignY=38&desc=Lightweight%20Collaborative%20Document%20Editor&descAlignY=58&descColor=f5a623&animation=fadeIn" width="100%"/>

<br/>

[![Django](https://img.shields.io/badge/Django-5.2-092E20?style=for-the-badge&logo=django&logoColor=white)](https://djangoproject.com)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Postgres](https://img.shields.io/badge/Neon-Postgres-00E599?style=for-the-badge&logo=postgresql&logoColor=white)](https://neon.tech)
[![Quill](https://img.shields.io/badge/Quill.js-Rich_Text-f5a623?style=for-the-badge&logo=quill&logoColor=white)](https://quilljs.com)

<br/>

**DocsApp** is a Google Docs-inspired collaborative document editor — create, format, share, and persist documents with a real Postgres backend, built for the Ajaia AI-Native assessment.

**Live Demo:** https://docs-81gt.onrender.com
*(free-tier hosting — first load may take 30–60s to wake up)*

</div>

---

## 🔑 Test Credentials

| Username | Password   |
|----------|------------|
| alice    | alice123   |
| bob      | bob123     |
| charlie  | charlie123 |

Or sign up for a new account directly from the login page.

---

## 🗺️ User Flow

```mermaid
flowchart LR
    A([🌐 Visit Site]) --> B{Logged in?}
    B -->|No| C([🔐 Login / Signup])
    B -->|Yes| D([📋 Dashboard])
    C --> D
    D --> E([📄 My Documents])
    D --> F([👥 Shared With Me])
    D --> G([➕ New Document])
    D --> H([📤 Upload .txt/.md])
    E --> I([✏️ Editor])
    F --> I
    G --> I
    H --> I
    I --> J([🎨 Format: bold/italic/lists/color/image])
    I --> K{Owner?}
    K -->|Yes| L([🔗 Share with user])
    K -->|No| M([👁️ Read-only access])
    L --> N([💾 Auto-save to Postgres])
    M --> N
```

---

## 🗄️ Database Schema

```mermaid
erDiagram
    User ||--o{ Document : "owns"
    User ||--o{ SharedAccess : "granted access via"
    Document ||--o{ SharedAccess : "shared through"

    User {
        int id PK
        string username
        string password
        string email
    }
    Document {
        int id PK
        string title
        text content "HTML from Quill"
        int owner_id FK
        datetime created_at
        datetime updated_at
    }
    SharedAccess {
        int id PK
        int document_id FK
        int shared_with_id FK
        datetime granted_at
    }
```

**Access control logic:** a user can open `/document/<id>/` if they are the `owner` OR have a matching `SharedAccess` row. Only the owner can edit content or create new shares — enforced at the view level on every POST.

---

## ✨ Features

| Feature | Details |
|---|---|
| **Document Editing** | Create, rename, edit — rich text via Quill.js (bold, italic, underline, headings, lists, text/background color, image embed) |
| **File Upload** | `.txt` / `.md` → instantly becomes a new editable document |
| **Sharing** | Owner grants access to other users; dashboard separates "My Documents" vs "Shared With Me" |
| **Persistence** | Neon Postgres — documents & shares survive refreshes and redeploys |
| **Auth** | Manual signup/login (no OAuth), seeded demo users included |

---

## ⚙️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | Django 5.2 (server-rendered templates) |
| Editor | Quill.js 1.3.6 (CDN) |
| Database | PostgreSQL (Neon, serverless) |
| Deployment | Render (Gunicorn) |
| Auth | Django's built-in `User` model + session auth |

---

## 🚀 Local Setup

```bash
# 1. Clone the repo
git clone https://github.com/life2-byte/Docs
cd Docs

# 2. Create virtual environment & install dependencies
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt

# 3. Create a .env file in the project root
DBNAME=your_neon_db_name
DBUSER=your_neon_user
DBPASSWORD=your_neon_password
DB_HOST=your_neon_host
DB_PORT=5432

# 4. Run migrations
python manage.py migrate

# 5. (Optional) seed demo users
python manage.py shell
>>> from django.contrib.auth.models import User
>>> User.objects.create_user(username='alice', password='alice123')
>>> User.objects.create_user(username='bob', password='bob123')
>>> User.objects.create_user(username='charlie', password='charlie123')

# 6. Run the server
python manage.py runserver
# Visit → http://127.0.0.1:8000/
```

---

## ✅ Running Tests

```bash
python manage.py test documents
```

14 automated tests covering model creation, access control (owner vs. shared vs. unauthorized), document editing, sharing logic, and file upload validation.

---

## 🚧 Known Limitations / Scope Cuts

- File upload supports **only `.txt` and `.md`** — not `.docx`/`.pdf` (kept scope focused per assignment guidance)
- Sharing is binary (has access / no access) — no granular view-only vs. edit permissions
- No real-time collaboration (single-editor-at-a-time model)
- Tables are not supported in the rich-text editor (Quill's core doesn't include this without a heavier plugin)

## 🛣️ What I'd Build Next (2–4 more hours)

- [ ] Granular sharing permissions (view-only vs. edit)
- [ ] Real-time collaborative cursors (WebSockets/Django Channels)
- [ ] Document version history
- [ ] Export to PDF/Markdown

---

<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:f5a623,100:0f0f14&height=100&section=footer" width="100%"/>

Built for the Ajaia AI-Native Full Stack Developer Assessment

</div>
