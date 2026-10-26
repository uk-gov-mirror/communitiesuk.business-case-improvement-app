-include .env

setup:
	poetry install && \
	echo "Setting up static assets..." && \
	echo "WARNING: THIS IS A DESTRUCTIVE ACTION. It will delete any changes you have made in ./static." && \
	echo "Press enter to continue or ctrl+c to cancel." && \
	read x && \
	rm -rf node_modules && \
	rm -rf static/hmrc-frontend static/govuk static/govuk-frontend static/images && \
	mkdir -p static/hmrc-frontend && \
	npm i && \
	mv ./node_modules/hmrc-frontend/hmrc/govuk ./static/hmrc-frontend/govuk && \
	mv ./node_modules/hmrc-frontend/hmrc/hmrc-frontend-*.min.css ./static/hmrc-frontend/hmrc-frontend.min.css && \
	poetry run python scripts/setup_govuk_frontend.py

run:
	docker compose up -d

run-build:
	docker compose up -d --build

run-build-nocache:
	docker compose build --no-cache
	docker compose up -d --build

run-extras:
	docker compose --profile dev-extras up -d --build

redeploy-local-lambda:
	docker compose exec ministack sh /docker-entrypoint-initaws.d/ready.d/02-deploy-process-business-case-response-lambda.sh

test:
	poetry run pytest tests/ -v

stop:
	docker compose --profile dev-extras down

full-reset:
	docker compose --profile dev-extras down --volumes --remove-orphans

