# LandSight backend.

Backend for land parcel analysis: geometry validation, legal constraints, natural and infrastructure profiles, suitability scoring, background workflows. Stores domain logic, DTO/contracts, migrations, API and worker entrypoints.

## Requirements
- Python 3.14+
- [uv](https://docs.astral.sh/uv/)
- make
- pre-commit

## Setup
```bash
make install    # sync all dependencies (including extras)
make env        # install git hooks via pre-commit
```

## Run checks
```bash
make check      # check-lint + check-fmt
```

## Formatting
```bash
make fmt        # auto formatting
```
