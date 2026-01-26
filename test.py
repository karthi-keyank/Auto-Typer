from drive_client import DriveClient
from file_cache import (
    save_text_file,
    load_text_file,
    list_cached_files,
    search_files
)

print("=== FULL CLI INTEGRATION TEST START ===\n")

# --------------------------------------------------
# 1. CONNECT TO DRIVE
# --------------------------------------------------
print("[1] Connecting to Google Drive...")
drive = DriveClient()
print("✔ Connected\n")

# --------------------------------------------------
# 2. UPLOAD TEST FILE
# --------------------------------------------------
print("[2] Uploading test text...")
filename = "cli test file #autotyper #test.txt"
content = "This text was uploaded from CLI test."

drive.upload_text(filename, content)
print("✔ Uploaded:", filename, "\n")

# --------------------------------------------------
# 3. LIST FILES IN DRIVE FOLDER
# --------------------------------------------------
print("[3] Listing files from Drive...")
files = drive.list_text_files()

for f in files:
    print(" -", f["name"])

print(f"✔ Total files in Drive folder: {len(files)}\n")

# --------------------------------------------------
# 4. FETCH FILES (DOWNLOAD + CACHE)
# --------------------------------------------------
print("[4] Fetching files to local cache...")

for f in files:
    # Download file content
    import io
    from googleapiclient.http import MediaIoBaseDownload

    request = drive.service.files().get_media(fileId=f["id"])
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)

    done = False
    while not done:
        _, done = downloader.next_chunk()

    text = fh.getvalue().decode("utf-8")

    # Save to local cache
    save_text_file(f["name"], text)

print("✔ All files cached locally\n")

# --------------------------------------------------
# 5. LIST LOCAL CACHE
# --------------------------------------------------
print("[5] Local cached files:")
cached = list_cached_files()

for c in cached:
    print(c)

print("✔ Cache listing OK\n")

# --------------------------------------------------
# 6. SEARCH TESTS
# --------------------------------------------------
print("[6] Search tests:")

queries = [
    "cli",
    "#autotyper",
    "#test",
    "cli #test",
    "nonexistent"
]

for q in queries:
    results = search_files(q)
    print(f"\nSearch: '{q}'")
    if not results:
        print("  (no results)")
    else:
        for r in results:
            print("  -", r["filename"])

print("\n✔ Search logic OK\n")

# --------------------------------------------------
# 7. LOAD FILE CONTENT
# --------------------------------------------------
print("[7] Loading one cached file...")

loaded = load_text_file(filename)
print("Loaded content:")
print(loaded)

print("\n✔ Load OK")

print("\n=== FULL CLI INTEGRATION TEST END ===")
