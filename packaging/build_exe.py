"""EXPERIMENTAL: bundle Guardian as a Windows executable (no Python needed on the target PC).  Run ON WINDOWS inside the venv:
   pip install pyinstaller && python packaging/build_exe.py      ->  dist/AttackReplayGuardian/AttackReplayGuardian.exe
Not verified by the author (built on Linux). install.py is the supported path for the demo."""
import subprocess, sys
from pathlib import Path
R = Path(__file__).resolve().parent.parent
sep = ";" if sys.platform.startswith("win") else ":"
subprocess.check_call([sys.executable, "-m", "PyInstaller", "--noconfirm", "--onedir", "--name", "AttackReplayGuardian", "--windowed",
    "--collect-all", "sklearn", "--collect-all", "uvicorn", "--hidden-import", "keyring.backends.Windows",
    "--add-data", f"{R/'web'}{sep}web", "--add-data", f"{R/'models'}{sep}models", "--add-data", f"{R/'data/splits'}{sep}data/splits", "--add-data", f"{R/'data/raw'}{sep}data/raw", "--add-data", f"{R/'data/supplement'}{sep}data/supplement",
    str(R / "guardian.py")], cwd=R)
