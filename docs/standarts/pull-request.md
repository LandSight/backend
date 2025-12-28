# Creating and Maintaining Pull Requests

## General Principles

- Pull requests must follow the branching process described in the [branching](branching.md) rules.
- One pull request should correspond to one logical task.
- Smaller, focused pull requests are preferred.

## Pre-requisites for Opening a Pull Request

Before opening a pull request, you must:

- Bring the changes into compliance with the [code style](code-style.md) requirements.
- Run the tests and ensure they pass successfully.

## Pull Request Formatting Requirements

The pull request title must:

- Concisely describe the essence of the changes.

The pull request description must:

- List the key changes.
- Explain the motivation for the changes.
- Include instructions for testing the changes, if necessary.
- Explicitly mention any breaking changes, if present.
- Include links to related issues and discussions.

## Working with Pull Requests

When working with a pull request, you must:

- Respond to review comments within the pull request discussion.
- Make changes and push them to the same branch from which the pull request was opened.
- After making changes, ensure that all checks pass again.
- After editing based on the review, request a re-review from the reviewer or clearly indicate in the PR that the changes have been made and it is ready for re-review.

## Conditions for Merging a Pull Request

A pull request may be merged when all of the following are true:

- All automated checks complete successfully.
- There are no unresolved comments or open questions about the changes.
- The pull request has been approved by a reviewer according to the repository settings.
