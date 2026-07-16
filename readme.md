# Business Case Improvement Application

This repository contains the **Develop a Business Case Application**, designed to help teams within MHCLG (Ministry of Housing, Communities & Local Government) assess, triage, and build business cases.

---

## Prerequisites

To run this application locally, you will need the following tools installed on your system:

- **Python**: `^3.12`
- **Poetry**: For managing Python dependencies and virtual environments.
- **Node.js & npm**: Required to fetch and prepare HMRC Frontend static assets.
- **Docker & Docker Compose**: (Optional but highly recommended) For running PostgreSQL, pgAdmin, or the complete application stack containerized.
- **Make**: (Optional) For running shortcuts defined in the `Makefile`.

---

## Getting Started

Follow these steps to set up and run the application in your local development environment.

### 1. Clone the Repository

```bash
git clone <repository-url>
cd business-case-improvement-app
```

### 2. Configure Environment Variables

Create a local `.env` file from the provided example:

```bash
cp .env.example .env
```

Ensure the settings in `.env` (such as `SECRET_KEY`) are configured as needed for local development.

### 3. Install Dependencies & Setup Assets

The project uses a Makefile helper to perform a clean setup of frontend assets (HMRC and GOV.UK Frontend) and Node dependencies.

Run the setup task:

```bash
make setup
```

*Note: This command is destructive for the local `./static` folder. It will install npm dependencies, move HMRC assets to the correct static locations, and run `scripts/setup_govuk_frontend.py` to retrieve GOV.UK Frontend templates and assets.*

If you do not have `make` installed, you can perform the setup steps manually:
1. Install Python dependencies:
   ```bash
   poetry install
   ```
2. Install npm dependencies:
   ```bash
   npm install
   ```
3. Copy HMRC frontend assets:
   ```bash
   mkdir -p static/hmrc-frontend
   mv ./node_modules/hmrc-frontend/hmrc/govuk ./static/govuk
   mv ./node_modules/hmrc-frontend/hmrc-frontend-*.min.css ./static/hmrc-frontend/hmrc-frontend.min.css
   ```
4. Run the GOV.UK Frontend download & setup script:
   ```bash
   poetry run python scripts/setup_govuk_frontend.py
   ```

### 4. Database Migrations

Apply the database migrations to set up your local database:

```bash
poetry run python manage.py migrate
```

### 5. Start the Development Server

Start the local Django server:

```bash
poetry run python manage.py runserver 8080
```

The application will be accessible at [http://localhost:8080/](http://localhost:8080/).

---

## Running with Docker

You can run the entire application, including a PostgreSQL database and pgAdmin, using Docker Compose.

- **Start all core services (Django app + PostgreSQL)** in the background:
  ```bash
  make run
  # Or: docker compose up -d
  ```

- **Rebuild and run services**:
  ```bash
  make run-build
  # Or: docker compose up -d --build
  ```

- **Start with extra services (pgAdmin)**:
  ```bash
  make run-extras
  # Or: docker compose --profile dev-extras up -d --build
  ```

- **Stop all services**:
  ```bash
  make stop
  # Or: docker compose --profile dev-extras down
  ```

  **Stop all services, including deleting volumes and cleaning up images**:
  ```bash
  make full-reset
  # Or: docker compose --profile dev-extras down --volumes --remove-orphans
  ```

When running with Docker, the Postgres database is accessible on port `5432` and pgAdmin (when using extras) is accessible at [http://localhost:5050/](http://localhost:5050/) (Credentials: `admin@local.dev` / `admin`).

If you want to see the database in pgAdmin, sign in and click Add New Server. Give it a name, and set the following details in the Connection tab: `Host: db`, `User: local_user`, `Password: local_password`

---

## Running Tests & Quality Control

### Unit Tests
The project uses `pytest` with `pytest-django`. Run the test suite using:

```bash
make test
# Or: poetry run pytest tests/ -v
```

### Code Style & Linting
We use `ruff` for fast python linting and formatting.

- **Check linting and style errors**:
  ```bash
  poetry run ruff check .
  ```

- **Automatically fix lint issues**:
  ```bash
  poetry run ruff check --fix .
  ```

- **Format the code**:
  ```bash
  poetry run ruff format .
  ```

---

Here is a quick summary of the available `Makefile` targets:

| Command | Description |
| :--- | :--- |
| `make setup` | Performs a clean setup of Python/npm packages and downloads HMRC / GOV.UK assets. |
| `make run` | Starts the Docker containers (web and db) in background mode. |
| `make run-build` | Forces a rebuild of Docker containers and starts them. |
| `make run-extras` | Starts the Docker containers including extra tools like pgAdmin. |
| `make test` | Runs the full `pytest` suite. |
| `make stop` | Tears down all running Docker containers including extras. |
| `make ecr-push` | Tags and pushes the local web image to AWS ECR (requires AWS CLI/credentials). |

---



## Managing the Triage Flow

The triage application flow is defined entirely in `apps/triage/flow.py`. This declarative approach allows you to update questions, routing, and results without changing HTML templates or views.

### 1. Updating Questions

Edit the `QUESTIONS` list in `apps/triage/flow.py`. Each dictionary represents a page.

```python
{
    "slug": "new-question-slug",
    "title": "What is your question?",
    "type": "radio", # or "checkbox", "select"
    "choices": [
        ("value-1", "Display Label 1"),
        ("value-2", "Display Label 2"),
    ],
},
```

### 2. Updating Routing

Update the `ROUTING` dictionary in `apps/triage/flow.py`. The key is a `(question_slug, answer_value)` tuple.

```python
ROUTING = {
    # ...
    ("current-question", "selected-answer"): "next-question-slug",
    ("current-question", "*"): "next-question-slug", # Wildcard fallback
}
```

### 3. Updating Results

1.  **Create Template**: Add a new template in `templates/triage/results/`.
2.  **Update Logic**: Modify `get_result_from_answers` in `apps/triage/flow.py` to return the new result slug based on the gathered answers.

```python
# In get_result_from_answers():
if total_value == "above-12k" and novel == "yes":
    return "my-new-result-slug"
```

### 4. Editing Macros

Common UI components are defined as Jinja2 macros in `templates/components/macros.html` - this is where you define the Gov UK (or other styling) components for use across the templates.

To modify a component (e.g., button styling) or add a new one, edit `macros.html`.

**Usage in templates:**
Import and call the macro at the top of your template:

```html
{% from "components/macros.html" import govuk_button %}

{{ govuk_button("Continue", classes="govuk-button--secondary") }}
```

