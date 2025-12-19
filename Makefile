UV ?= uv
PRE-COMMIT ?= pre-commit

DOCS_DIR = docs
DOCS_BUILD_DIR = $(DOCS_DIR)/_build

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
	$(UV) run --group=docs sphinx-build -b html $(DOCS_DIR) $(DOCS_BUILD_DIR)

.PHONY: docs-serve
docs-serve:
	$(UV) run --group=dev sphinx-autobuild $(DOCS_DIR) $(DOCS_BUILD_DIR)

.PHONY: changelog-build
changelog-build:
	$(UV) run --group=docs towncrier build

.PHONY: changelog-fragment
changelog-fragment:
	$(UV) run --group=docs towncrier create
