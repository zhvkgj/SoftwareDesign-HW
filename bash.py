from src.bash_runner.runner import Bash
import sys

exit(Bash.run(sys.stdin, sys.stdout, sys.stderr))
