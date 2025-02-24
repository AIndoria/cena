define BROWSER_PYSCRIPT
import os, webbrowser, sys

from urllib.request import pathname2url

webbrowser.open("file://" + pathname2url(os.path.abspath(sys.argv[1])))
endef
export BROWSER_PYSCRIPT

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT

BROWSER := python -c "$$BROWSER_PYSCRIPT"

help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

purge: clean ## ⚠️  Removes All Developer Data for a fresh server start
	rm -r ./dev/data/recipes/
	rm -r ./dev/data/users/
	rm -f ./dev/data/cena_v*.db
	rm -f ./dev/data/cena.log
	rm -f ./dev/data/.secret

clean: clean-pyc clean-test ## 🧹 Remove all build, test, coverage and Python artifacts

clean-pyc: ## 🧹 Remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test: ## 🧹 Remove test and coverage artifacts
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/
	rm -fr .pytest_cache

test-all: lint test ## 🧪 Check Lint Format and Testing

test: ## 🧪 Run tests quickly with the default Python
	poetry run pytest

lint: ## 🧺 Check style with flake8
	poetry run black .
	poetry run black . --check
	poetry run flake8 cena tests

coverage: ## ☂️  Check code coverage quickly with the default Python
	poetry run pytest
	poetry run coverage report -m
	poetry run coverage html
	$(BROWSER) htmlcov/index.html

setup: ## 🏗  Setup Development Instance
	poetry install && \
	cd frontend && \
	npm install && \
	cd ..

backend: ## 🎬 Start Cena Backend Development Server
	poetry run python cena/db/init_db.py && \
	poetry run python cena/services/image/minify.py && \
	poetry run python cena/app.py


.PHONY: frontend
frontend: ## 🎬 Start Cena Frontend Development Server
	cd frontend && npm run serve

frontend-build: ## 🏗  Build Frontend in frontend/dist
	cd frontend && npm run build

.PHONY: docs
docs: ## 📄 Start Mkdocs Development Server
	poetry run python dev/scripts/api_docs_gen.py && \
	cd docs && poetry run python -m mkdocs serve

docker-dev: ## 🐳 Build and Start Docker Development Stack
	docker-compose -f docker-compose.dev.yml -p dev-cena down && \
	docker-compose -f docker-compose.dev.yml -p dev-cena up --build

docker-prod: ## 🐳 Build and Start Docker Production Stack
	docker-compose -f docker-compose.yml -p cena up --build

code-gen: ## 🤖 Run Code-Gen Scripts
	poetry run python dev/scripts/app_routes_gen.py

