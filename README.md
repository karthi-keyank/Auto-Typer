# Auto Typer for Skillrack Assessments

## 📌 Problem

Skillrack does not allow pasting code.  
During timed assessments this becomes hard — especially when:

- students are sick or tired
- typing speed is slow
- code is already written and tested elsewhere

They still need to submit on time — but typing everything manually wastes precious minutes.

## 💡 Solution

This project is an **Auto Typer** built in Python.  
It simulates real keyboard typing (not paste), so your code is entered automatically.

Paste your code into the app → press Start → it types everything for you.

> Use responsibly and follow your institution rules. This tool is meant to **help students who genuinely struggle**, not for misuse.

---

## ✨ Features

- Simple GUI
- Start delay (time to switch to Skillrack)
- Adjustable typing speed (per-character delay)
- Pause / Resume
- Stop anytime
- Restart button
- Progress bar + live status
- **Coding Mode** — auto deletes extra paired brackets after typing

---

## 🚀 How it works

- **Tkinter** → GUI  
- **pyautogui** → fake keyboard typing  
- **Threads** → smooth UI while typing runs

You focus the Skillrack editor — the app types for you.

---

## 🚀 Installation (Super Easy — EXE Included)

You **don’t need Python**.

The project is packaged using **PyInstaller**.  
The executable is already built and available in the **dist/** folder.

---

## 🎮 Usage

1. Open **AutoTyper.exe**
2. Paste your code into the text box
3. Set:
   - Start Delay (seconds)
   - Character Delay (ms — 0 is fastest)
4. Turn on **Coding Mode** if your code uses many brackets
5. Place cursor in Skillrack editor
6. Click **Start**

Watch it type automatically ⚡

---

## ⚠️ Disclaimer

This tool supports students dealing with:

- health issues  
- accessibility needs  
- extreme time pressure  

Do not misuse it.  
You are responsible for following your platform’s rules.

---


