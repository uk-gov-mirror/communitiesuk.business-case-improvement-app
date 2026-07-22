FROM python:3.14.6-alpine3.24
RUN apk add --update --no-cache curl=8.21.0-r0

WORKDIR /usr/src/app

#  Install Poetry
ARG POETRY_VERSION=2.1.3
ARG DEBUG=false
ENV DEBUG=$DEBUG
RUN pip install "poetry==${POETRY_VERSION}" --no-cache-dir

# Copy Poetry files
COPY pyproject.toml poetry.lock* ./

# Install dependencies — no dev deps in production, no venv needed in container
RUN poetry config virtualenvs.create false \
    && poetry install --only main --no-interaction --no-ansi

# Copy application code
COPY . .

# Download GOV.UK Frontend assets and fix symlinks
RUN chmod +x scripts/setup_govuk_frontend.py
RUN python scripts/setup_govuk_frontend.py

# Collect static files
RUN python manage.py collectstatic --noinput \
    --settings=config.settings

# Create Non-root user - allow to access Temp DB (TODO: we won't need temp DB in future)
RUN mkdir -p /usr/src/app/data && addgroup --system appuser && adduser --system --ingroup appuser appuser && chown -R appuser:appuser /usr/src/app

USER appuser

EXPOSE 8080

RUN chmod +x entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]

CMD ["gunicorn", "config.wsgi:application", \
    "--bind", "0.0.0.0:8080", \
    "--workers", "2", \
    "--timeout", "60", \
    "--access-logfile", "-", \
    "--error-logfile", "-"]
