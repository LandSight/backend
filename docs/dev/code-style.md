# Code Style

## Basic Rules
- **Line length**: 120 characters
- **Quotes**: Double quotes only (`"`)
- **Docstrings**: NumPy style
- **Type annotations**: Mandatory everywhere
- **Modern syntax**: Python 3.14+

## Code Checking
All rules are defined in Ruff configuration (`pyproject.toml`):
- Enabled rules: `ANN`, `ARG`, `B`, `C4`, `D`, `DTZ`, `E`, `ERA`, `F`, `I`, `N`, `PGH`, `PLC`, `PLE`, `PLR`, `PLW`, `RSE`, `RUF`, `S`, `SIM`, `T20`, `TC`, `TRY`, `UP`, `W`
- Disabled rules: `A003`, `D100`, `D104`, `D105`, `D107`, `E203`, `E501`

### Special exceptions:
- **`__init__.py`**: Unused imports allowed (`F401`)
- **`tests/`**: Magic numbers allowed (`PLR2004`) and `assert` statements allowed (`S101`)

## Automation
- `just fmt` — automatic formatting
- `just lint` — style and type checking
