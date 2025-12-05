# LandSight backend.

Backend for land parcel analysis: geometry validation, legal constraints, natural and infrastructure profiles, suitability scoring, background workflows. Stores domain logic, DTO/contracts, migrations, API and worker entrypoints.

## Requirements
- [uv](https://docs.astral.sh/uv/) ≥ 0.9
- make ≥ 4.4
- pre-commit ≥ 4.4

## Setup
```bash
make install         # install dependencies for prod

make install-dev     # install dependencies for development

make setup-dev       # install dev deps and setup dev environment
```

## Run checks
```bash
make check      # check-lint + check-fmt
```

## Formatting
```bash
make fmt        # auto formatting
```
