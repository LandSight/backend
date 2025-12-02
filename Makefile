UV ?= uv
PRE-COMMIT ?= pre-commit


.PHONY: install
install:          ## install deps (prod + dev)
	$(UV) sync --all-extras

.PHONY: env
env: install      ## init repo extras (e.g. hooks)
	$(PRE-COMMIT) install

UV ?= uv
PRE-COMMIT ?= pre-commit


.PHONY: install
install:          ## install deps (prod + dev)
	$(UV) sync --all-extras

.PHONY: env
env: install      ## init repo extras (e.g. hooks)
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

.PHONY: lint
lint:             ## run linters
	$(UV) run --extra=lint ty check
	$(UV) run --extra=fmt ruff check --show-fixes --preview

.PHONY: fmt
fmt:              ## run formatter
	$(UV) run --extra=fmt ruff format --preview
