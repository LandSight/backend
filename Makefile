UV ?= uv
PRE-COMMIT ?= pre-commit

BUILD_DIR = build
DOCS_BUILD_DIR = $(BUILD_DIR)/docs

DOCS_HOST ?= 127.0.0.1
DOCS_PORT ?= 8008

.PHONY: install
install:
	$(UV) venv
	$(UV) sync --all-groups
	$(PRE-COMMIT) install

.PHONY: test
test:
	$(UV) run --group=test pytest --cov=src/app --cov-report=term-missing --cov-append

.PHONY: lint
lint:
	$(UV) run --group=dev ty check
	$(UV) run --group=dev ruff format --preview --check
	$(UV) run --group=dev ruff check --show-fixes --preview

.PHONY: fmt
fmt:
	$(UV) run --group=lint ruff format --preview

.PHONY: docs-clean
docs-clean:
	rm -rf $(DOCS_BUILD_DIR)

.PHONY: docs-build
docs-build: docs-clean
	$(UV) run --group=docs mkdocs build

.PHONY: docs-serve
docs-serve:
	$(UV) run --group=docs mkdocs serve --dev-addr $(DOCS_HOST):$(DOCS_PORT) --no-livereload

.PHONY: changelog-build
changelog-build:
	$(UV) run --group=docs towncrier build

.PHONY: changelog-fragment
changelog-fragment:
	$(UV) run --group=docs towncrier create
