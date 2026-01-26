from datetime import datetime
from typing import List, Dict

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
        self.db = get_db()
        self.col = self.db.collection(COLLECTION_NAME)

    # --------------------------------------------------
    # UPLOAD TEXT (duplicate-safe)
    # --------------------------------------------------
    def upload_text(self, filename: str, text: str) -> str:
        existing_names = self._get_existing_names()

        final_name = self._resolve_duplicate(filename, existing_names)

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
        docs = self.col.stream()

        results = []
        for doc in docs:
            data = doc.to_dict()
            results.append({
                "id": doc.id,
                "name": data.get("name"),
            })

        return results

    # --------------------------------------------------
    # DOWNLOAD TEXT
    # --------------------------------------------------
    def download_text(self, doc_id: str) -> str:
        doc = self.col.document(doc_id).get()

        if not doc.exists:
            raise FileNotFoundError("Text not found in Firebase")

        return doc.to_dict().get("content", "")

    # --------------------------------------------------
    # INTERNAL HELPERS
    # --------------------------------------------------
    def _get_existing_names(self) -> set:
        docs = self.col.stream()
        return {doc.to_dict().get("name") for doc in docs}

    def _resolve_duplicate(self, filename: str, existing_names: set) -> str:
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
