===========================
Contributing to the Project
===========================

Thank you for your interest in contributing to this project.
We welcome community participation and appreciate improvements of any size — from small fixes to new features
and documentation enhancements.


Development Environment Setup
=============================

Before you start, make sure the following tools are installed on your system:

- ``uv >= 0.9.0`` — for dependency and virtual environment management.
- ``make >= 4.0.0`` — for running commands defined in the ``Makefile``.

Setup steps:

1. Clone the repository:

   .. code-block:: bash

      git clone https://github.com/LandSight/backend.git
      cd backend

2. Create a virtual environment and install dependencies:

   .. code-block:: bash

      make install


.. _code-quality:

Code Quality Standards and Conventions
======================================

This project follows strict rules for code style and structure.

Code quality is enforced by the ``ruff`` and ``ty`` linters, configured in ``pyproject.toml``.


Auxiliary Commands
------------------

.. code-block:: bash

   make check-lint  # Run static analysis.
   make check-fmt   # Check code style and formatting.
   make checks      # Run all checks.
   make fmt         # Format the code.


Code Style
----------

- **PEP 8** — baseline recommendations for Python code style.
- **NumPy-style docstring** — a unified format for documenting parameters, return values, and exceptions.
- Naming follows ``pep8-naming``:

  - classes — ``CamelCase``.
  - functions and variables — ``snake_case``.
  - constants — ``UPPER_CASE``.
  - private classes, functions, and variables must start with ``_``.

- Maximum line length is **120** characters.
- Double quotes are used for strings.


Typing
------

All functions must have type annotations for all parameters and the return value.


Docstrings and Formatting
-------------------------

A single docstring format is used across the project — `NumPy-style docstring <https://numpydoc.readthedocs.io/en/latest/format.html>`_.

Main requirements:

- The ``Parameters`` section is used to describe parameters, including parameter name, type, and a short description.
- The ``Returns`` section is used to describe return values.
- The ``Raises`` section is used to describe possible exceptions.
- Additional sections may be added when needed (for example, ``Examples``, ``Notes``, ``Warnings``, ``See Also``, etc.).


.. _testing:

Testing
=======

The project uses ``pytest`` for automated tests.


Running Tests
-------------

To run the test suite, use:

.. code-block:: bash

   make test


Test Layout
-----------

All tests are located in the ``tests`` directory at the repository root.

The ``tests`` directory is organized by test type and, where possible, mirrors the structure of the source code
in the ``src`` directory:

Key principles:

- **Mirroring the code structure.**

  For modules under ``src/app/...``, corresponding test modules are created under ``tests/unit/app/...``.

- **Separation by test type.**

  - ``tests/unit`` — unit tests that verify individual functions and classes in isolation.
  - ``tests/integration`` — integration tests that verify interactions between multiple components.
  - ``tests/e2e`` — end-to-end tests that verify typical end-user scenarios.

- **Shared fixtures and utilities.**

  - ``tests/conftest.py`` — global pytest fixtures available throughout the test tree.
  - ``tests/factories/`` — object factories.
  - ``tests/data/`` — test data.

Naming:

- Test files must be named using the ``test_*.py`` pattern.
- Where possible, the test module name should match the name of the module under test
  (for example, ``src/app/package/module.py`` → ``tests/unit/app/package/test_module.py``).


Test Policy
-----------

- All new functionality must be covered by at least unit tests.
- When fixing bugs, tests that reproduce the fixed issue must be added or updated.
- Tests must be deterministic: results must not depend on execution order, external environment, or time.
- Running tests is mandatory before creating a pull request.


Failing and Expected-to-Fail Tests
----------------------------------

- The use of ``xfail`` is allowed only for well-understood, documented issues.


Commit Message Conventions
==========================

This project uses the `Conventional Commits <https://www.conventionalcommits.org/>`_ specification.
All commits must follow this format.


General Format
--------------

A commit message must have the following structure:

.. code-block:: text

   <type>[optional scope]: <short summary>

If a change is breaking, this must be explicitly indicated by adding ``!`` after the type or scope:

.. code-block:: text

   <type>[optional scope]!: <short summary>

Where:

- ``<type>`` — the type of change.
- ``[optional scope]`` — an optional scope (module or subsystem) in parentheses.
- ``<short summary>`` — a short description of the change.


Supported Types
^^^^^^^^^^^^^^^

The following commit types are used in the project:

- ``feat`` — adding new functionality.
- ``fix`` — fixing a bug.
- ``docs`` — documentation changes (RST/Markdown, comments, docstrings) that do not affect behavior.
- ``style`` — changes that do not affect behavior (formatting, whitespace, import order, etc.) when they are not handled by auto-formatting.
- ``refactor`` — code refactoring without changing external behavior.
- ``test`` — adding or modifying tests.
- ``chore`` — maintenance changes that do not affect application code (e.g. updating linters configs, editor settings, .gitignore, etc.).
- ``build`` — changes that affect the build system or external dependencies (build scripts, package manifests, lockfiles, tooling for packaging, etc.).
- ``release`` — release preparation: version bumps, changelog updates, and blocking fixes in the release branch.
- ``ci`` — changes to CI/CD configuration (workflows, pipelines, jobs, triggers).
- ``revert`` — reverting a previous commit.


Scope
^^^^^

The scope is specified in parentheses immediately after the type and helps indicate which part of the system is affected.

Scope requirements:

- The scope is written in lowercase.
- The scope must be short and reflect the module or subsystem.
- Using a scope is recommended but not mandatory, for complex subsystems, the scope must be specified.


Body and Footer
^^^^^^^^^^^^^^^

If needed, a commit message may include a body and footers after the short summary.

Recommended:

- Use the body to describe the motivation for the change and important implementation details.
- When there are related issues or discussions in the issue tracker, add links in the footer,
  for example: ``Refs: #123``, ``Closes #456``.


Commit Requirements
-------------------

Commit messages must:

- Contain a short description in the imperative or declarative mood.
- Not end with a period.
- Describe a single logical change.

Commit working state:

- Changes should be split into a sequence of small, meaningful commits.
- Each commit must leave the project in a working state: the project builds, and tests and checks pass.

The following commits are not allowed:

- Commits that contain several logically independent changes, different changes (refactoring, new functionality, test updates) must be split into separate commits.
- Commits with uninformative messages such as ``fix``, ``update``, ``wip``, and similar.


.. _branching-process:

Branching Process
=================

The project uses a branching model based on `git-flow <https://nvie.com/posts/a-successful-git-branching-model/>`_.


Primary Branches
----------------

The repository has two long-lived branches:

- ``main`` — the stable branch that contains vetted release versions.
- ``develop`` — the main development branch.

Rules:

- Direct commits to ``main`` and ``develop`` are not allowed, changes reach these branches only via pull requests.
- The ``main`` branch must always be in a releasable state.
- The ``develop`` branch may contain work-in-progress functionality but must remain in a working state.


Branch Naming
-------------

General rules:

- Branch names are written in lowercase.
- Words in a branch name are separated by hyphens.
- Branch names may contain Latin letters, digits, and hyphens.
- A branch name must clearly and concisely reflect the task being worked on.
- When there is a related issue, its identifier is included in the branch name after the branch type and before the short description.

Examples:

.. code-block:: text

   feature/<short-summary>
   bugfix/<issue-number>-<short-summary>
   hotfix/<short-summary>
   release/<version>


Temporary Branches
------------------

Temporary branches are used for feature development, bug fixes, and release preparation:

- ``feature/<name>`` — new feature development.
- ``bugfix/<name>`` — fixing issues that do not require an immediate release.
- ``hotfix/<name>`` — urgent fixes for critical problems in a released version.
- ``release/<version>`` — release preparation.

Rules:

- ``feature/<name>`` and ``bugfix/<name>`` branches are created from ``develop`` and merged back into ``develop`` via pull requests.
- ``hotfix/<name>`` branches are created from ``main`` and merged into both ``main`` and ``develop`` via separate pull requests.
- ``release/<version>`` branches are created from ``develop`` and merged into both ``main`` and ``develop`` via separate pull requests.
- Temporary branches are deleted after they are merged.


Creating and Maintaining Pull Requests
======================================

General Principles
------------------

- Pull requests must follow the branching process described in the \"Branching Process\" section.
- One pull request should correspond to one logical task.
- Smaller, focused pull requests are preferred.


Pre-requisites for Opening a Pull Request
----------------------------------------

Before opening a pull request, you must:

- Bring the changes into compliance with the \"Code Quality Standards and Conventions\" section.
- Run the tests as described in the \"Testing\" section and ensure they pass successfully.


Pull Request Formatting Requirements
------------------------------------

The pull request title must:

- Concisely describe the essence of the changes.

The pull request description must:

- List the key changes.
- Explain the motivation for the changes.
- Include instructions for testing the changes, if necessary.
- Explicitly mention any breaking changes, if present.
- Include links to related issues and discussions.


Working with Pull Requests
--------------------------

When working with a pull request, you must:

- Respond to review comments within the pull request discussion.
- Make changes and push them to the same branch from which the pull request was opened.
- After making changes, ensure that all checks pass again.
- After editing based on the review, request a re-review from the reviewer or clearly indicate in the PR that the changes have been made and it is ready for re-review.

Conditions for Merging a Pull Request
-------------------------------------

A pull request may be merged when all of the following are true:

- All automated checks complete successfully.
- There are no unresolved comments or open questions about the changes.
- The pull request has been approved by a reviewer according to the repository settings.


Discussing Ideas and Reporting Issues
=====================================

General Rules
-------------

- The repository issue tracker is used for feature ideas and bug reports.
- Before creating a new issue, make sure a similar one does not already exist.
- Each issue must describe exactly one idea or one problem.


Feature Ideas and Proposals
---------------------------

Issue requirements:

- A short and unambiguous title.
- A description of the problem the proposed functionality should solve.
- The motivation for the change.
- The expected behavior of the system after the feature is implemented.
- Constraints and assumptions, if any.


Bug Reports
-----------

Issue requirements:

- A short and unambiguous title.
- A clear description of the problem.
- Expected behavior.
- Actual behavior.
- Steps to reproduce the issue.
- Environment details (Python version, OS, configuration in use).
- Relevant log excerpts or stack traces, if available.


Working with Issues
-------------------

- Before starting work on a task, make sure the issue is still relevant.
- If you plan to work on an issue, explicitly state this in a comment.
- Pull requests are linked to issues via references in the pull request description.
- Issues are closed after the corresponding pull request is merged or at the maintainers discretion.
