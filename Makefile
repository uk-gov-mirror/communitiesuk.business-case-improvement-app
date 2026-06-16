setup:
	echo "Setting up static assets..." && \
	echo "WARNING: THIS IS A DESTRUCTIVE ACTION. It will delete any changes you have made in ./static." && \
	echo "Press enter to continue or ctrl+c to cancel." && \
	read x && \
	rm -rf node_modules && \
	rm -rf static/hmrc-frontend static/govuk static/govuk-frontend static/images && \
	mkdir -p static/hmrc-frontend && \
	npm i && \
	mv ./node_modules/hmrc-frontend/hmrc/govuk ./static/govuk && \
	mv ./node_modules/hmrc-frontend/hmrc/hmrc-frontend-*.min.css ./static/hmrc-frontend/hmrc-frontend.min.css && \
	poetry run python scripts/setup_govuk_frontend.py

run:
	docker compose up -d

run-build:
	docker compose up -d --build

run-extras:
	docker compose --profile dev-extras up -d --build

test:
	poetry run pytest tests/ -v
