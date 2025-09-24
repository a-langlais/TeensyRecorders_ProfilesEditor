import dearpygui.dearpygui as dpg
from PIL import Image
from pathlib import Path
import re
import sys, os

# ---------------------
# Gestion des ressources
# ---------------------
def resource_path(relative_path):
    """Retourne le chemin correct que ce soit en mode script ou compilé."""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    elif getattr(sys, 'frozen', False):
        return os.path.join(os.path.dirname(sys.executable), relative_path)
    else:
        return os.path.join(os.path.abspath("."), relative_path)

INI_PATH = Path(resource_path("initial_profile/Profiles.ini"))
FONT_PATH = resource_path("fonts/DejaVuSans.ttf")
IMG_PATH = resource_path("img/logo_PR.png")

# ---------------------
# Utilitaires INI
# ---------------------
def load_profiles(path):
    with open(path, encoding = "utf-8") as f:
        return f.readlines()

def get_value(lines, section, key, default = ""):
    in_section = False
    for line in lines:
        if line.strip().startswith("[") and line.strip().endswith("]"):
            in_section = (line.strip().lower() == f"[{section.lower()}]")
        elif in_section and line.strip().startswith(key+"="):
            return line.split("=",1)[1].strip()
    return default

def update_value(lines, section, key, new_value):
    in_section = False
    for i, line in enumerate(lines):
        if line.strip().startswith("[") and line.strip().endswith("]"):
            in_section = (line.strip().lower() == f"[{section.lower()}]")
        elif in_section and line.strip().startswith(key+"="):
            lines[i] = f"{key}={new_value}\n"
            break
    return lines

def save_profiles(lines, path):
    with open(path, "w", encoding = "utf-8") as f:
        f.writelines(lines)

# ---------------------
# Chargement initial
# ---------------------
lines = load_profiles(INI_PATH)

# Nom des profils
PROFILE_LABELS = {
    "Profile 2": "2",
    "Profile 3": "3",
    "Profile 4": "4",
    "Profile 5": "5"
}

# Champs exposés
FIELDS = {
    "ProfileName": {"type": "text"},
    "OpMode": {"type": "combo", "choices": [
        "Auto record","Walkin. Protoc.","Road Protocol",
        "Fixed P. Proto.","RhinoLogger","Heterodyne",
        "Timed recording","Audio Rec.","Synchro"
    ]},
    "StartTime": {"type": "text"},
    "EndTime": {"type": "text"},
    "SampFreqU": {"type": "combo", "choices": ["24","48","96","192","250","384","500"]},
    "NumericGain": {"type": "combo", "choices": ["0","6","12","18","24"]},
    "StereoMode": {"type": "combo", "choices": ["Stereo","MonoRight","MonoLeft"]},
    "MicrophoneType": {"type": "combo", "choices": ["SPU0410","ICS40730","FG23329"]},
    "LEDSynchro": {"type": "combo", "choices": ["NO","REC","3 REC"]},
    "WavPrefix": {"type": "text"},
    "MaxFileLength": {"type": "int", "min": 1, "max": 999, "default": 60},
    "MinFreqUS": {"type": "int", "min": 10000, "max": 120000},
    "MaxFreqUS": {"type": "int", "min": 20000, "max": 120000},
    "MinLevel": {"type": "int", "min": 0, "max": 100, "default": 15},
    "PreTrigger": {"type": "int", "min": 0, "max": 10, "default": 5},
    "THSensorEnable": {"type": "combo", "choices": ["0","1"], "default": "1"},
    "GPSenable": {"type": "combo", "choices": ["0","1"], "default": "0"},
}

# Groupes de champs
SECTION_TITLES = {
    "Profil": ["ProfileName", "OpMode"],
    "Horaires": ["StartTime", "EndTime"],
    "Audio": ["SampFreqU", "NumericGain", "StereoMode", "MicrophoneType"],
    "Fichiers": ["LEDSynchro", "WavPrefix", "MaxFileLength"],
    "Fréquences": ["MinFreqUS", "MaxFreqUS", "MinLevel", "PreTrigger"],
    "Capteurs": ["THSensorEnable", "GPSenable"]
}


# ---------------------
# Cache mémoire
# ---------------------
profile_cache = {pid: {} for pid in PROFILE_LABELS.values()}

# ---------------------
# Validation
# ---------------------
def validate_name(text, limit, warn_tag):
    if re.search(r"[^A-Za-z0-9 _-]", text):
        dpg.set_value(warn_tag, "[WARNING] Seuls A–Z, 0–9, espace, - et _ sont autorisés")
        dpg.configure_item(warn_tag, show = True, color=(255, 165, 0))
        return False
    elif len(text) > limit:
        dpg.set_value(warn_tag, f"[WARNING] Limité à {limit} caractères max")
        dpg.configure_item(warn_tag, show = True, color=(255, 165, 0))
        return False
    else:
        dpg.configure_item(warn_tag, show = False)
        return True

def validate_final(name: str, limit: int) -> str:
    name = re.sub(r"[^A-Za-z0-9 _-]", "", str(name))
    return name[:limit]

def validate_int(val, min_val, max_val, warn_tag):
    try:
        v = int(val)
        if v < min_val or v > max_val:
            dpg.set_value(warn_tag, f"[WARNING] Doit être entre {min_val} et {max_val}")
            dpg.configure_item(warn_tag, show = True, color=(255, 165, 0))
            return False
        else:
            dpg.configure_item(warn_tag, show = False)
            return True
    except ValueError:
        if str(val).strip() != "":
            dpg.set_value(warn_tag, "[WARNING] Doit être un entier")
            dpg.configure_item(warn_tag, show = True, color=(255, 165, 0))
            return False
        else:
            dpg.configure_item(warn_tag, show = False)
            return True

# ---------------------
# Callback unique pour maj + validation
# ---------------------
def on_value_change(sender, app_data, user_data):
    profile_id, key, meta = user_data
    section = f"Profile_{profile_id}"

    # validation
    if key in ["ProfileName", "WavPrefix"]:
        limit = 11 if key == "ProfileName" else 5
        warn_tag = f"{section}_{key}_warn"
        validate_name(app_data, limit, warn_tag)

    elif meta["type"] == "int":
        warn_tag = f"{section}_{key}_warn"
        validate_int(app_data, meta["min"], meta["max"], warn_tag)

    # mettre en cache
    profile_cache[profile_id][key] = app_data

# ---------------------
# Callbacks
# ---------------------
def show_profile(sender, app_data, user_data):
    label = dpg.get_value("profile_selector")
    profile_id = PROFILE_LABELS[label]
    section = f"Profile_{profile_id}"

    dpg.delete_item("form_area", children_only = True)

    for section_name, keys in SECTION_TITLES.items():
        # Titre de la section
        with dpg.group(parent = "form_area"):
            dpg.add_text(section_name, color = (0, 150, 250))
            dpg.add_separator()

        # Paramètres de la section
        for key in keys:
            meta = FIELDS[key]
            raw_val = get_value(lines, section, key, default = str(meta.get("default", "")))
            val = profile_cache[profile_id].get(key, str(raw_val).strip('"'))

            with dpg.group(horizontal = True, parent = "form_area"):
                dpg.add_text(f"{key:15}")
                if meta["type"] == "text":
                    dpg.add_input_text(default_value = val, tag = f"{section}_{key}", width = 200,
                                       callback = on_value_change, user_data = (profile_id, key, meta))
                    if key in ["ProfileName", "WavPrefix"]:
                        dpg.add_text("", tag = f"{section}_{key}_warn", color = (255, 165, 0), show = False)

                elif meta["type"] == "combo":
                    choices = meta["choices"].copy()
                    if val not in choices:
                        choices.append(val)
                    dpg.add_combo(choices, default_value = val or str(meta.get("default", "0")),
                                  tag = f"{section}_{key}", width=200,
                                  callback=on_value_change, user_data=(profile_id,key,meta))

                elif meta["type"] == "int":
                    dpg.add_input_text(default_value = val, tag = f"{section}_{key}", width = 100,
                                       callback = on_value_change, user_data = (profile_id, key, meta))
                    dpg.add_text("", tag = f"{section}_{key}_warn", color=(255, 165, 0), show = False)


def save_callback():
    global lines
    label = dpg.get_value("profile_selector")
    profile_id = PROFILE_LABELS[label]
    section = f"Profile_{profile_id}"

    for key, meta in FIELDS.items():
        val = profile_cache[profile_id].get(key, dpg.get_value(f"{section}_{key}"))

        if key == "ProfileName":
            val = validate_final(val, 11)
            if not val:
                dpg.set_value("output", "[ERROR] ProfileName invalide")
                dpg.configure_item("output", color = (200, 0, 0))
                return
        elif key == "WavPrefix":
            val = validate_final(val, 5)
            if not val:
                dpg.set_value("output", "[ERROR] WavPrefix invalide")
                dpg.configure_item("output", color = (200, 0, 0))
                return
        elif meta["type"] == "int":
            try:
                val_int = int(val)
                if not (meta["min"] <= val_int <= meta["max"]):
                    dpg.set_value("output", f"[ERROR] {key} hors bornes ({meta['min']}–{meta['max']})")
                    dpg.configure_item("output", color = (200, 0, 0))
                    return
            except ValueError:
                dpg.set_value("output", f"[ERROR] {key} doit être un entier")
                dpg.configure_item("output", color = (200, 0, 0))
                return

        lines = update_value(lines, section, key, f"\"{val}\"")

    out_name = dpg.get_value("out_filename") or "Profiles_custom.ini"
    out_path = Path(out_name)
    save_profiles(lines, out_path)
    dpg.set_value("output", f"[SUCCESS] Profil {label} sauvegardé dans {out_path.resolve()}")
    dpg.configure_item("output", color=(0, 200, 0))

# ---------------------
# GUI
# ---------------------
dpg.create_context()
dpg.create_viewport(title = "TeensyRecorders Profiles Editor (v0.1)", width = 670, height = 900)

with dpg.font_registry():
    dpg.add_font(FONT_PATH, 14, tag = "emoji_font")
dpg.bind_font("emoji_font")

# Charger l'image
with dpg.texture_registry():
    image = Image.open(IMG_PATH).convert("RGBA")
    width, height = image.size
    data = [c/255 for c in image.tobytes()]
    dpg.add_static_texture(width, height, data, tag = "logo_texture")

with dpg.window(tag = "PrimaryWindow", width = 700, height = 800,
                no_title_bar = True, no_collapse = True, no_move = True):

    # Entête
    with dpg.group(horizontal = True):
        if dpg.does_item_exist("logo_texture"):
            dpg.add_image("logo_texture")
        with dpg.group():
            dpg.add_text("TeensyRecorders Profiles Editor (v0.1)", color = (0, 150, 250))
            dpg.add_text("Outil pour éditer et sauvegarder facilement vos fichiers Profiles.ini.\n"
                         "Compatible avec les profils 2 à 5, avec validation automatique des valeurs.")
            dpg.add_text("Lien vers le projet : https://framagit.org/PiBatRecorderPojects/TeensyRecorders")

    dpg.add_spacer(height = 10)
    dpg.add_separator()

    # --- Sélecteur de profil ---
    dpg.add_text("Sélectionne un profil à modifier")
    dpg.add_radio_button(tuple(PROFILE_LABELS.keys()), default_value = "Profile 2",
                         tag = "profile_selector", callback=show_profile, horizontal = True)

    # --- Zone formulaire ---
    with dpg.child_window(tag = "form_area", width = -1, height = 620):
        pass

    # --- Boutons sauvegarde ---
    with dpg.group(horizontal = True):
        dpg.add_text("Nom de fichier de sortie :")
        dpg.add_input_text(default_value = "Profiles_custom.ini", tag = "out_filename", width = 300)
    dpg.add_button(label = "Sauvegarder ce profil", callback = save_callback)
    dpg.add_text("", tag = "output")

# Init
dpg.set_primary_window("PrimaryWindow", True)
dpg.set_value("profile_selector", "Profile 2")
show_profile(None, None, None)

dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
