# Contributing to the LandSight

Thank you for your interest in contributing to the LandSight.
We welcome community participation and appreciate improvements of any size — from small fixes to new features
and documentation enhancements.

## Development Environment Setup

Before you start, make sure the following tools are installed on your system:

- `uv >= 0.9.0` — for dependency and virtual environment management.
- `just >= 1.45.0` — for running commands defined in the `justfile`.

Setup steps:

1. Clone the repository:
```bash
git clone https://github.com/LandSight/backend.git
cd backend
```

2. Create a virtual environment and install dependencies:
```bash
just install
```

## Code Style

This project follows strict rules for code style and structure.

More information on [code style](dev/code-style.md) page.

To run static analysis and auto formatter, use commands:
```bash
just lint        # Run static analysis.
just fmt         # Format the code.
```

## Testing

The project uses `pytest` for automated tests.

All tests are located in the `tests` directory at the repository root.

The `tests` directory is organized by test type and, where possible, mirrors the structure of the source code
in the `src` directory.

More information on the [testing](dev/testing.md) page.

To run the test suites, use command:
```bash
just test
```

## Commit Style

This project uses the [Conventional Commits](https://www.conventionalcommits.org/) specification.
All commits must follow this format.

More information on the [commit style](dev/commit-style.md) page.

## Branching

The project uses a branching model based on the [git-flow](https://nvie.com/posts/a-successful-git-branching-model/).

The repository has two long-lived branches:

- `main` — the stable branch that contains vetted release versions
- `develop` — the main development branch

Rules:

- Direct commits to `main` and `develop` are not allowed, changes reach these branches only via pull requests
- The `main` branch must always be in a releasable state
- The `develop` branch may contain work-in-progress functionality but must remain in a working state

More information on the [branching](dev/branching.md) page.

## Pull Requests

### General Principles

- Pull requests must follow the branching process described in the \"Branching\" section.
- One pull request should correspond to one logical task.
- Smaller, focused pull requests are preferred.

### Pre-requisites for Opening a Pull Request

Before opening a pull request, you must:

- Bring the changes into compliance with the \"Code Style\" section.
- Run the tests as described in the \"Testing\" section and ensure they pass successfully.

More information about creating and maintaining pull requests on [pull request](dev/pull-request.md) page.

## Issues

- The repository issue tracker is used for feature ideas and bug reports.
- Before creating a new issue, make sure a similar one does not already exist.
- Each issue must describe exactly one idea or one problem.

More information about discussing ideas and reporting issues on the [issues](dev/issues.md) page.

## Changelog

This project maintains a curated, user-facing changelog.

All pull requests that introduce **user-visible changes** are required to
include a changelog entry. The purpose of the changelog is to clearly
communicate meaningful changes to users and downstream consumers.

The detailed information - including supported change types, writing
guidelines, and examples - is documented on the [changelog policy](dev/changelog-policy.md) page.

### Tooling

This project uses **Towncrier** to manage changelog entries.

Instead of editing the changelog file directly, contributors add small
fragment files that are later assembled during the release process.

Common commands:
```bash
just changelog-fragment   # Create a changelog fragment.
just changelog-build      # Build the changelog.
```

These commands ensure consistent formatting and structure of the changelog.

### Responsibility

- **Contributors** are responsible for adding changelog fragments for
  user-visible changes.
- **Reviewers** verify that changelog entries are accurate, complete,
  and correctly categorized.
- **Maintainers** finalize and curate changelog entries during the
  release process.
