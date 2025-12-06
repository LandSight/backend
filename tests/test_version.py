import re

from app import __version__


VERSION_PATTERN = re.compile(r"^(?P<major>\d+)\.(?P<minor>\d+)\.(?P<patch>\d+)(?P<suffix>.*)$")


def test_version_format() -> None:
    """Ensure __version__ looks like major.minor.patch optionally followed by any suffix such as 'a0'."""
    match = VERSION_PATTERN.match(__version__)
    assert match is not None, "Version must start with three numeric release components."
    assert all(part.isdigit() for part in match.group("major", "minor", "patch"))
