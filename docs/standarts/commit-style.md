# Commit Style

This project uses the [Conventional Commits](https://www.conventionalcommits.org/) specification.
All commits must follow this format.

## Format
```
<type>(<scope>)<!>: <summary>

<body>
```

Where:
- `<type>` — the type of change
- `<scope>` — an optional scope (module or subsystem) in parentheses. Using a scope is recommended but not mandatory, for complex subsystems, the scope must be specified
- `<!>` - if there are any [breaking changes](breaking-change.md)
- `<summary>` — a short description of the change

## Types
- `feat`: New functionality
- `fix`: Bug fixes
- `perf`: Performance optimizations
- `docs`: Documentation changes
- `style`: Code formatting only
- `refactor`: Code restructuring without behavior change
- `test`: Test additions or modifications
- `chore`: Build, CI, or maintenance tasks

## Rules
- **Line length**: Maximum 72 characters
- **Scope**: Indicate which part of the system is affected and must be written in lowercase
- **Summary**: Must be written in the imperative or declarative mood and not end with a period
- **Body**: Optional, explains why not how, maximum 72 characters per line
- **Issue reference**: Include `#<issue-number>` in body for tracking
- **Atomicity**: One logical change per commit. Prefer small, meaningful commits
- **Working state**: Each commit must leave the project in a working state (build and checks pass)
- **Breaking changes**:
  - Add `!` before colon in commit header
  - Prefix body with `BREAKING CHANGE:` with description of changes
