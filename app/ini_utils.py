import sys, os
from pathlib import Path

def resource_path(relative_path: str) -> Path:
    if hasattr(sys, '_MEIPASS'):
        return Path(os.path.join(sys._MEIPASS, relative_path))
    return Path(os.path.abspath(relative_path))

def load_profiles(path):
    with open(path, encoding="utf-8") as f:
        return f.readlines()

def get_value(lines, section, key, default=""):
    """
    Retourne la valeur logique (sans guillemets externes).
    """
    header = f"[{section.lower()}]"
    in_section = False
    for line in lines:
        s = line.strip()
        if s.startswith("[") and s.endswith("]"):
            in_section = (s.lower() == header)
            continue
        if in_section and s.startswith(key + "="):
            raw = line.split("=", 1)[1].strip()
            # enlever guillemets externes si présents
            if len(raw) >= 2 and raw[0] == '"' and raw[-1] == '"':
                return raw[1:-1]
            return raw
    return default

def update_value(lines, section, key, new_value):
    """
    Met à jour STRICTEMENT une clé existante en conservant le style original:
    - si la valeur d'origine est entre guillemets -> garde les guillemets
    - sinon -> pas de guillemets
    Ne crée pas de nouvelle ligne.
    """
    header = f"[{section.lower()}]"
    in_section = False

    for i, line in enumerate(lines):
        s = line.strip()
        if s.startswith("[") and s.endswith("]"):
            in_section = (s.lower() == header)
            continue

        if in_section and s.startswith(key + "="):
            left, right = line.split("=", 1)
            right_stripped = right.strip()

            # détecter quote
            quoted = len(right_stripped) >= 2 and right_stripped[0] == '"' and right_stripped[-1] == '"'

            # préserver \n existant
            nl = "\n" if line.endswith("\n") else ""

            if quoted:
                lines[i] = f"{left}=\"{new_value}\"{nl}"
            else:
                lines[i] = f"{left}={new_value}{nl}"
            return lines

    # clé absente => on ne touche pas (important pour format strict)
    return lines

def save_profiles(lines, path: Path):
    with open(path, "w", encoding="utf-8") as f:
        f.writelines(lines)
