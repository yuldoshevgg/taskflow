# TaskFlow – Task Management Application

A Django-based task management web application deployed with Docker, PostgreSQL, and Nginx.

## Features

- User authentication (register, login, logout)
- Task CRUD (Create, Read, Update, Delete)
- Task categories with colour labels
- Filter tasks by status (To Do / In Progress / Done)
- Priority levels (Low / Medium / High)
- Django admin panel
- CI/CD via GitHub Actions

## Tech Stack

| Layer       | Technology                 |
|-------------|----------------------------|
| Backend     | Django 4.2, Gunicorn       |
| Database    | PostgreSQL 15              |
| Reverse proxy | Nginx                    |
| Containerisation | Docker, Docker Compose |
| CI/CD       | GitHub Actions             |

## Database Models

- **Category** – name, colour, created_by (FK → User)
- **Task** – title, description, status, priority, due_date, category (FK → Category), created_by (FK → User)

## Local Setup (Docker)

```bash
# Clone the repo
git clone <repo-url>
cd taskflow

# Copy and edit environment variables
cp .env.example .env
# Edit .env with your values

# Build and start all services
docker compose up --build -d

# Create a superuser
docker compose exec web python manage.py createsuperuser

# Visit the app
open http://localhost
```

## Running Tests Locally

```bash
cd app
pip install -r requirements.txt
# Set env vars (see .env.example)
pytest tasks/tests.py -v
```

## CI/CD Pipeline

On every push to `main`:
1. Runs all pytest tests against a real PostgreSQL container
2. Builds the Docker image
3. Pushes to Docker Hub (requires `DOCKERHUB_USERNAME` and `DOCKERHUB_TOKEN` secrets)

## Environment Variables

| Variable      | Description                        |
|---------------|------------------------------------|
| `SECRET_KEY`  | Django secret key                  |
| `DEBUG`       | True for development, False in prod|
| `ALLOWED_HOSTS` | Comma-separated allowed hosts    |
| `DB_NAME`     | PostgreSQL database name           |
| `DB_USER`     | PostgreSQL username                |
| `DB_PASSWORD` | PostgreSQL password                |
| `DB_HOST`     | Database host (use `db` in Docker) |
| `DB_PORT`     | PostgreSQL port (default 5432)     |
