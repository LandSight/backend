# Testing

All tests are located in the `tests` directory at the repository root.

The `tests` directory is organized by test type and, where possible, mirrors the structure of the source code
in the `src` directory/

## Key principles
- **Separation by test type.**
  - `tests/unit` — unit tests that verify individual functions and classes in isolation
  - `tests/integration` — integration tests that verify interactions between multiple components
  - `tests/e2e` — end-to-end tests that verify typical end-user scenarios

- **Mirroring the code structure.**

  For modules under `src/app/<module>/...`, corresponding test modules are created under `tests/<type>/<module>/...`

- **Shared fixtures and utilities.**

  - `tests/conftest.py` — global pytest fixtures available throughout the test tree
  - `tests/factories/` — object factories
  - `tests/data/` — test data

## Naming:

- Test files must be named using the `test_*.py` pattern
- Where possible, the test module name should match the name of the module under test
  (for example, `src/app/<package>/.../module.py` → ``tests/unit/<package>/.../test_module.py``).


## Test Policy

- All new functionality must be covered by at least unit tests
- When fixing bugs, tests that reproduce the fixed issue must be added or updated
- Tests must be deterministic: results must not depend on execution order, external environment, or time
- Running tests is mandatory before creating a pull request


## Failing and Expected-to-Fail Tests

- The use of `xfail` is allowed only for well-understood, documented issues.
