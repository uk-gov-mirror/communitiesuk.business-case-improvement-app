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

*Note: the service needs to have users Logged into use, set ENTRA_ID_ENABLED to use local or ENTRA auth*
`ENTRA_ID_ENABLED=false` is the default and is for local use or if you need to allow testing with users who do not have an MHCLG account — the app then uses standard Django username/password login and needs no external services. See [Authentication](#authentication) for what changes when it's enabled.

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

### 5. Create a User Account

**Every page in the application requires a signed-in user** — there is no public area. Before you can use the app locally you need a user account. You can either use Entra, or you can create a standard Django user.

With `ENTRA_ID_ENABLED=false` (the default in `.env.example`), the app uses standard Django username/password login, so create a superuser:

```bash
poetry run python manage.py createsuperuser
```

You'll be prompted for three things, in this order:

```
Username: your.name
Email address: your.name@communities.gov.uk
Password: ********
Password (again): ********
```

> **You sign in with your email address, nut username** The user model sets `USERNAME_FIELD = "email"`, so the sign-in form's first field expects the email you entered above. 

### 6. Start the Development Server

Start the local Django server:

```bash
poetry run python manage.py runserver 8080
```

The application will be accessible at [http://localhost:8080/](http://localhost:8080/). You'll be redirected to `/accounts/login/` — sign in with the email and password from step 5.

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

When running with Docker, the Postgres database is accessible on port `5432` and pgAdmin (when using extras) is accessible at [http://localhost:5050/](http://localhost:5050/) (Credentials: `admin@local.dev` / `admin`). Use the password `local_password` to connect to the database.

### Creating a user in Docker

The Docker setup uses its own Postgres volume, separate from any local database, so you'll need an account there too:

```bash
docker compose run web python manage.py createsuperuser
```
As above, sign in with the **email address** you provide, not the username.

---

## Running Tests & Quality Control

### Unit Tests
The project uses `pytest` with `pytest-django`. Run the test suite using:

```bash
make test
# Or: poetry run pytest tests/ -v
```

The authentication tests require `ENTRA_ID_ENABLED=true` at settings load time, because the app registers a different set of URLs and middleware depending on that flag. Set it in your `.env` before running.

Without this enabled you'll get the error`AttributeError: 'Settings' object has no attribute 'ENTRA_AUTH'`.

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



## Authentication

Authentication is handled by the `apps/accounts` app. It runs in one of two modes, controlled by a single environment variable, `ENTRA_ID_ENABLED`:

| | `ENTRA_ID_ENABLED=false` (local dev) | `ENTRA_ID_ENABLED=true` (test/prod) |
|---|---|---|
| Sign-in | Django username/password form | Redirect to Microsoft Entra ID |
| User accounts | Created manually | Created automatically on first sign-in |
| Admin access | `createsuperuser`, or promote via `/admin/` | Promote via `/admin/` (see below) |

**Every route requires a signed-in user in both modes.** There is no public area — a request without a valid session is always redirected to sign in. Once signed in, everyone has the same level of access to the application itself; `/admin/` is the only area requiring additional permissions.

### Local development (`ENTRA_ID_ENABLED=false`)

This is the default and requires no external services. See [Create a User Account](#5-create-a-user-account) in Getting Started.

**Sign in with your email address** The user model uses email as its identifier (`USERNAME_FIELD = "email"`). The form field is labelled "Email address" for this reason.

**Adding more test users.** Once you have a superuser, you can create additional accounts at `/admin/` → **Accounts → Users**. Set a password via the "Password" field on the add form; that user can then sign in with their email and that password. This is useful for testing with users who do not have an ENTRA email address.

> Accounts created by an Entra sign-in have **no usable password** — they authenticate against Microsoft, not locally. If you switch a database from Entra mode to local mode, those users won't be able to sign in until an admin sets a password for them via `/admin/`.

### Entra ID (`ENTRA_ID_ENABLED=true`)

Used in the deployed environments and can be used in local testing if the below env vars are set locally. Authorisation is handled and verrified by Entra, the app verifies the token and allowed tenants. The app maps the resulting claims onto a local user record (creating one on first sign-in), and from then on a standard Django session keeps them signed in.

Requires these environment variables — ask for access to the values and make sure they are set in Secrets Manager. 

| Variable | Purpose |
|---|---|
| `ENTRA_CLIENT_ID` | Application (client) ID from the app registration |
| `ENTRA_CLIENT_SECRET` | Client secret from the app registration |
| `ENTRA_AUTHORITY` | e.g. `https://login.microsoftonline.com/organizations` |
| `ENTRA_REDIRECT_URI` | Must match the app registration's Redirect URI **exactly** - this is set to /auth_callback in the app|
| `ENTRA_LOGOUT_REDIRECT` | Where to send someone after signing out |
| `ENTRA_ALLOWED_TENANTS` | Space-separated tenant IDs permitted to sign in |
| `ENTRA_BOOTSTRAP_ADMIN_EMAIL` | Email of the first admin (see below), useful for first time deployment|


### Administrator access

Admin rights need to be manually promoted to avoid any user automatically acquiring them. Elevated access is granted in one of two ways:

**Routine:** an existing admin promotes someone at `/admin/` → **Accounts → Users** → tick **Staff status** and **Superuser status**. The person must have signed in at least once so their record exists. Changes take effect on their next request; they don't need to sign out.

**Bootstrapping a new environment:** there's no admin yet to do the promoting, and no password login in Entra mode. The `promote_superuser` management command covers this:

```bash
python manage.py promote_superuser                            # uses ENTRA_BOOTSTRAP_ADMIN_EMAIL
python manage.py promote_superuser --email someone@email.com  # or name explicitly
```

It flags that person's account as an administrator, creating the record first if they haven't signed in yet. It grants nothing on its own — they still authenticate through Entra as normal — and it's idempotent, so it's safe to re-run. Run it once per environment on first deploy, or after a database reset.

In deployed environments this runs as a one-off ECS task; see `infrastructure/maintenance-tasks/`.

### Troubleshooting
Some issues that might happen on first deploy

| Symptom | Likely cause |
|---|---|
| Redirect loop between the app and Microsoft | `ENTRA_REDIRECT_URI` doesn't match the app registration exactly |
| `AADSTS50011` | Redirect URI not registered |
| `/admin/` redirects to `/` | Signed in but not an admin — needs promoting |
| Sign-in page times out in a deployed environment | The container can't reach `login.microsoftonline.com`; check outbound  egress  |

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

