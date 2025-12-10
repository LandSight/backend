UV ?= uv
PRE-COMMIT ?= pre-commit

DOCS_BUILD_DIR = docs/_build
DOCS_DIR = docs/

.PHONY: install
install:
	$(UV) sync

.PHONY: install-dev
install-dev: install
	$(UV) sync --all-extras

.PHONY: setup-dev
setup-dev: install-dev
	$(PRE-COMMIT) install

.PHONY: test
test:
	$(UV) run --extra=test pytest

.PHONY: check-fmt
check-fmt:
	$(UV) run --extra=fmt ruff format --preview --check

.PHONY: check-lint
check-lint:
	$(UV) run --extra=lint ty check
	$(UV) run --extra=fmt ruff check --show-fixes --preview

.PHONY: check
check: check-lint check-fmt

.PHONY: fmt
fmt:
	$(UV) run --extra=fmt ruff format --preview

.PHONY: docs-build
docs-build: docs-clean
	$(UV) run --extra=docs sphinx-build -b html $(DOCS_DIR) $(DOCS_BUILD_DIR)

.PHONY: docs-serve
docs-serve:
	$(UV) run --extra=docs sphinx-autobuild $(DOCS_DIR) $(DOCS_BUILD_DIR)

.PHONY: docs-clean
docs-clean:
	rm -rf $(DOCS_BUILD_DIR)
