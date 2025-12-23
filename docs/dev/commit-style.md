# Commit Style

## Format
```
<type>(<scope>)<!>: <summary>

<body>
```

## Types
- `feat`: New functionality
- `fix`: Bug fixes
- `perf`: Performance optimizations
- `docs`: Documentation changes
- `style`: Code formatting only
- `refactor`: Code restructuring without behavior change
- `test`: Test additions or modifications
- `chore`: Build, CI, or maintenance tasks

## Scopes
- `api`: API endpoints and contracts
- `core`: Core business logic
- `gis`: GIS processing and analysis
- `db`: Database schema and queries
- `auth`: Authentication and authorization
- `config`: Configuration management
- `logging`: Logging and monitoring

## Rules
- **Summary line**: Maximum 72 characters, imperative mood ("Add" not "Added")
- **Body**: Optional, explains why not how, maximum 72 characters per line
- **Issue reference**: Include `#<issue-number>` in body for tracking
- **Breaking changes**:
  - Add `!` before colon in commit header
  - Prefix body with `BREAKING CHANGE:` with description of changes
