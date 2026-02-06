import sys
from pathlib import Path
import firebase_admin
from firebase_admin import credentials, firestore


# ======================================================
# RESOURCE PATH RESOLUTION (PyInstaller safe)
# ======================================================

def _possible_resource_paths() -> list[Path]:
    """
    Returns all possible base paths where bundled resources may exist.
    Order matters: earlier = higher priority.
    """
    paths = []

    # 1️⃣ PyInstaller onefile extraction dir
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        paths.append(Path(sys._MEIPASS))

    # 2️⃣ Executable directory
    paths.append(Path(sys.executable).parent)

    # 3️⃣ Normal Python execution (source folder)
    paths.append(Path(__file__).parent)

    return paths


def _find_resource(filename: str) -> Path:
    """
    Searches for a resource file in all valid runtime locations.
    Raises FileNotFoundError with full diagnostics if missing.
    """
    checked = []

    for base in _possible_resource_paths():
        candidate = base / filename
        checked.append(str(candidate))
        if candidate.exists():
            return candidate

    raise FileNotFoundError(
        "Required resource file not found:\n"
        f"  File: {filename}\n\n"
        "Checked locations:\n  - "
        + "\n  - ".join(checked)
    )


# ======================================================
# FIREBASE CONFIG
# ======================================================

SERVICE_ACCOUNT_FILE = "firebase_service_account.json"

# Resolve service account path robustly
SERVICE_ACCOUNT_PATH = _find_resource(SERVICE_ACCOUNT_FILE)


# ======================================================
# FIREBASE INITIALIZATION
# ======================================================

_app = None
_db = None


def init_firebase():
    """
    Initializes Firebase Admin SDK once.
    Raises clear, actionable errors on failure.
    """
    global _app, _db

    if _app is not None:
        return _db

    try:
        cred = credentials.Certificate(SERVICE_ACCOUNT_PATH)
        _app = firebase_admin.initialize_app(cred)
        _db = firestore.client()
        return _db

    except Exception as e:
        raise RuntimeError(
            "Firebase initialization failed.\n\n"
            f"Service account path:\n  {SERVICE_ACCOUNT_PATH}\n\n"
            "Possible causes:\n"
            "- Invalid service account JSON\n"
            "- Firebase Admin SDK not bundled correctly\n"
            "- Corrupted PyInstaller build\n\n"
            f"Original error:\n{e}"
        ) from e


def get_db():
    """
    Returns Firestore client (lazy init).
    """
    if _db is None:
        return init_firebase()
    return _db
