from src.bash_runner.runner import bash
import sys

exit(bash(sys.stdin, sys.stdout, sys.stderr))
