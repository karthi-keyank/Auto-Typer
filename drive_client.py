import os
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
# PYINSTALLER-SAFE PATH HANDLING
# ======================================================

def get_base_path():
    """
    Returns correct base path whether running as script
    or as PyInstaller exe.
    """
    if getattr(sys, "frozen", False):
        return Path(sys._MEIPASS)
    return Path(__file__).parent


BASE_PATH = get_base_path()
CREDENTIALS_PATH = BASE_PATH / CREDENTIALS_FILE
TOKEN_PATH = BASE_PATH / TOKEN_FILE


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

            with open(TOKEN_PATH, "w") as token:
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

        # Create folder
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
    # UPLOAD TEXT FILE
    # -------------------------------

    def upload_text(self, filename, text):
        file_metadata = {
            "name": filename,
            "parents": [self.folder_id]
        }

        text_bytes = io.BytesIO(text.encode("utf-8"))

        media = MediaIoBaseUpload(
            text_bytes,
            mimetype="text/plain",
            resumable=False
        )

        self.service.files().create(
            body=file_metadata,
            media_body=media,
            fields="id"
        ).execute()
    # -------------------------------
    # LIST ALL TEXT FILES
    # -------------------------------
    def list_text_files(self):
        """
        Returns list of dicts:
        [{id, name}]
        """
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
    # DOWNLOAD FILE
    # -------------------------------
    def download_file(self, file_id, save_path):
        """
        save_path: Path object
        """
        request = self.service.files().get_media(fileId=file_id)
        fh = io.FileIO(save_path, "wb")
        downloader = MediaIoBaseDownload(fh, request)

        done = False
        while not done:
            _, done = downloader.next_chunk()

        fh.close()
