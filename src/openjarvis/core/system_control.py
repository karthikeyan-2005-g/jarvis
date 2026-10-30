"""Windows System Controller for Iron Man Jarvis actions."""

from __future__ import annotations

import os
import re
import subprocess
import webbrowser
from typing import Optional


APP_COMMANDS = {
    "chrome": "start chrome",
    "google chrome": "start chrome",
    "browser": "start chrome",
    "edge": "start msedge",
    "microsoft edge": "start msedge",
    "notepad": "start notepad",
    "calculator": "start calc",
    "calc": "start calc",
    "code": "start code",
    "vs code": "start code",
    "vscode": "start code",
    "visual studio code": "start code",
    "pycharm": "start pycharm",
    "explorer": "start explorer",
    "file explorer": "start explorer",
    "files": "start explorer",
    "my computer": "start explorer",
    "this pc": "start explorer",
    "downloads": "start explorer shell:Downloads",
    "desktop": "start explorer shell:Desktop",
    "documents": "start explorer shell:Personal",
    "settings": "start ms-settings:",
    "task manager": "start taskmgr",
    "taskmgr": "start taskmgr",
    "terminal": "start wt",
    "powershell": "start powershell",
    "cmd": "start cmd",
    "command prompt": "start cmd",
    "paint": "start mspaint",
    "snipping tool": "start snippingtool",
}

WEBSITES = {
    "youtube": "https://www.youtube.com",
    "google": "https://www.google.com",
    "github": "https://www.github.com",
    "gmail": "https://mail.google.com",
    "whatsapp": "https://web.whatsapp.com",
    "chatgpt": "https://chatgpt.com",
    "reddit": "https://www.reddit.com",
    "twitter": "https://twitter.com",
    "x": "https://x.com",
    "linkedin": "https://www.linkedin.com",
    "wikipedia": "https://www.wikipedia.org",
}

KILL_TARGETS = {
    "chrome": "chrome.exe",
    "google chrome": "chrome.exe",
    "browser": "chrome.exe",
    "edge": "msedge.exe",
    "microsoft edge": "msedge.exe",
    "notepad": "notepad.exe",
    "calculator": "CalculatorApp.exe",
    "calc": "CalculatorApp.exe",
    "code": "Code.exe",
    "vscode": "Code.exe",
    "vs code": "Code.exe",
    "pycharm": "pycharm64.exe",
    "cmd": "cmd.exe",
    "paint": "mspaint.exe",
}


def clean_prompt(text: str) -> str:
    """Normalize input and strip conversational fluff (Jarvis, please, hey, etc.)."""
    s = text.strip().lower()
    # Remove leading conversational prefixes
    s = re.sub(
        r"^(?:hey\s+|hi\s+|hello\s+)?(?:jarvis[,\s]*)?(?:please\s+|can\s+you\s+|could\s+you\s+)?(?:please\s+)?",
        "",
        s,
    ).strip()
    # Remove trailing conversational suffixes
    s = re.sub(r"(?:\s+please|\s+for\s+me|\s+now|\s+right\s+now)$", "", s).strip()
    # Normalize punctuation except colons
    s = re.sub(r"[^\w\s:]", "", s)
    return s


def handle_system_command(user_text: str, dry_run: bool = False) -> Optional[str]:
    """Parse user intent and execute native Windows actions like Iron Man Jarvis.

    Returns a spoken response string if an action was handled, or None if the
    request should be passed to the LLM for general reasoning.
    """
    if not user_text:
        return None

    clean = clean_prompt(user_text)

    # -------------------------------------------------------------
    # 0. Tamil Commands Support
    # -------------------------------------------------------------
    if "குரோம்" in user_text:
        if any(w in user_text for w in ("மூடு", "க்ளோஸ்", "நிறுத்து")):
            if not dry_run:
                subprocess.Popen("taskkill /f /im chrome.exe", shell=True, stderr=subprocess.DEVNULL)
            return "கூகுள் குரோம் மூடப்பட்டது, ஐயா."
        if not dry_run:
            subprocess.Popen("cmd.exe /c start chrome", shell=True)
        return "கூகுள் குரோம் திறக்கப்படுகிறது, ஐயா."

    if "யூடியூப்" in user_text:
        if not dry_run:
            webbrowser.open("https://www.youtube.com")
        return "யூடியூப் திறக்கப்படுகிறது, ஐயா."

    if "நோட்பேட்" in user_text:
        if not dry_run:
            subprocess.Popen("cmd.exe /c start notepad", shell=True)
        return "நோட்பேட் திறக்கப்படுகிறது, ஐயா."

    if "கால்குலேட்டர்" in user_text:
        if not dry_run:
            subprocess.Popen("cmd.exe /c start calc", shell=True)
        return "கால்குலேட்டர் திறக்கப்படுகிறது, ஐயா."

    if any(k in user_text for k in ("பேட்டரி", "லேப்டாப் நிலை", "சிஸ்டம் நிலை")):
        try:
            import psutil
            battery = psutil.sensors_battery()
            cpu = psutil.cpu_percent(interval=0.1)
            ram = psutil.virtual_memory().percent
            batt_msg = f"பேட்டரி {battery.percent}% உள்ளது." if battery else "சார்ஜர் இணைக்கப்பட்டுள்ளது."
            return f"சிஸ்டம் நிலை: CPU பயன்பாடு {cpu}%, RAM பயன்பாடு {ram}%. {batt_msg}"
        except Exception:
            return "அனைத்து சிஸ்டம்களும் சீராக இயங்குகின்றன, ஐயா."

    # -------------------------------------------------------------
    # 1. Lock Screen / Workstation
    # -------------------------------------------------------------
    if clean in ("lock laptop", "lock pc", "lock screen", "lock windows", "lock computer"):
        if not dry_run:
            subprocess.Popen("rundll32.exe user32.dll,LockWorkStation", shell=True)
        return "Locking your workstation now, sir."

    # -------------------------------------------------------------
    # 2. Open Application (e.g. "open google chrome", "open notepad")
    # Evaluated before general websites to prioritize "google chrome" over "google"
    # -------------------------------------------------------------
    open_match = re.search(r"^(?:open|launch|start|run)\s+(?:the\s+|my\s+)?([a-zA-Z0-9_\s]+)", clean)
    if open_match:
        target = open_match.group(1).strip()
        # Sort keys by length descending to match "google chrome" before "chrome"
        for app_name in sorted(APP_COMMANDS.keys(), key=len, reverse=True):
            cmd = APP_COMMANDS[app_name]
            if target == app_name or target.startswith(f"{app_name} ") or target == f"the {app_name}":
                if not dry_run:
                    subprocess.Popen(f"cmd.exe /c {cmd}", shell=True)
                return f"Opening {app_name.title()} right away, sir."

    # -------------------------------------------------------------
    # 3. Open Website (e.g. "open youtube", "open github", "open google")
    # -------------------------------------------------------------
    for site, url in WEBSITES.items():
        if clean in (f"open {site}", f"launch {site}", f"{site} open", f"go to {site}") or \
           clean.startswith(f"open {site} ") or clean.startswith(f"go to {site} "):
            if not dry_run:
                webbrowser.open(url)
            return f"Opening {site.capitalize()} for you, sir."

    # -------------------------------------------------------------
    # 4. Close Application (e.g. "close chrome", "kill notepad")
    # -------------------------------------------------------------
    close_match = re.search(r"^(?:close|kill|exit|stop|terminate)\s+(?:the\s+)?([a-zA-Z0-9_\s]+)", clean)
    if close_match:
        target = close_match.group(1).strip()
        for name in sorted(KILL_TARGETS.keys(), key=len, reverse=True):
            exe = KILL_TARGETS[name]
            if target == name or target.startswith(f"{name} "):
                if not dry_run:
                    subprocess.Popen(f"taskkill /f /im {exe}", shell=True, stderr=subprocess.DEVNULL)
                return f"Closed {name.title()} for you, sir."

    # -------------------------------------------------------------
    # 5. Play on YouTube (e.g. "play believer on youtube" or "play starboy")
    # -------------------------------------------------------------
    play_match = re.search(r"^play\s+(.*?)(?:\s+on\s+youtube)?$", clean)
    if play_match:
        query = play_match.group(1).replace("on youtube", "").strip()
        if query:
            url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
            if not dry_run:
                webbrowser.open(url)
            return f"Playing {query} on YouTube for you, sir."

    # -------------------------------------------------------------
    # 6. Google Search (e.g. "search google for ...", "search for ...")
    # -------------------------------------------------------------
    search_match = re.search(r"^(?:search\s+google\s+for|search\s+for|google)\s+(.+)", clean)
    if search_match:
        query = search_match.group(1).strip()
        if query and not any(query.startswith(k) for k in APP_COMMANDS.keys()):
            url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
            if not dry_run:
                webbrowser.open(url)
            return f"Searching Google for {query}."

    # -------------------------------------------------------------
    # 7. Check Battery / Laptop System Specs
    # -------------------------------------------------------------
    if any(k in clean for k in ("battery", "battery status", "system status", "pc status", "laptop status", "specs")):
        try:
            import psutil
            battery = psutil.sensors_battery()
            cpu = psutil.cpu_percent(interval=0.1)
            ram = psutil.virtual_memory().percent
            batt_msg = f"Battery is at {battery.percent}%." if battery else "Running on AC power."
            return f"System status: CPU usage is at {cpu}%, RAM is at {ram}%. {batt_msg}"
        except Exception:
            return "All laptop systems are operating smoothly, sir."

    return None
