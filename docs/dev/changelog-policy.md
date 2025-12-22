# Changelog Policy

## Purpose

This project maintains a structured, curated changelog intended for **end users, integrators, and operators**.

The goal of the changelog is to:

- Clearly communicate **meaningful, user-visible changes**
- Highlight **breaking changes, security fixes, and behavioral changes**
- Avoid noise from internal refactoring and maintenance work

---

## Scope

The changelog includes changes that affect:

- Runtime behavior
- Public APIs
- Configuration, deployment, or operations
- Required user actions or migrations

---

## Tooling

The project uses **Towncrier** to generate the changelog.

Each pull request that introduces a user-visible change **must include**

---

## Change Types

The following change types are supported.

| Type        | Description                               | Example                                                      |
|-------------|-------------------------------------------|--------------------------------------------------------------|
| **Feature** | New user-facing functionality             | Added a new endpoint for bulk user import                    |
| **Bugfix**  | Fix for incorrect existing behavior       | Fixed crash when submitting an empty form                    |
| **Security**| Security-related fixes or mitigations     | Fixed privilege escalation in admin API                      |
| **Deprecation** | Functionality marked for future removal | Deprecated legacy authentication method                     |
| **Removal** | Removed previously deprecated feature    | Removed legacy authentication method                         |
| **Docs**    |  User-facing documentation changes         | Updated configuration reference for caching                  |
| **Ops**     | Operational or deployment changes         | Changed default worker concurrency settings                  |

---

## Excluded Changes

The following changes **must not** be included in the changelog:

- Refactoring without behavior changes
- Formatting or lint-only changes
- Test-only changes
- CI/CD configuration changes
- Internal tooling changes
- Dependency updates without user-visible impact

---

## Writing Guidelines

Changelog entries should:

- Be written in **user-oriented language**
- Focus on **what changed**, not **how**
- Avoid internal code references
- Be concise but complete

### Good Example

> Fixed incorrect validation of user input during order creation.

### Bad Example

> Refactored `OrderValidator` to handle edge cases.

---


## Responsibility

- Contributors add changelog fragments
- Reviewers verify correctness
- Maintainers finalize entries during release

---

## Enforcement

Pull requests introducing user-visible changes **must not be merged**
without an appropriate changelog fragment.

Exceptions require explicit maintainer approval.

---

## Summary

The changelog is a communication tool, not a development log.

> **If a user might notice or care about the change — it belongs in the changelog.**
