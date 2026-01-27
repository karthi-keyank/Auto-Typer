import json
import urllib.request
import urllib.error
from typing import Optional, Dict, Tuple


# ======================================================
# CONFIG
# ======================================================

GITHUB_API_LATEST_RELEASE = "https://api.github.com/repos/{owner}/{repo}/releases/latest"

# GitHub API requires a User-Agent
DEFAULT_HEADERS = {
    "User-Agent": "AutoTyper-App-Update-Checker"
}


# ======================================================
# VERSION UTILITIES
# ======================================================

def parse_version(version: str) -> Tuple[int, ...]:
    """
    Converts '3.2.1' -> (3, 2, 1)
    Strips leading 'v' if present.
    """
    version = version.strip().lower()
    if version.startswith("v"):
        version = version[1:]

    parts = version.split(".")
    nums = []

    for p in parts:
        try:
            nums.append(int(p))
        except ValueError:
            nums.append(0)

    return tuple(nums)


def is_newer(latest: str, current: str) -> bool:
    """
    Returns True if latest > current using semantic versioning.
    """
    return parse_version(latest) > parse_version(current)


# ======================================================
# GITHUB FETCH
# ======================================================

def fetch_latest_release(owner: str, repo: str) -> Optional[Dict]:
    """
    Fetches latest GitHub release metadata.
    Returns dict or None on failure.
    """
    url = GITHUB_API_LATEST_RELEASE.format(owner=owner, repo=repo)

    req = urllib.request.Request(url, headers=DEFAULT_HEADERS)

    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = resp.read().decode("utf-8")
            return json.loads(data)

    except urllib.error.HTTPError as e:
        # 404, 403, etc.
        print("Update check HTTP error:", e)
    except urllib.error.URLError as e:
        # Network issues
        print("Update check network error:", e)
    except Exception as e:
        print("Update check error:", e)

    return None


# ======================================================
# PUBLIC API
# ======================================================

def check_for_update(
    current_version: str,
    owner: str,
    repo: str
) -> Optional[Dict]:
    """
    Checks GitHub for a newer release.

    Returns:
        {
            "latest_version": str,
            "release_notes": str,
            "release_url": str
        }
    or None if:
        - no update
        - network failure
        - invalid response
    """

    release = fetch_latest_release(owner, repo)
    if not release:
        return None

    latest_version = release.get("tag_name", "")
    if not latest_version:
        return None

    if not is_newer(latest_version, current_version):
        return None

    return {
        "latest_version": latest_version.lstrip("v"),
        "release_notes": release.get("body", ""),
        "release_url": release.get("html_url", "")
    }
