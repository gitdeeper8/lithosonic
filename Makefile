# LITHO-SONIC Makefile
# Version: 1.0.0 | DOI: 10.5281/zenodo.18931304

.PHONY: help install dev test lint clean docker run docs

help:
	@echo "LITHO-SONIC Makefile"
	@echo ""
	@echo "Usage:"
	@echo "  make install     Install dependencies"
	@echo "  make dev         Install development dependencies"
	@echo "  make test        Run tests"
	@echo "  make lint        Run linters"
	@echo "  make clean       Clean build artifacts"
	@echo "  make docker      Build Docker image"
	@echo "  make run         Run locally"
	@echo "  make docs        Build documentation"

install:
	pip install --upgrade pip
	pip install -r requirements.txt
	pip install -e .

dev:
	pip install --upgrade pip
	pip install -r requirements-dev.txt
	pip install -e .

test:
	pytest tests/ -v --cov=lithosonic

test-coverage:
	pytest tests/ -v --cov=lithosonic --cov-report=html --cov-report=term

lint:
	flake8 lithosonic/ tests/
	black --check lithosonic/ tests/
	isort --check-only lithosonic/ tests/
	mypy lithosonic/

format:
	black lithosonic/ tests/
	isort lithosonic/ tests/

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf .mypy_cache/
	rm -rf __pycache__/
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete

docker:
	docker build -t lithosonic:latest .
	docker build -t lithosonic:dev -f Dockerfile.dev .

run:
	python -m lithosonic.cli serve --host 0.0.0.0 --port 5000

collect:
	python -m lithosonic.cli collect --interval 60

process:
	python -m lithosonic.cli process --interval 300

lsi:
	python -m lithosonic.cli lsi

docs:
	cd docs && make html
	@echo "Documentation built in docs/_build/html/"

serve-docs:
	cd docs/_build/html && python -m http.server 8000

init-db:
	python scripts/init_db.py

test-sensors:
	python scripts/test_sensors.py --all

check:
	python scripts/diagnose.py --all

backup:
	./scripts/backup.sh

restore:
	./scripts/restore.sh

release: clean lint test
	python -m build
	twine check dist/*

docker-run:
	docker run -p 5000:5000 -v $(PWD)/data:/data lithosonic:latest

docker-compose-up:
	docker-compose up -d

docker-compose-down:
	docker-compose down

docker-compose-logs:
	docker-compose logs -f

.PHONY: help install dev test test-coverage lint format clean docker run collect process lsi docs serve-docs init-db test-sensors check backup restore release docker-run docker-compose-up docker-compose-down docker-compose-logs
