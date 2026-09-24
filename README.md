# Saree App

A work-in-progress saree shop application built with FastAPI, Jinja2 templates, SQLAlchemy, and SQLite.

The current version contains an admin login, product management pages, saree categories, image uploads, product editing, product deletion, and a local SQLite database. The application is still under development and is not ready for production use.

## Requirements

- Python 3.10 or newer
- PowerShell on Windows, or an equivalent shell on macOS/Linux

## Setup

From the project root, create and activate a virtual environment:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

Install the Python dependencies:

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Create a `.env` file in the project root. Do not commit this file:

```env
ADMIN_EMAIL=your-admin-email@example.com
ADMIN_PASSWORD=change-this-password
SESSION_SECRET=replace-with-a-long-random-secret
```

Use a long, unpredictable value for `SESSION_SECRET`. The values in `.env` are loaded when the application starts.

## Run the application

Start the development server from the project root:

```powershell
uvicorn app.main:app --reload
```

Open the application at:

- http://127.0.0.1:8000/
- http://127.0.0.1:8000/admin/login

The first application start creates the local `test.db` SQLite database and the `products` table automatically. Uploaded product images are stored under `uploads/products/`.

## Current workflow

1. Open `/admin/login`.
2. Sign in with the credentials from `.env`.
3. Open the admin dashboard.
4. Add a product with its name, saree category, description, price, stock, and image.
5. View, edit, or delete products from the product management page.

## Project structure

```text
app/
  main.py                 FastAPI application entry point
  database.py             SQLite engine and SQLAlchemy session
  core/
    auth.py               Admin session check
    config.py             Environment configuration
  models/
    product.py            Product database model
  routers/
    admin.py              Admin and product routes
  templates/              Jinja2 HTML templates
uploads/products/         Uploaded product images
```

## Development status

This is an early development version. Before production use, the project still needs security hardening, validation and error handling, tests, a production database configuration, safer image handling, and a customer-facing storefront or API. The current local database, uploaded files, and secret configuration are intentionally ignored by Git.

## Useful commands

Compile the Python application files:

```powershell
python -m compileall -q app
```

Run the development server with auto-reload:

```powershell
uvicorn app.main:app --reload
```
