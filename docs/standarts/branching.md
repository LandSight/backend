# Branching

The project uses a branching model based on the [git-flow](https://nvie.com/posts/a-successful-git-branching-model/).

## Branch Types

This project uses several types of branches to support development, maintenance,
and release workflows.

### Primary Branches

- `main` — the stable branch that contains vetted release versions
- `develop` — the main development branch

### Supporting Branches

Supporting branches are used for implementing changes and preparing releases.

- `feature/<name>` — development of new functionality.
- `bugfix/<issue>-<name>` — fixes for non-critical bugs.
- `hotfix/<name>` — urgent fixes for critical issues in released versions.
- `release/<version>` — release preparation and stabilization.

## Branch Rules

- Direct commits to `main` and `develop` are not allowed.
  All changes must reach these branches via pull requests.

- The `main` branch must always be in a releasable state.

- The `develop` branch may contain work-in-progress functionality
  but must remain in a working state.

- `feature/*` and `bugfix/*` branches:
  - are created from `develop`
  - are merged back into `develop` via pull requests

- `hotfix/*` branches:
  - are created from `main`
  - are merged into both `main` and `develop` via separate pull requests

- `release/*` branches:
  - are created from `develop`
  - are merged into both `main` and `develop` via separate pull requests

- Supporting branches are deleted after being merged.


## Branch Naming

General rules:

- Branch names are written in lowercase.
- Words in a branch name are separated by hyphens.
- Branch names may contain Latin letters, digits, and hyphens.
- A branch name must clearly and concisely reflect the task being worked on.
- When there is a related issue, its identifier is included in the branch name after the branch type and before the short description.

Examples:
```text
feature/<short-summary>
bugfix/<issue-number>-<short-summary>
hotfix/<short-summary>
release/<version>
```
