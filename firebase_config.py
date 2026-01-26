import sys
from pathlib import Path
import firebase_admin
from firebase_admin import credentials, firestore


# ======================================================
# PATH HANDLING (PyInstaller safe)
# ======================================================

def get_resource_path():
    if getattr(sys, "frozen", False):
        return Path(sys._MEIPASS)
    return Path(__file__).parent


RESOURCE_PATH = get_resource_path()

# 🔑 Firebase service account key
SERVICE_ACCOUNT_FILE = "firebase_service_account.json"
SERVICE_ACCOUNT_PATH = RESOURCE_PATH / SERVICE_ACCOUNT_FILE


# ======================================================
# FIREBASE INIT
# ======================================================

_app = None
_db = None


def init_firebase():
    global _app, _db

    if _app is not None:
        return _db

    if not SERVICE_ACCOUNT_PATH.exists():
        raise FileNotFoundError(
            "Firebase service account key not found:\n"
            f"{SERVICE_ACCOUNT_PATH}"
        )

    cred = credentials.Certificate(SERVICE_ACCOUNT_PATH)
    _app = firebase_admin.initialize_app(cred)
    _db = firestore.client()

    return _db


def get_db():
    if _db is None:
        return init_firebase()
    return _db
