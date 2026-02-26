# Makefile for OpenCode Python SDK

.PHONY: help install install-dev test test-cov format lint type-check clean build

help:
	@echo "OpenCode Python SDK - Development Commands"
	@echo ""
	@echo "Available commands:"
	@echo "  make install       - Install package"
	@echo "  make install-dev   - Install package with dev dependencies"
	@echo "  make test          - Run tests"
	@echo "  make test-cov      - Run tests with coverage"
	@echo "  make format        - Format code with black and isort"
	@echo "  make lint          - Run linters"
	@echo "  make type-check    - Run type checking with mypy"
	@echo "  make clean         - Clean build artifacts"
	@echo "  make build         - Build package"

install:
	pip install -e .

install-dev:
	pip install -e ".[dev]"

test:
	pytest tests/

test-cov:
	pytest tests/ --cov=opencode_sdk --cov-report=html --cov-report=term

format:
	black opencode_sdk/ tests/ examples/
	isort opencode_sdk/ tests/ examples/

lint:
	black --check opencode_sdk/ tests/ examples/
	isort --check opencode_sdk/ tests/ examples/

type-check:
	mypy opencode_sdk/

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf htmlcov/
	rm -rf .coverage
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

build: clean
	python -m build

.DEFAULT_GOAL := help
