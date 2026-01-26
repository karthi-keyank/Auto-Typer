---

# 🧠 AutoTyper for Skillrack Assessments (v3.0)

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

## ✨ Key Features (v3.0)

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

### ☁️ Google Drive Integration

* Upload text/code snippets to Google Drive
* Fetch snippets from Drive
* Automatic Drive folder creation (`AutoTyperTexts`)
* Secure OAuth login via browser
* Logout supported

> Each user syncs with **their own Google Drive**
> Files are private and not shared across users.
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
* Logout from Google Drive
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
* **Google Drive API** → cloud sync
* **Threading** → non-blocking UI
* **Offline-first design** → fast & reliable

---

## 🚀 Installation (Windows – EXE)

You **do NOT need Python**.

The app is packaged using **PyInstaller**.

### Option 1: Use Prebuilt EXE

* Download `AutoTyper.exe`
* Run directly (no setup required)

### Option 2: Build Yourself

```powershell
pyinstaller --onefile --windowed --name AutoTyper --add-data "credentials.json;." main.py
```

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
* Google login is required only for Drive features
* Logging out removes stored Drive access
* Local cache can be cleared anytime

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
* Dark mode
* Snippet categories & folders
* Content preview in search
* Version history
* Settings persistence

---

## ⭐ Final Note

AutoTyper v3.0 is designed to be:

* Fast
* Safe
* Offline-first
* Productivity-focused

It is no longer just an auto typer —
it’s a **personal code & text assistant**.
