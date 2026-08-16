import sys
from pathlib import Path


HERE = Path(__file__).resolve()
REPO = HERE.parents[3]
sys.path.insert(0, str(REPO / "src"))
sys.path.insert(0, str(HERE.parents[1] / "scripts"))

