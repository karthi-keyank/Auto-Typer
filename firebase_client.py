from typing import List, Dict, Set
from datetime import datetime

from firebase_admin import firestore
from firebase_config import get_db


# ======================================================
# CONFIG
# ======================================================

COLLECTION_NAME = "texts"


# ======================================================
# FIREBASE CLIENT
# ======================================================

class FirebaseClient:
    def __init__(self):
        try:
            self.db = get_db()
            self.col = self.db.collection(COLLECTION_NAME)
        except Exception as e:
            raise RuntimeError(
                "Failed to initialize Firebase client.\n"
                f"{e}"
            ) from e

    # --------------------------------------------------
    # UPLOAD TEXT (duplicate-safe)
    # --------------------------------------------------
    def upload_text(self, filename: str, text: str) -> str:
        if not filename or not text:
            raise ValueError("Filename or text is empty")

        existing_names = self._get_existing_names()
        final_name = self._resolve_duplicate(
            filename,
            existing_names
        )

        self.col.add({
            "name": final_name,
            "content": text,
            "created_at": firestore.SERVER_TIMESTAMP,
        })

        return final_name

    # --------------------------------------------------
    # LIST TEXT FILES
    # --------------------------------------------------
    def list_text_files(self) -> List[Dict]:
        results = []

        try:
            docs = self.col.stream()
        except Exception as e:
            raise RuntimeError(
                "Failed to list texts from Firebase.\n"
                f"{e}"
            ) from e

        for doc in docs:
            data = doc.to_dict()
            if not data:
                continue

            name = data.get("name")
            if not isinstance(name, str):
                continue

            results.append({
                "id": doc.id,
                "name": name,
            })

        return results

    # --------------------------------------------------
    # DOWNLOAD TEXT
    # --------------------------------------------------
    def download_text(self, doc_id: str) -> str:
        if not doc_id:
            raise ValueError("Document ID is empty")

        doc = self.col.document(doc_id).get()

        if not doc.exists:
            raise FileNotFoundError(
                "Text not found in Firebase"
            )

        data = doc.to_dict() or {}
        content = data.get("content")

        if not isinstance(content, str):
            return ""

        return content

    # --------------------------------------------------
    # INTERNAL HELPERS
    # --------------------------------------------------
    def _get_existing_names(self) -> Set[str]:
        names = set()

        try:
            docs = self.col.stream()
        except Exception:
            return names

        for doc in docs:
            data = doc.to_dict()
            if not data:
                continue

            name = data.get("name")
            if isinstance(name, str):
                names.add(name)

        return names

    def _resolve_duplicate(
        self,
        filename: str,
        existing_names: Set[str]
    ) -> str:
        if filename not in existing_names:
            return filename

        if filename.lower().endswith(".txt"):
            base = filename[:-4]
            ext = ".txt"
        else:
            base = filename
            ext = ""

        counter = 1
        while True:
            candidate = f"{base} ({counter}){ext}"
            if candidate not in existing_names:
                return candidate
            counter += 1
