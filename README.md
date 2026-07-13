# Catalog

**Catalog** is a Django project created as part of a DevOps coursework assignment.

## Project overview

This repository contains a basic Django 6 application with Django REST Framework prepared for building a book catalog API.

Key features:

- Django project: `bookcatalog`
- Application: `api`
- REST framework enabled via `djangorestframework`
- Local SQLite database: `db.sqlite3`

## Repository structure

- `manage.py` — Django management command entry point
- `bookcatalog/` — Django project configuration
- `api/` — application for API logic
- `db.sqlite3` — SQLite database file
- `pyproject.toml` — project metadata and dependencies
- `README.md` — project documentation

## Installation

1. Make sure Python 3.12+ is installed.
2. Open a terminal and go to the project folder:
   ```bash
   cd d:/Documents/IT/cct/DevOps/catalog
   ```
3. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```
4. Install dependencies:
   ```bash
   pip install django djangorestframework
   ```

## Run the project

1. Apply database migrations:
   ```bash
   python manage.py migrate
   ```
2. Start the development server:
   ```bash
   python manage.py runserver
   ```
3. Open the application in a browser:
   ```text
   http://127.0.0.1:8000/
   ```

## Current state

- The project is configured with Django and Django REST Framework.
- The `api` app currently contains placeholder files and no defined models or API endpoints.
- The URL configuration in `bookcatalog/urls.py` only includes the Django admin route.

## Next steps

- Add models for books, authors, and categories in `api/models.py`.
- Create serializers and views for the REST API.
- Register API routes in `bookcatalog/urls.py`.
- Write tests in `api/tests.py`.

## Note

The `main.py` file contains a simple test script and is not part of the main Django application.
