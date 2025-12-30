# Versioning

This project follows Semantic Versioning [SemVer](https://semver.org/) and uses a single version for the application.

## SemVer Rules

- **MAJOR**: [breaking changes](breaking-change.md) or backward-incompatible behavior
- **MINOR**: backward-compatible features or API additions
- **PATCH**: backward-compatible bug fixes and internal changes

## Pre-release Tags

We use release candidates for stabilization:

- Format: `X.Y.Z-rc.N`
- Examples: `1.2.0-rc.1`, `1.2.0-rc.2`
- A release candidate must be followed by the final `X.Y.Z` without
  additional changes that would invalidate the candidate
