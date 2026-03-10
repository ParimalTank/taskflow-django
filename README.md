# TaskFlow - Organization-based Task Management (Kanban Board)

**Live Demo:** [https://taskflow-django-u5xi.onrender.com](https://taskflow-django-u5xi.onrender.com)

A full-stack collaborative task management application built with Django, Django REST Framework, and Supabase (PostgreSQL). Features organization-based team collaboration with role-based access, member invitations, and drag-and-drop Kanban boards.

## Tech Stack

| Layer | Technology |
|-------|-----------|
| **Backend** | Django 6.0 + Django REST Framework |
| **Frontend** | Django Templates + Bootstrap 5 + Bootstrap Icons |
| **Database** | Supabase (PostgreSQL) |
| **Auth** | Django built-in authentication |
| **Fonts** | Google Fonts (Inter) |

## Features

### Organizations & Teams
- **Create Organizations** — Set up team workspaces
- **Role-based Access** — Owner, Admin, and Member roles
- **Invite Members** — Invite users by username with role assignment
- **Accept/Decline Invitations** — Manage pending invites from the dashboard

### Boards & Tasks
- **Project Boards** — Create boards within an organization
- **Kanban View** — Visual columns: To Do, In Progress, Done
- **Drag & Drop** — Move tasks between columns with instant status updates
- **Task Assignment** — Assign tasks to any organization member
- **Priority Levels** — Low, Medium, High with color-coded badges

### General
- **User Authentication** — Register, Login, Logout
- **REST API** — Full CRUD API for boards and tasks
- **Admin Panel** — Django admin for data management
- **Modern UI** — Clean design with glassmorphism navbar, hover animations, responsive layout

## App Flow

```
Register/Login → Organizations List → Create/Select Org → Org Dashboard (Boards + Members)
                                                              ↓
                                                     Select Board → Kanban View → Drag & Drop Tasks
```

## Project Structure

```
django-fe/
├── config/                  # Project configuration
│   ├── settings.py          # Settings (DB, apps, middleware, DRF)
│   ├── urls.py              # Root URL routing
│   └── wsgi.py              # WSGI entry point
├── accounts/                # User authentication
│   ├── forms.py             # Registration form
│   ├── views.py             # Login, Register views
│   └── urls.py              # Auth routes
├── organizations/           # Organizations & team management
│   ├── models.py            # Organization, Membership, Invitation models
│   ├── forms.py             # Org creation & invite forms
│   ├── views.py             # Org CRUD, invite, member management views
│   ├── admin.py             # Admin registration with inlines
│   └── urls.py              # Org routes
├── boards/                  # Project boards
│   ├── models.py            # Board model (linked to Organization)
│   ├── views.py             # Board CRUD views (org-scoped)
│   ├── forms.py             # Board form
│   ├── api_views.py         # Board REST API views
│   ├── serializers.py       # DRF serializers
│   └── urls.py              # Board routes
├── tasks/                   # Tasks within boards
│   ├── models.py            # Task model (status, priority, assignee)
│   ├── views.py             # Task CRUD + drag-and-drop status API
│   ├── forms.py             # Task form (with org member assignment)
│   ├── api_views.py         # Task REST API views
│   ├── serializers.py       # DRF serializers
│   └── urls.py              # Task routes
├── templates/               # HTML templates
│   ├── base.html            # Base layout (navbar, toasts, scripts)
│   ├── accounts/            # Login, Register pages
│   ├── organizations/       # Org list, detail, form, invite pages
│   ├── boards/              # Board list, detail (Kanban), form pages
│   └── tasks/               # Task form, delete confirmation
├── static/css/style.css     # Custom CSS (variables, components, responsive)
├── .env                     # Environment variables (not in git)
├── .env.example             # Example env file
├── requirements.txt         # Python dependencies
└── manage.py                # Django management CLI
```

## Data Models

```
Organization ──< Membership >── User
     │                            │
     └──< Board ──< Task ────────┘ (assigned_to)
                      │
              Invitation (pending/accepted/declined)
```

| Model | Key Fields |
|-------|-----------|
| **Organization** | name, slug, description, created_by |
| **Membership** | user, organization, role (OWNER/ADMIN/MEMBER) |
| **Invitation** | organization, invited_by, invited_user, role, status |
| **Board** | name, description, organization, owner |
| **Task** | title, description, status, priority, board, assigned_to |

## Setup Instructions

### 1. Clone and create virtual environment

```bash
git clone <repo-url>
cd django-fe
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Supabase

1. Go to [Supabase Dashboard](https://supabase.com/dashboard)
2. Create a new project (or use existing)
3. Click **Connect** on the project page and copy the **URI** connection string
4. Copy `.env.example` to `.env` and fill in your credentials:

```bash
cp .env.example .env
# Edit .env with your Supabase DATABASE_URL, SUPABASE_URL, and SUPABASE_KEY
```

### 4. Run migrations

```bash
python manage.py migrate
```

### 5. Create superuser (for admin panel)

```bash
python manage.py createsuperuser
```

### 6. Run the development server

```bash
python manage.py runserver
```

Visit: http://127.0.0.1:8000

## Pages & URL Routes

### Authentication
| URL | Page |
|-----|------|
| `/accounts/register/` | User Registration |
| `/accounts/login/` | User Login |
| `/accounts/logout/` | Logout (POST) |

### Organizations
| URL | Page |
|-----|------|
| `/orgs/` | Organization List + Pending Invitations |
| `/orgs/create/` | Create New Organization |
| `/orgs/<slug>/` | Org Dashboard (Boards tab + Members tab) |
| `/orgs/<slug>/edit/` | Edit Organization (Owner/Admin) |
| `/orgs/<slug>/invite/` | Invite Member by Username |
| `/orgs/invitations/<id>/accept/` | Accept Invitation (POST) |
| `/orgs/invitations/<id>/decline/` | Decline Invitation (POST) |

### Boards (scoped to organization)
| URL | Page |
|-----|------|
| `/orgs/<slug>/boards/` | Board List |
| `/orgs/<slug>/boards/create/` | Create New Board |
| `/orgs/<slug>/boards/<id>/` | Board Detail (Kanban View + Drag & Drop) |
| `/orgs/<slug>/boards/<id>/edit/` | Edit Board |
| `/orgs/<slug>/boards/<id>/delete/` | Delete Board Confirmation |

### Tasks (scoped to organization)
| URL | Page |
|-----|------|
| `/orgs/<slug>/tasks/create/<board_id>/` | Create Task |
| `/orgs/<slug>/tasks/<id>/edit/` | Edit Task |
| `/orgs/<slug>/tasks/<id>/delete/` | Delete Task Confirmation |
| `/tasks/<id>/update-status/` | Update Task Status (AJAX/POST) |

## REST API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/boards/` | List boards (user's orgs) |
| POST | `/api/boards/` | Create a board |
| GET | `/api/boards/<id>/` | Get board details |
| PUT | `/api/boards/<id>/` | Update a board |
| DELETE | `/api/boards/<id>/` | Delete a board |
| GET | `/api/tasks/` | List tasks (user's orgs) |
| POST | `/api/tasks/` | Create a task |
| GET | `/api/tasks/<id>/` | Get task details |
| PUT | `/api/tasks/<id>/` | Update a task |
| DELETE | `/api/tasks/<id>/` | Delete a task |

## Role Permissions

| Action | Owner | Admin | Member |
|--------|-------|-------|--------|
| View boards & tasks | Yes | Yes | Yes |
| Create/edit boards & tasks | Yes | Yes | Yes |
| Invite members | Yes | Yes | No |
| Edit organization | Yes | Yes | No |
| Remove members | Yes | No | No |

## Key Concepts Covered

- **Django MVT Pattern** (Model-View-Template)
- **Django ORM** (Models, ForeignKey relationships, QuerySets, Migrations)
- **Django Forms** (ModelForm, custom validation, dynamic querysets)
- **Django Authentication** (login, register, logout, @login_required)
- **Role-based Access Control** (Owner/Admin/Member permissions)
- **Django REST Framework** (Serializers, Generic Views, API)
- **Template Inheritance** (base.html → child templates with blocks)
- **HTML5 Drag & Drop API** (with AJAX status updates)
- **Supabase as PostgreSQL** (cloud-hosted database)
- **CSRF Protection** (built-in security for forms and AJAX)
- **URL Namespacing** (org-scoped nested URLs)
- **Data Migrations** (handling schema changes with existing data)
