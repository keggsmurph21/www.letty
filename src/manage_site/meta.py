import os
from pathlib import Path


# This gets passed in via the `setup-env` script!
ROOT = Path(os.environ["LETTY_ROOT"])

INPUT_DATA = ROOT / "data.yml"

WWW_ROOT = ROOT / "www"
STATIC_ROOT = WWW_ROOT / "static"
GENERATED_ROOT = WWW_ROOT / "generated"
