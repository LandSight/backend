from pathlib import Path


PROJECT_DIR = Path(__file__).parent.parent.parent.parent.resolve()
ENV_FILE = PROJECT_DIR / ".env"

COLLATION_CI_TEXT_NAME = "ci_text"
