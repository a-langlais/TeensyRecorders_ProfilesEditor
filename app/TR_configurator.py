import dearpygui.dearpygui as dpg
from pathlib import Path
import re

INI_PATH = Path("initial_profile/Profiles.ini")

# ---------------------
# Utilitaires INI
# ---------------------
def load_profiles(path):
    with open(path, encoding="utf-8") as f:
        return f.readlines()

def get_value(lines, section, key, default=""):
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
    with open(path, "w", encoding="utf-8") as f:
        f.writelines(lines)

# ---------------------
# Chargement initial
# ---------------------
lines = load_profiles(INI_PATH)

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
    "MaxFileLength": {"type": "int", "min": 1, "max": 999, "default": "60"},
    "MinFreqUS": {"type": "int", "min": 10000, "max": 120000},
    "MaxFreqUS": {"type": "int", "min": 20000, "max": 120000},
    "MinLevel": {"type": "int", "min": 0, "max": 100, "default": "15"},
    "PreTrigger": {"type": "int", "min": 0, "max": 10, "default": "5"},
    "THSensorEnable": {"type": "combo", "choices": ["0","1"], "default": "1"},
    "GPSenable": {"type": "combo", "choices": ["0","1"], "default": "0"},
}

# ---------------------
# Cache mémoire
# ---------------------
profile_cache = {pid: {} for pid in PROFILE_LABELS.values()}

def cache_update(sender, app_data, user_data):
    """Met à jour le cache quand un champ est modifié"""
    profile_id, key = user_data
    profile_cache[profile_id][key] = app_data

# ---------------------
# Validation
# ---------------------
def validate_name_live(sender, app_data, user_data):
    text = app_data
    field_type = user_data.split("_")[-1]
    warn_tag = f"{user_data}_warn"
    limit = 11 if field_type == "ProfileName" else 5
    if re.search(r"[^A-Za-z0-9 _-]", text):
        dpg.set_value(warn_tag, "[WARNING] Seuls A–Z, 0–9, espace, - et _ sont autorisés")
        dpg.configure_item(warn_tag, show=True)
    elif len(text) > limit:
        dpg.set_value(warn_tag, f"[WARNING] Limité à {limit} caractères max")
        dpg.configure_item(warn_tag, show=True)
    else:
        dpg.configure_item(warn_tag, show=False)

def validate_final(name: str, limit: int) -> str:
    name = re.sub(r"[^A-Za-z0-9 _-]", "", name)
    return name[:limit]

def validate_int_live(sender, app_data, user_data):
    field, min_val, max_val = user_data
    warn_tag = f"{field}_warn"
    try:
        val = int(app_data)
        if val < min_val or val > max_val:
            dpg.set_value(warn_tag, f"[WARNING] Doit être entre {min_val} et {max_val}")
            dpg.configure_item(warn_tag, show=True)
        else:
            dpg.configure_item(warn_tag, show=False)
    except ValueError:
        if app_data.strip() != "":
            dpg.set_value(warn_tag, "[WARNING] Doit être un entier")
            dpg.configure_item(warn_tag, show=True)
        else:
            dpg.configure_item(warn_tag, show=False)

# ---------------------
# Callbacks
# ---------------------
def show_profile(sender, app_data, user_data):
    """Affiche un profil en rechargeant depuis le cache s'il existe"""
    label = dpg.get_value("profile_selector")
    profile_id = PROFILE_LABELS[label]
    section = f"Profile_{profile_id}"

    dpg.delete_item("form_area", children_only=True)

    for key, meta in FIELDS.items():
        # Prendre d'abord depuis le cache, sinon depuis le fichier ini
        val = profile_cache[profile_id].get(
            key,
            get_value(lines, section, key, default=meta.get("default","")).strip('"')
        )

        with dpg.group(horizontal=True, parent="form_area"):
            dpg.add_text(f"{key:15}")
            if meta["type"] == "text":
                if key in ["ProfileName", "WavPrefix"]:
                    dpg.add_input_text(default_value=val, tag=f"{section}_{key}", width=200,
                                       callback=lambda s,a,u=(profile_id,key): (validate_name_live(s,a,f"{section}_{key}"), cache_update(s,a,u)),
                                       user_data=f"{section}_{key}")
                    dpg.add_text("", tag=f"{section}_{key}_warn", color=(255,0,0), show=False)
                else:
                    dpg.add_input_text(default_value=val, tag=f"{section}_{key}", width=200,
                                       callback=cache_update, user_data=(profile_id,key))
            elif meta["type"] == "combo":
                choices = meta["choices"].copy()
                if val not in choices:
                    choices.append(val)
                dpg.add_combo(choices, default_value=val or meta.get("default","0"),
                              tag=f"{section}_{key}", width=200,
                              callback=cache_update, user_data=(profile_id,key))
            elif meta["type"] == "int":
                dpg.add_input_text(default_value=val, tag=f"{section}_{key}", width=100,
                                   callback=lambda s,a,u=(profile_id,key,meta): (validate_int_live(s,a,(f"{section}_{key}", meta["min"], meta["max"])), cache_update(s,a,(profile_id,key))),
                                   user_data=(f"{section}_{key}", meta["min"], meta["max"]))
                dpg.add_text("", tag=f"{section}_{key}_warn", color=(255,0,0), show=False)

def save_callback():
    global lines
    label = dpg.get_value("profile_selector")
    profile_id = PROFILE_LABELS[label]
    section = f"Profile_{profile_id}"

    # Sauvegarder les valeurs du cache dans le fichier ini
    for key, meta in FIELDS.items():
        val = profile_cache[profile_id].get(key, dpg.get_value(f"{section}_{key}"))

        if key == "ProfileName":
            val = validate_final(val, 11)
            if not val:
                dpg.set_value("output", "[ERROR] ProfileName invalide")
                dpg.configure_item("output", color=(200,0,0))  # rouge
                return
        elif key == "WavPrefix":
            val = validate_final(val, 5)
            if not val:
                dpg.set_value("output", "[ERROR] WavPrefix invalide")
                dpg.configure_item("output", color=(200,0,0))  # rouge
                return
        elif meta["type"] == "int":
            try:
                val_int = int(val)
                if not (meta["min"] <= val_int <= meta["max"]):
                    dpg.set_value("output", f"[ERROR] {key} hors bornes ({meta['min']}–{meta['max']})")
                    dpg.configure_item("output", color=(200,0,0))  # rouge
                    return
            except ValueError:
                dpg.set_value("output", f"[ERROR] {key} doit être un entier")
                dpg.configure_item("output", color=(200,0,0))  # rouge
                return

        # mettre à jour le fichier ini
        lines = update_value(lines, section, key, f"\"{val}\"")

    out_name = dpg.get_value("out_filename") or "Profiles_custom.ini"
    out_path = Path(out_name)
    save_profiles(lines, out_path)
    dpg.set_value("output", f"[SUCCESS] Profil {label} sauvegardé dans {out_path.resolve()}")
    dpg.configure_item("output", color=(0,200,0))  # vert

# ---------------------
# GUI
# ---------------------
dpg.create_context()
dpg.create_viewport(title="TeensyRecorders Configurator", width=670, height=800)

with dpg.font_registry():
    dpg.add_font("fonts/DejaVuSans.ttf", 14, tag="emoji_font")
dpg.bind_font("emoji_font")

with dpg.window(tag="PrimaryWindow", width=700, height=760, no_title_bar=True, no_collapse=True, no_move=True):
    # --- Titre + présentation ---
    dpg.add_text("Teensy Profiles Configurator", color=(0,150,250))
    dpg.add_text("Outil pour éditer et sauvegarder facilement vos fichiers Profiles.ini.\n"
                 "Compatible avec les profils 2 à 5, avec validation automatique des valeurs.")
    dpg.add_text("Lien vers le projet : https://framagit.org/PiBatRecorderPojects/TeensyRecorders")
    dpg.add_spacer(height=10)
    dpg.add_separator()

    # --- Sélecteur de profil ---
    dpg.add_text("Sélectionne un profil à modifier")
    dpg.add_radio_button(tuple(PROFILE_LABELS.keys()), default_value="Profile 2",
                         tag="profile_selector", callback=show_profile, horizontal=True)

    # --- Zone formulaire ---
    with dpg.child_window(tag="form_area", width=-1, height=520):
        pass

    # --- Boutons sauvegarde ---
    with dpg.group(horizontal=True):
        dpg.add_text("Nom de fichier de sortie :")
        dpg.add_input_text(default_value="Profiles_custom.ini", tag="out_filename", width=300)
    dpg.add_button(label="Sauvegarder ce profil", callback=save_callback)
    dpg.add_text("", tag="output")

# Init avec Profile 2
dpg.set_primary_window("PrimaryWindow", True)
dpg.set_value("profile_selector", "Profile 2")
show_profile(None, None, None)

dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
