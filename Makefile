UV ?= uv
PRE-COMMIT ?= pre-commit


.PHONY: install
install:
	$(UV) sync

.PHONY: install-dev
install-dev: install
	$(UV) sync --all-extras

.PHONY: setup-dev
setup-dev: install-dev
	$(PRE-COMMIT) install

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
