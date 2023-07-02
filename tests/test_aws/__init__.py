import sys
from pathlib import Path

TEST_DIR = Path(__file__).parent
FIXTURE_DIR = TEST_DIR / "fixtures"

AWS_DIR = TEST_DIR.parent.parent / "aws"

sys.path.insert(0, AWS_DIR.as_posix())
