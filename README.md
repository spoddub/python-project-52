[![CI](https://github.com/spoddub/python-project-52/actions/workflows/ci.yml/badge.svg)](https://github.com/spoddub/python-project-52/actions)
[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=spoddub_python-project-52&metric=sqale_rating)](https://sonarcloud.io/summary/new_code?id=spoddub_python-project-52)

[**Task Manager — live demo on Render**](https://python-project-52-mqpb.onrender.com/)

# Task Manager (Django)

Task Manager is a training web app to manage tasks (users, statuses, labels, tasks) built with Django and server-side rendering (Django Templates + Bootstrap).
It supports sign-up/sign-in, CRUD for all entities, task filtering by status/assignee/label and “only my tasks”, deployment to Render, static files via WhiteNoise, and error monitoring with Rollbar.

---

## This project was built using these tools:

| Tool                                                              | What it’s used for                                                                |
| ----------------------------------------------------------------- | --------------------------------------------------------------------------------- |
| [uv](https://docs.astral.sh/uv/)                                  | Extremely fast Python package manager (replacement for pip/pip-tools/venv/pyenv). |
| [ruff](https://docs.astral.sh/ruff/)                              | Fast Python linter & code formatter.                                              |
| [Django](https://docs.djangoproject.com/en/stable/)               | Web framework with ORM, CBV and templates.                                        |
| [django-bootstrap5](https://github.com/zostera/django-bootstrap5) | Convenient Bootstrap 5 helpers in Django templates.                               |
| [django-filter](https://django-filter.readthedocs.io/)            | Declarative filtering (FilterSet/FilterView).                                     |
| [Gunicorn](https://docs.gunicorn.org/)                            | WSGI server for production.                                                       |
| [WhiteNoise](https://whitenoise.readthedocs.io/)                  | Serving static files in production.                                               |
| [python-dotenv](https://pypi.org/project/python-dotenv/)          | Loading environment variables from `.env`.                                        |
| [dj-database-url](https://pypi.org/project/dj-database-url/)      | Parse `DATABASE_URL` for Postgres/SQLite.                                         |
| [Rollbar](https://docs.rollbar.com/docs/python)                   | Production error monitoring.                                                      |

---

## Installation & Development

### Requirements

- Python ≥ 3.10
- (Optional) `uv` installed globally — see the [docs](https://docs.astral.sh/uv/getting-started/).

### Clone

```bash
git clone https://github.com/spoddub/python-project-52.git
cd python-project-52
```

### Environment variables

Create a `.env` file in the project root (for local dev you only need `SECRET_KEY` and `DJANGO_DEBUG`):

```dotenv
# local development
SECRET_KEY=change-me-local-secret
DJANGO_DEBUG=1

# Example for Postgres (prod):
# DATABASE_URL=postgresql://USER:PASSWORD@HOST:5432/DBNAME

# Optional: Rollbar (prod)
# ROLLBAR_ACCESS_TOKEN=your-post_server_item-token
# ROLLBAR_ENV=production

# You normally do NOT need to set ALLOWED_HOSTS locally.
# If you deploy behind a custom host, you may also add:
# ALLOWED_HOSTS=example.com
# CSRF_TRUSTED_ORIGINS=https://example.com
```

### Local run (SQLite)

```bash
make dev
# creates a .venv, installs deps, runs migrations, starts Django dev server
# app will be available at http://0.0.0.0:8000/
```

### Developer commands

```bash
make lint       # ruff check --fix
make format     # ruff format
make test       # run Django tests (coverage XML for CI is produced in the workflow)
```

---

## Deployment (Render)

In your Render Web Service settings:

- **Build Command:** `make build`
- **Start Command:** `make render-start`

Environment variables on Render:

- `SECRET_KEY` — Django secret key
- `DJANGO_DEBUG=0` — production mode
- `DATABASE_URL` — connection string for your Render PostgreSQL instance
- `ROLLBAR_ACCESS_TOKEN` — Rollbar `post_server_item` token
- `ROLLBAR_ENV=production`
- `RENDER_EXTERNAL_HOSTNAME` — _set automatically by Render_; the app picks it up for `ALLOWED_HOSTS`/CSRF

Static files are collected during the build (`build.sh`) and served by WhiteNoise.

---

## Features

- Server-side rendering (Django Templates + Bootstrap 5), no custom CSS required.
- Authentication and user management (CRUD; a user can edit/delete only their own account).
- Statuses: CRUD, deletion protected if used by tasks.
- Labels: CRUD, many-to-many with tasks, deletion protected if used.
- Tasks: CRUD, author set automatically; only the author can delete.
- Filtering: by status, executor, labels and “only my tasks”.
- Logging & errors: Rollbar middleware; CSRF/SECURE settings for Render.
- SQLite for local development and PostgreSQL in production via `dj-database-url`.

---

## Makefile targets (main)

```make
install          # uv export + uv pip install --system -r requirements.txt
install-local    # create .venv and install dependencies into it
migrate          # apply migrations
collectstatic    # collect static files
run              # run dev server (0.0.0.0:8000)
dev              # install-local + migrate + run
build            # build script for Render (build.sh)
render-start     # start gunicorn on Render
lint             # ruff check --fix
format           # ruff format
test             # Django tests
```

---

## CI & Quality

- **GitHub Actions** runs linting, formatting check, tests with coverage, and SonarCloud analysis.
- **SonarCloud** monitors code quality & coverage of new code. If you fork/rename the project, update the project key in the badges and SonarCloud settings.
