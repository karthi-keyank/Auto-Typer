import io
import sys
from pathlib import Path

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload, MediaIoBaseUpload
from google.auth.transport.requests import Request


# ======================================================
# CONFIG
# ======================================================

SCOPES = ["https://www.googleapis.com/auth/drive.file"]
DRIVE_FOLDER_NAME = "AutoTyperTexts"

CREDENTIALS_FILE = "credentials.json"
TOKEN_FILE = "token.json"


# ======================================================
# PATH HANDLING
# ======================================================

def get_runtime_path():
    """
    Writable path for runtime files (token.json).
    """
    if getattr(sys, "frozen", False):
        return Path(sys.executable).parent
    return Path(__file__).parent


def get_resource_path():
    """
    Read-only bundled resources (credentials.json).
    """
    if getattr(sys, "frozen", False):
        return Path(sys._MEIPASS)
    return Path(__file__).parent


RUNTIME_PATH = get_runtime_path()
RESOURCE_PATH = get_resource_path()

CREDENTIALS_PATH = RESOURCE_PATH / CREDENTIALS_FILE
TOKEN_PATH = RUNTIME_PATH / TOKEN_FILE


# ======================================================
# DRIVE CLIENT
# ======================================================

class DriveClient:
    def __init__(self):
        self.service = self._authenticate()
        self.folder_id = self._get_or_create_folder(DRIVE_FOLDER_NAME)

    # -------------------------------
    # AUTHENTICATION
    # -------------------------------
    def _authenticate(self):
        creds = None

        if TOKEN_PATH.exists():
            creds = Credentials.from_authorized_user_file(
                TOKEN_PATH, SCOPES
            )

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    CREDENTIALS_PATH, SCOPES
                )
                creds = flow.run_local_server(port=0)

            with open(TOKEN_PATH, "w", encoding="utf-8") as token:
                token.write(creds.to_json())

        return build("drive", "v3", credentials=creds)

    # -------------------------------
    # FOLDER MANAGEMENT
    # -------------------------------
    def _get_or_create_folder(self, name):
        query = (
            f"name='{name}' and "
            "mimeType='application/vnd.google-apps.folder' and "
            "trashed=false"
        )

        response = self.service.files().list(
            q=query,
            spaces="drive",
            fields="files(id, name)"
        ).execute()

        files = response.get("files", [])

        if files:
            return files[0]["id"]

        metadata = {
            "name": name,
            "mimeType": "application/vnd.google-apps.folder"
        }

        folder = self.service.files().create(
            body=metadata,
            fields="id"
        ).execute()

        return folder["id"]

    # -------------------------------
    # UPLOAD TEXT FILE (with duplicate handling)
    # -------------------------------
    def upload_text(self, filename, text):
        # 1️⃣ Get existing filenames in Drive folder
        existing_files = self.service.files().list(
            q=f"'{self.folder_id}' in parents and trashed=false",
            fields="files(name)"
        ).execute()

        existing_names = {f["name"] for f in existing_files.get("files", [])}

        # 2️⃣ Resolve duplicate filename
        final_name = filename

        if final_name in existing_names:
            # Split name and extension
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
                    final_name = candidate
                    break
                counter += 1

        # 3️⃣ Upload with resolved name
        file_metadata = {
            "name": final_name,
            "parents": [self.folder_id]
        }

        media = MediaIoBaseUpload(
            io.BytesIO(text.encode("utf-8")),
            mimetype="text/plain",
            resumable=False
        )

        self.service.files().create(
            body=file_metadata,
            media_body=media,
            fields="id"
        ).execute()
        
        return final_name
    # -------------------------------
    # LIST ALL TEXT FILES
    # -------------------------------
    def list_text_files(self):
        query = (
            f"'{self.folder_id}' in parents and "
            "mimeType='text/plain' and "
            "trashed=false"
        )

        response = self.service.files().list(
            q=query,
            fields="files(id, name)"
        ).execute()

        return response.get("files", [])

    # -------------------------------
    # DOWNLOAD FILE (to bytes)
    # -------------------------------
    def download_file(self, file_id) -> str:
        request = self.service.files().get_media(fileId=file_id)
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)

        done = False
        while not done:
            _, done = downloader.next_chunk()

        return fh.getvalue().decode("utf-8")


# ======================================================
# LOGOUT (OAuth reset)
# ======================================================

def logout():
    """
    Logs out from Google by deleting stored OAuth token.
    Next Drive action will ask for login again.
    """
    if TOKEN_PATH.exists():
        TOKEN_PATH.unlink()
