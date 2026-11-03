"""Build the GroMush site: python3 -I build.py [--base /gromush-site/]. See README-build.md."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from gen.build import main  # noqa: E402

if __name__ == "__main__":
    sys.exit(main())
