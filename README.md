# catalog

DevOps course work 2026.

A RESTful API for managing a book catalog, built as part of the Continuous Assessment (CA) for the Diploma in DevOps at CCT College. The project is a web service named `bookcatalog` with a fully automated delivery pipeline: containerised with Docker, tested and built via GitHub Actions, and deployed to Kubernetes with Helm using a GitOps workflow (ArgoCD).

## Tech stack

* **Python 3.13** (Docker image) — web app
* **Django 5.2** & **Django REST Framework** — web framework and API layer
* **uv** — ultra-fast Rust-based Python package and project manager
* **PostgreSQL 17** — database (Docker Compose / production via Bitnami Helm chart)
* **SQLite** — development database (`db.sqlite3`, used when `DEVELOPMENT_MODE=true`)
* **pytest** + **pytest-django** — integration test suite
* **Docker** & **Docker Compose** — containerisation and local development stack
* **GitHub Actions** — CI/CD (tests, image build, automated Helm configuration update)
* **Kubernetes (K3d)** & **Helm** — local cluster and deployment chart
* **ArgoCD** — GitOps continuous deployment

## Project structure

```
catalog/
├── pyproject.toml           # Python dependencies and project metadata
├── uv.lock                  # Strictly pinned dependency versions
├── Dockerfile               # App container image (python:3.13-slim)
├── entrypoint.sh            # Container entrypoint: run migrations and start server
├── docker-compose.yml       # Local stack: app + PostgreSQL 17
├── pytest.ini               # pytest-django configuration
├── bookcatalog/             # Project configuration package (settings, core urls)
│   └── settings.py          # Settings; env-driven DB selection (SQLite vs Postgres)
├── api/                     # Application: the REST API
│   ├── models.py            # Book model (Title, Author, ISBN, Published Date)
│   ├── serializers.py       # Data validation layer
│   ├── views.py             # API endpoints logic
│   ├── urls.py              # /api/books/ routes
│   └── tests/               # Automated integration tests
├── books-catalog-chart/     # Helm chart for Kubernetes deployment
│   ├── Chart.yaml           # Chart metadata and PostgreSQL dependency
│   ├── values.yaml          # Default values (image tag updated by CI)
│   └── templates/           # K8s manifests: Deployment, Service, Ingress,
│                            # ConfigMap, and a Job for database migrations
└── .github/
    ├── workflows/main.yml   # CI/CD pipeline definition
    └── actions/             # Shared composite action (uv setup + install deps)

```

## The API

The `api` app exposes a book catalogue backed by the `Book` model (`title`, `author`, `isbn`, `published_date`):

| Method | Path | Description |
| --- | --- | --- |
| GET | `/api/books/` | List all books in the database |
| POST | `/api/books/` | Create a new book (with input validation) |

## Configuration

Settings are dynamically read from the environment via `environs`:

| Variable | Default | Purpose |
| --- | --- | --- |
| `DEVELOPMENT_MODE` | `true` | `true` → SQLite; `false` → PostgreSQL |
| `DATABASE_NAME` | `""` | Postgres database name |
| `DATABASE_USER` | `""` | Postgres user |
| `DATABASE_PASSWORD` | `""` | Postgres password |
| `DATABASE_HOST` | `""` | Postgres host (port is fixed at 5432) |

## Prerequisites

Before running this project, ensure you have the following installed on your machine:

* **Git**: For version control.
* **Docker & Docker Compose**: For containerisation and local database stack.
* **uv**: An ultra-fast Python package manager (required for local development without Docker).

## Getting Started

First, clone the repository to your local machine and navigate into the project directory:

```
git clone https://github.com/YOUR_GITHUB_USERNAME/catalog.git
cd catalog

```

## Running locally

### With the virtual environment (SQLite)

```
# Create the virtual environment and sync dependencies from uv.lock
uv sync

# Apply database migrations
uv run manage.py migrate

# (Optional) Create an admin user to access the Django admin panel
uv run manage.py createsuperuser

# Start the development server
uv run manage.py runserver

```

The app will be available at [http://127.0.0.1:8000/api/books/](http://127.0.0.1:8000/api/books/), and the admin site at [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/).

### With Docker Compose (PostgreSQL)

```
docker compose up --build

```

This starts the app alongside a PostgreSQL 17 container. The `entrypoint.sh` automatically applies migrations before starting the server. The API will be available at [http://127.0.0.1:8000/api/books/](http://127.0.0.1:8000/api/books/).

### Tests

```
uv run pytest

```

### GitOps Deployment (Local Cluster)

To replicate the production-like Kubernetes deployment locally using GitOps:

1. Provision a local Kubernetes cluster (e.g., using `k3d`).
2. Install ArgoCD into the cluster.
3. In the ArgoCD UI, create a new Application pointing to this GitHub repository and the `books-catalog-chart/` directory.

ArgoCD will automatically download the Bitnami PostgreSQL dependency, execute the database migrations via a Kubernetes Job, and spin up the Django application.

## CI/CD Pipeline

On pushes to the `main` branch, the GitHub Actions workflow (`.github/workflows/main.yml`) executes the following automated pipeline:

1. **test** — Uses a custom composite action to instantly install `uv` and dependencies, then runs the integration tests.
2. **build-and-push** — If tests pass, builds the Docker image and pushes it to GitHub Container Registry (`ghcr.io`) tagged with the unique commit hash (`github.sha`).
3. **update-helm** — Automatically updates the `image.tag` value in `books-catalog-chart/values.yaml` to the new commit hash and commits this change back to the repository.

## Kubernetes Deployment & GitOps

The `books-catalog-chart/` Helm chart deploys the API application along with a dependent Bitnami PostgreSQL database.

* **Database Migrations**: Database migrations are handled by a standard Kubernetes `Job` with a `restartPolicy: OnFailure`. This ensures the migration script safely waits for the PostgreSQL StatefulSet to become healthy without causing ArgoCD synchronization conflicts (avoiding problematic Helm Hooks).
* **ArgoCD (Continuous Deployment)**: ArgoCD continuously monitors the `main` branch. Whenever the CI pipeline updates the image tag in `values.yaml`, ArgoCD detects the configuration drift and automatically synchronizes the Kubernetes cluster, pulling the new image and rolling out the updated pods without manual intervention.

## CA Notes

* **Environment Bypass**: The entire project was developed within a native Linux VM (Ubuntu Server) via VirtualBox to ensure flawless Docker and K3d compatibility, bypassing Windows 11 Hyper-V limitations.