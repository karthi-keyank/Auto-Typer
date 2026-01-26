import sys
from pathlib import Path
from typing import List, Dict


# ======================================================
# PYINSTALLER-SAFE BASE PATH
# ======================================================

def get_base_path():
    if getattr(sys, "frozen", False):
        return Path(sys.executable).parent
    return Path(__file__).parent


BASE_PATH = get_base_path()
CACHE_DIR = BASE_PATH / "text_cache"


# ======================================================
# CACHE
# ======================================================

def ensure_cache_dir():
    CACHE_DIR.mkdir(parents=True, exist_ok=True)


def save_text_file(filename: str, content: str):
    ensure_cache_dir()
    path = CACHE_DIR / filename
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def load_text_file(filename: str) -> str:
    path = CACHE_DIR / filename
    if not path.exists():
        raise FileNotFoundError(filename)
    with open(path, "r", encoding="utf-8") as f:
        return f.read()
    
def clear_cache():
    ensure_cache_dir()
    for file in CACHE_DIR.iterdir():
        if file.is_file():
            file.unlink()



# ======================================================
# PARSING
# ======================================================

def parse_filename(filename: str) -> Dict:
    name_part = filename.replace(".txt", "")
    parts = name_part.split()

    name_words = []
    tags = []

    for part in parts:
        if part.startswith("#"):
            tags.append(part[1:].lower())
        else:
            name_words.append(part.lower())

    return {
        "filename": filename,
        "name": " ".join(name_words),
        "name_words": name_words,
        "tags": tags
    }


def list_cached_files() -> List[Dict]:
    ensure_cache_dir()
    results = []
    for file in CACHE_DIR.iterdir():
        if file.is_file() and file.suffix == ".txt":
            results.append(parse_filename(file.name))
    return results


# ======================================================
# SMART SEARCH ENGINE 🔍
# ======================================================

def search_files(query: str) -> List[Dict]:
    query = query.strip().lower()
    if not query:
        return []

    tokens = query.split()

    name_tokens = [t for t in tokens if not t.startswith("#")]
    tag_tokens = [t[1:] for t in tokens if t.startswith("#")]

    results = []

    for info in list_cached_files():
        score = 0

        # ---------- TAG MATCHING ----------
        for qtag in tag_tokens:
            for tag in info["tags"]:
                if qtag == tag:
                    score += 5        # exact tag
                elif tag.startswith(qtag):
                    score += 3        # prefix tag

        # ---------- NAME MATCHING ----------
        for word in name_tokens:
            if word in info["name"]:
                score += 2            # partial match
            for nw in info["name_words"]:
                if nw.startswith(word):
                    score += 3        # prefix word

        # ---------- FALLBACK ----------
        # If user types "test" instead of "#test"
        for word in name_tokens:
            for tag in info["tags"]:
                if tag.startswith(word):
                    score += 1

        if score > 0:
            results.append({
                **info,
                "score": score
            })

    # Sort by relevance
    results.sort(key=lambda x: x["score"], reverse=True)
    return results
