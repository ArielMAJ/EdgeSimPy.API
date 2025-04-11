CONTAINER_ENGINE := $(shell which podman || which docker)
COMPOSE := $(CONTAINER_ENGINE) compose

ifneq ("$(wildcard .env)","")
	include .env
	export
endif

.PHONY: run
run: ## Run the project.
	poetry run python -m src.main

.PHONY: install
install: ## Install Python package dependencies.
	python -m pip install --upgrade pip setuptools wheel poetry
	poetry lock
	poetry install --no-root
	poetry run pre-commit install

.PHONY: test
test: ## Run automated tests.
	ENVIRONMENT=test poetry run pytest --cov

.PHONY: up-database
up-database: ## Start database container.
	$(COMPOSE) up -d postgres --force-recreate

.PHONY: down
down: ## Stop all containers.
	$(COMPOSE) down

.PHONY: revision
revision: ## Create a new database revision following the repository's models.
	poetry run alembic revision --autogenerate -m "$(MESSAGE)"

.PHONY: migrate
migrate: ## Run database migrations.
	poetry run alembic upgrade head

.PHONY: downgrade
downgrade: ## Undo last database migration.
	poetry run alembic downgrade -1

.PHONY: docker-rm
docker-rm: ## Remove all docker/podman containers.
	$(CONTAINER_ENGINE) rm -f $$($(CONTAINER_ENGINE) ps -a -q)

.PHONY: docker-rmi
docker-rmi: ## Remove all downloaded docker/podman images.
	$(CONTAINER_ENGINE) rmi -f $$($(CONTAINER_ENGINE) images -q)

.PHONY: export-requirements
export-requirements: ## Export poetry managed packages to a requirements.txt (needed by Vercel).
	poetry export -f requirements.txt --output requirements.txt --without-hashes

.PHONY: pre-commit
pre-commit: ## Run pre-commit checks.
	poetry run pre-commit run --config ./.pre-commit-config.yaml

.PHONY: patch
patch: ## Bump project version to next patch (bugfix release).
	poetry version patch

.PHONY: minor
minor: ## Bump project version to next minor (feature release).
	poetry version minor

.PHONY: clean
clean: ## Clean project's temporary files.
	find . -name '__pycache__' -exec rm -rf {} +
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.log' -exec rm -f {} +

.DEFAULT_GOAL := help
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sed 's/Makefile://g' | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
