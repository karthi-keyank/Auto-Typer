---
# 🧠 AutoTyper for Skillrack Assessments (v3.1)

AutoTyper is a **Windows desktop application** that automatically types text and code **character by character**, simulating real keyboard input.

It is designed to help during platforms like **Skillrack**, where **copy–paste is disabled**, especially in **timed assessments**.

---

## 📌 The Problem

Skillrack and similar platforms **do not allow pasting code**.

During timed assessments, this becomes difficult when:

* typing speed is slow
* the user is tired, sick, or under pressure
* the solution is already written and tested elsewhere

Manually retyping everything wastes **valuable time** and increases mistakes.

---

## 💡 The Solution

AutoTyper **simulates real keyboard typing** instead of pasting.

You paste your prepared code into AutoTyper →
place the cursor in the Skillrack editor →
click **Start** →
AutoTyper types everything automatically.

> ⚠️ Use responsibly and follow your institution’s rules.
> This tool is meant to **assist**, not to enable misuse.

---

## ✨ Key Features (v3.1)

### ⌨️ Auto Typing

* Simulates **real keyboard input**
* Adjustable typing speed (per-character delay)
* Start delay (time to switch to Skillrack tab)
* Pause / Resume
* Stop anytime
* Restart typing instantly

---

### 🧠 Coding Mode

* Automatically removes extra paired brackets
* Useful for C, C++, Java, Python, etc.
* Prevents common auto-typing bracket issues

---

### 🔍 Smart Search

* Search snippets by **name**
* Search using **#tags**
* Partial and mixed search supported

Examples:

```
binary
#python
regex #python
```

---

### ☁️ Cloud Sync (Firebase)

* Upload text/code snippets to the cloud
* Fetch snippets from anywhere
* Multi-line text supported
* No copy–paste limitations
* Fast and reliable sync

> All snippets are stored in **Firebase Firestore**
> The backend is **community-ready** by design.

---

### 📁 Local Cache (Offline-First)

* All fetched snippets are stored locally
* Search works **even without internet**
* One-click **Clear Local Cache**
* Extremely fast search performance

---

### 🔁 Duplicate Upload Handling

* Automatically renames duplicates:

```
code.txt
code (1).txt
code (2).txt
```

* No overwriting
* No prompts
* Safe and predictable behavior

---

### ⚙️ Settings Panel

* Clear Local Cache
* Reset Cloud Connection
* Clean modal UI
* Confirmation for destructive actions

---

### 🎨 Polished UI

* Clean, modern layout
* Search dropdown results
* Clear section separation
* Status bar with live updates
* Button-only controls (no accidental keyboard shortcuts)

---

## 🛠️ How It Works (Technical Overview)

* **Tkinter** → GUI
* **pyautogui** → keyboard input simulation
* **Firebase Firestore** → cloud snippet storage
* **Firebase Admin SDK** → secure backend access
* **Threading** → non-blocking UI
* **Offline-first design** → fast & reliable

---

## 🚀 Installation (Windows – EXE)

You **do NOT need Python**.

The app is packaged using **PyInstaller**.

### Option 1: Use Prebuilt EXE

* Download `AutoTyper.exe`
* Run directly (no setup required)

---

### Option 2: Build Yourself

Requirements:

* Python 3.9+
* `firebase-admin`
* `pyautogui`
* `pyinstaller`

Build command:

```powershell
pyinstaller --onefile --noconsole --add-data "firebase_service_account.json;." --name AutoTyper main.py
```

> The Firebase service account file is bundled securely inside the EXE.

---

## 🎮 How to Use

1. Open **AutoTyper.exe**
2. Paste your code/text into the editor
3. Set:

   * **Start Delay** (seconds)
   * **Character Delay** (ms — `0` is fastest)
4. Enable **Coding Mode** if needed
5. Place cursor in Skillrack editor
6. Click **Start**

AutoTyper will type everything automatically ⚡

---

## ⚠️ Important Notes

* AutoTyper types like a **human keyboard**, not paste
* Internet is required only for cloud sync
* Local cache works offline
* Cloud data is not deleted when clearing cache

---

## ⚠️ Disclaimer

This tool is intended to support users who face:

* health issues
* accessibility limitations
* extreme time pressure

You are **fully responsible** for complying with:

* Skillrack rules
* Institutional policies
* Examination guidelines

The developer is not responsible for misuse.

---

## 🔮 Future Plans

* Community/shared snippet library
* Public / private snippets
* User authentication
* Dark mode
* Snippet categories & folders
* Content preview in search
* Version history
* Settings persistence

---

## ⭐ Final Note

AutoTyper v3.1 is designed to be:

* Fast
* Safe
* Offline-first
* Cloud-powered

It is no longer just an auto typer —
it’s a **personal and community-ready code & text assistant** 🚀

