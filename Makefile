-include .env

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

stop:
	docker compose --profile dev-extras down

ecr-push-dev:
	aws ecr get-login-password --region eu-west-2 --profile bpi-dev | \
		docker login --username AWS --password-stdin $(DEV_ACCOUNT_ID).dkr.ecr.eu-west-2.amazonaws.com
	docker tag business-case-improvement-app-web:latest $(DEV_ACCOUNT_ID).dkr.ecr.eu-west-2.amazonaws.com/dpi-bci-dev-webapp:latest
	docker push $(DEV_ACCOUNT_ID).dkr.ecr.eu-west-2.amazonaws.com/dpi-bci-dev-webapp:latest

ecr-push-test:
	aws ecr get-login-password --region eu-west-2 --profile bpi-test | \
		docker login --username AWS --password-stdin $(TEST_ACCOUNT_ID).dkr.ecr.eu-west-2.amazonaws.com
	docker tag business-case-improvement-app-web:latest $(TEST_ACCOUNT_ID).dkr.ecr.eu-west-2.amazonaws.com/dpi-bci-test-webapp:latest
	docker push $(TEST_ACCOUNT_ID).dkr.ecr.eu-west-2.amazonaws.com/dpi-bci-test-webapp:latest
