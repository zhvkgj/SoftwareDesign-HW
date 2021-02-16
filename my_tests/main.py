import sys
import pytest
from pathlib import Path

TEST_DIR = str(Path(__file__).parent.absolute())

if __name__ == "__main__":
    sys.exit(pytest.main([TEST_DIR, '-s']))
