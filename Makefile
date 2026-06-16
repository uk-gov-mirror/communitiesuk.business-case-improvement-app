run:
	docker compose up -d

run-build:
	docker compose up -d --build

run-extras:
	docker compose --profile dev-extras up -d --build
