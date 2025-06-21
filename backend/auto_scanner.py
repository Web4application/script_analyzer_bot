import os
import json
from pathlib import Path
from backend.llm import analyze_js_code, generate_readme

HISTORY_FILE = Path.home() / ".analyzer_bot_history.json"
PROJECT_ROOTS = [
    Path.home() / "Projects",
    Path.home() / "Documents/code",
]

SUPPORTED_EXT = [".js", ".ts", ".py", ".go"]

def load_history():
    if HISTORY_FILE.exists():
        with open(HISTORY_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_history(history):
    with open(HISTORY_FILE, 'w') as f:
        json.dump(history, f, indent=2)

def scan_projects():
    history = load_history()

    for root in PROJECT_ROOTS:
        if not root.exists(): continue

        for dirpath, _, filenames in os.walk(root):
            if any(f.endswith(tuple(SUPPORTED_EXT)) for f in filenames):
                key = str(Path(dirpath).resolve())
                if key not in history:
                    history[key] = {"status": "new"}

    save_history(history)
    return history

def analyze_and_complete(key):
    js_files = []
    for dirpath, _, filenames in os.walk(key):
        for file in filenames:
            if file.endswith(".js"):
                js_files.append(Path(dirpath) / file)

    if not js_files:
        return {"status": "no-js"}

    all_code = "\n\n".join((Path(f).read_text() for f in js_files))
    analysis = analyze_js_code(all_code)
    readme = generate_readme(all_code)

    # Save README
    readme_path = Path(key) / "README.generated.md"
    with open(readme_path, "w") as f:
        f.write(readme)

    # Update history
    history = load_history()
    history[key]["status"] = "completed"
    history[key]["readme_path"] = str(readme_path)
    save_history(history)

    return {"status": "done", "readme": readme}
