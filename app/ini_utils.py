import sys, os
from pathlib import Path

def resource_path(relative_path: str) -> Path:
    """Retourne le chemin correct (dev ou PyInstaller onefile)."""
    if hasattr(sys, '_MEIPASS'):
        return Path(os.path.join(sys._MEIPASS, relative_path))
    return Path(os.path.abspath(relative_path))

def load_profiles(path):
    with open(path, encoding="utf-8") as f:
        return f.readlines()

def get_value(lines, section, key, default=""):
    in_section = False
    for line in lines:
        if line.strip().startswith("[") and line.strip().endswith("]"):
            in_section = (line.strip().lower() == f"[{section.lower()}]")
        elif in_section and line.strip().startswith(key+"="):
            return line.split("=", 1)[1].strip().strip('"')
    return default

def update_value(lines, section, key, new_value):
    in_section = False
    for i, line in enumerate(lines):
        if line.strip().startswith("[") and line.strip().endswith("]"):
            in_section = (line.strip().lower() == f"[{section.lower()}]")
        elif in_section and line.strip().startswith(key+"="):
            lines[i] = f"{key}=\"{new_value}\"\n"
            break
    return lines

def save_profiles(lines, path: Path):
    with open(path, "w", encoding="utf-8") as f:
        f.writelines(lines)
