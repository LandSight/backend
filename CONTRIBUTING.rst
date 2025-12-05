Contributing to the LandSight backend
=====================================

Welcome! This document explains how to set up your environment and which conventions to follow before submitting changes.

Quick start
-----------

1. Clone the repository and ``cd backend``.
2. Set up dev dependencies and hooks::

       make setup-dev

3. Make sure `uv <https://docs.astral.sh/uv/>`_ is installed.

Workflow
--------

- Branches: start from ``main`` and choose a descriptive prefix:

  - ``feature/<summary>`` — new functionality or API surface.
  - ``bugfix/<summary>`` — fixes for existing defects.
  - ``refactor/<summary>`` — architectural changes without behavioral changes.
  - ``chore/<summary>`` — infrastructure, configs, dependency/tooling updates.
  - ``docs/<summary>`` — documentation, guides, diagrams, examples.
  - ``test/<summary>`` — work on tests and fixtures.
  - ``ci/<summary>`` — CI/CD pipelines and automation.
  - ``hotfix/<summary>`` — urgent fixes destined for the stable branch.
  - ``release/<version>`` — preparing a release (changelog, version bump).

- Commits: follow `Conventional Commits <https://www.conventionalcommits.org/en/v1.0.0/>`_. Main types:

  - ``feat:`` — add new functionality or API.
  - ``fix:`` — fix bugs or regressions.
  - ``refactor:`` — restructure code without changing external behavior.
  - ``chore:`` — infrastructure, configuration, dependency/tooling maintenance.
  - ``docs:`` — documentation and examples.
  - ``test:`` — tests and fixtures.
  - ``ci:`` — CI/CD pipelines.
  - ``build:`` — build system, packaging, Docker.
  - ``perf:`` — performance optimizations.
  - ``hotfix:`` — urgent production fixes.
  - ``revert:`` — revert previous commits.
  - Use scopes (``type(scope): …``) to narrow the affected area.
  - Add ``!`` before the colon (``type(scope)!: …``) to mark breaking changes.

- Branch flow:

  - ``main`` — stable branch; only release-ready code lands here.
  - ``develop`` — integration branch. Merge all working branches via PRs here and run checks/QA.
  - ``feature/*``, ``bugfix/*``, ``refactor/*``, ``chore/*``, ``docs/*``, ``test/*``, ``ci/*`` — working branches. Create them from the latest ``main`` and rebase frequently onto ``develop``/``main``.
  - ``hotfix/*`` — emergency fixes. Merge into ``main`` (with prior agreement) and then back into ``develop``.
  - When ``develop`` is ready for release, merge into ``main`` and bump the version.

Quality checks
--------------

- **Lint/typing/format** — ``make check`` (runs ``ty`` and ``ruff``).
- **Tests** — ``make test`` (``uv run --extra=test pytest``). Ensure the suite is green before opening a PR.
- **Logging** — initialize logging via ``app.logging.configure_logging()`` and ``get_logger()`` in your entry points.
- **Documentation** — write docstrings in reStructuredText (PEP 257). Ruff enforces ``lint.pydocstyle.convention = "pep257"``.

Versioning
----------

- We follow SemVer: ``MAJOR.MINOR.PATCH``.

  - ``MAJOR`` — breaking API/contract changes.
  - ``MINOR`` — new functionality without breaking compatibility.
  - ``PATCH`` — backward-compatible bug fixes.

- The version lives in ``src/app/__meta__.py`` and is exposed via ``app.__version__``.

Before opening a pull request
-----------------------------

1. Rebase or merge the latest ``main`` into your branch.
2. Run::

       pre-commit run --all-files
       make check
       make test

3. Keep commits small and well described.
4. Craft your pull request carefully:

   - Title: ``<type>: <short summary>`` — e.g. ``feat: add logging helpers``.
   - Description should include:

     1. **What** changed (key bullet points).
     2. **Why** it is needed (motivation, link to issue/task).
     3. **How to verify** (manual steps or commands).
     4. **Checklist** — confirm lint/tests/docs/migrations are handled.

   - Attach screenshots/logs if API behavior or UI visibly changes.
   - Mention dependencies on other PRs/branches, if any.

Issues and questions
--------------------

- Check for duplicates and discuss the idea in chat if you are unsure before creating a new issue.
- Title: briefly describe the problem/feature (``bug:``, ``feature:``, ``doc:``, etc.).
- Minimum issue template:

  1. **Context** — required outcome or failing scenario.
  2. **Steps / Expected / Actual** — reproduction steps and expected vs actual result (for bugs).
  3. **Additional info** — logs, screenshots, specs.
  4. **Priority / Impact** — severity and blocking impact.
- For features — attach designs, API sketches, or business requirements.
- For bugs — propose a fix idea or note if a hotfix is needed.
- Use the team chat for quick questions so the tracker stays focused.
