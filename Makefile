SHELL := /bin/zsh
.DEFAULT_GOAL := help

install: ## Install all dependencies in editable mode
	pip install -e '.[dev,pub]'

check: pytest pylint bandit ## Run pytest, pylint and bandit

pytest: ## Execute unit tests with pytest
	python -m pytest .

pylint: ## Check code smells with pylint
	python -m pylint --exit-zero src

bandit: ## Check securty smells with bandit
	python -m bandit -c pyproject.toml -r src

style: black isort ## Run black and isort

black: ## Auto-format python code using black
	python -m black src

isort: ## Auto-format python code using isort
	python -m isort src

build: ## Build package into dist folder and check artifacts
	python -m build .
	python -m twine check dist/*

publish: ## Publish artifacts to pypi
	python -m twine upload dist/*

help: # Run `make help` to get help on the make commands
	@echo "\033[36mAvailable commands:\033[0m"
	@grep -E '^[0-9a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
