# Code Style

Code quality is enforced by the ``ruff`` and ``ty`` linters, configured in ``pyproject.toml``.

## Basic Rules
- **PEP 8**: baseline recommendations for Python code style
- **Line length**: 120 characters
- **Quotes**: Double quotes only (`"`)
- **Docstrings**: [NumPy style](https://numpydoc.readthedocs.io/en/latest/format.html)
    - The `Parameters` section is used to describe parameters, including parameter name, type, and a short description
    - The `Returns` section is used to describe return values
    - The `Raises` section is used to describe possible exceptions
    - Additional sections may be added when needed (for example, `Examples`, `Notes`, `Warnings`, `See Also`, etc.)
- **Type annotations**: Mandatory everywhere
- **Modern syntax**: Python 3.14+
- **Naming follows**:
    - Classes — `CamelCase`
    - Functions and variables — `snake_case`
    - Constants — `UPPER_CASE`
    - Private classes, functions, and variables must start with `_`

### Special exceptions:
- **`__init__.py`**: Unused imports allowed
- **`tests/`**: Magic numbers allowed and `assert` statements allowed

## Automation
- `just fmt` — automatic formatting
- `just lint` — style and type checking
