import sys, re
from pathlib import Path
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QComboBox, QPushButton, QFileDialog, QMessageBox, QFormLayout, QTabWidget
)
from PySide6.QtGui import QPixmap, QFont, QIntValidator
from PySide6.QtCore import Qt

# ----------------------
# Utilitaires INI
# ----------------------
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

def save_profiles(lines, path):
    with open(path, "w", encoding="utf-8") as f:
        f.writelines(lines)

# ----------------------
# Configuration
# ----------------------
FIELDS = {
    "ProfileName": {"type": "text", "limit": 11},
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
    "WavPrefix": {"type": "text", "limit": 5},
    "MaxFileLength": {"type": "int", "min": 1, "max": 999, "default": 60},
    "MinFreqUS": {"type": "int", "min": 10000, "max": 120000},
    "MaxFreqUS": {"type": "int", "min": 20000, "max": 120000},
    "MinLevel": {"type": "int", "min": 0, "max": 100, "default": 15},
    "PreTrigger": {"type": "int", "min": 0, "max": 10, "default": 5},
    "THSensorEnable": {"type": "combo", "choices": ["0","1"], "default": "1"},
    "GPSenable": {"type": "combo", "choices": ["0","1"], "default": "0"},
}

SECTION_TITLES = {
    "Profil": ["ProfileName", "OpMode"],
    "Horaires": ["StartTime", "EndTime"],
    "Audio": ["SampFreqU", "NumericGain", "StereoMode", "MicrophoneType"],
    "Fichiers": ["LEDSynchro", "WavPrefix", "MaxFileLength"],
    "Fréquences": ["MinFreqUS", "MaxFreqUS", "MinLevel", "PreTrigger"],
    "Capteurs": ["THSensorEnable", "GPSenable"]
}

PROFILE_LABELS = {"Profile 2": "2", "Profile 3": "3", "Profile 4": "4", "Profile 5": "5"}

# ----------------------
# Interface principale
# ----------------------
class ProfileEditor(QWidget):
    def __init__(self, ini_path, logo_path="img/logo_PR.png"):
        super().__init__()
        self.setWindowTitle("TeensyRecorders Profiles Editor (PySide6)")
        self.setFixedWidth(500)
        self.setFixedHeight(400)

        self.ini_path = Path(ini_path)
        self.lines = load_profiles(self.ini_path)
        self.profile_id = "2"
        self.inputs = {}
        self.out_dir = Path(".")
        self.out_name = "Profiles_custom.ini"

        # Cache mémoire : un dict par profil
        self.cache = {pid: {} for pid in PROFILE_LABELS.values()}

        layout = QVBoxLayout()

        # --- Entête (1/3 – 2/3) ---
        header_layout = QHBoxLayout()
        logo_label = QLabel()
        pixmap = QPixmap(str(logo_path))
        if not pixmap.isNull():
            logo_label.setPixmap(pixmap.scaledToHeight(80, Qt.SmoothTransformation))
            logo_label.setAlignment(Qt.AlignCenter)

        text_layout = QVBoxLayout()
        title = QLabel("TeensyRecorders Profiles Editor (v0.2)")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        desc = QLabel(
            "Outil pour éditer et sauvegarder facilement vos fichiers Profiles.ini.\n"
            "Compatible avec les profils 2 à 5, avec validation automatique des valeurs."
        )
        desc.setWordWrap(True)
        text_layout.addWidget(title)
        text_layout.addWidget(desc)

        header_layout.addWidget(logo_label, stretch=1)   # 1/3
        header_layout.addLayout(text_layout, stretch=4)  # 2/3
        layout.addLayout(header_layout)

        # Sélecteur de profil
        profile_layout = QHBoxLayout()
        profile_layout.addWidget(QLabel("Sélection du profil :"))
        self.profile_combo = QComboBox()
        self.profile_combo.addItems(PROFILE_LABELS.keys())
        self.profile_combo.currentTextChanged.connect(self.change_profile)
        profile_layout.addWidget(self.profile_combo)
        layout.addLayout(profile_layout)

        # Onglets par section
        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)

        # Construit le formulaire pour le profil courant
        self.build_form()

        # Sélection dossier sortie + preview
        dir_layout = QHBoxLayout()
        browse_btn = QPushButton("Choisir dossier sortie")
        browse_btn.clicked.connect(self.select_output_dir)
        dir_layout.addWidget(browse_btn)

        self.out_dir_label = QLabel(str(self.out_dir.resolve()))
        self.out_dir_label.setStyleSheet("color: gray;")
        self.out_dir_label.setTextInteractionFlags(Qt.TextSelectableByMouse)  # permet de copier le chemin
        dir_layout.addWidget(self.out_dir_label, stretch=1)

        layout.addLayout(dir_layout)

        # Bouton sauvegarde en dessous
        save_layout = QHBoxLayout()

        save_btn = QPushButton("Sauvegarder")
        save_btn.clicked.connect(self.save_profile)
        save_layout.addWidget(save_btn)

        self.out_name_edit = QLineEdit(self.out_name)
        self.out_name_edit.setPlaceholderText("Nom du fichier de sortie (ex: Profiles_custom.ini)")
        save_layout.addWidget(self.out_name_edit, stretch=1)

        layout.addLayout(save_layout)

        self.setLayout(layout)

    # ----------------------
    # Helpers cache
    # ----------------------
    def ensure_profile_cache(self, pid: str):
        """Initialise le cache du profil depuis l'INI (une seule fois)."""
        if not self.cache.get(pid):
            self.cache[pid] = {}
        section = f"Profile_{pid}"
        for key, meta in FIELDS.items():
            if key not in self.cache[pid]:
                raw = get_value(self.lines, section, key, str(meta.get("default", "")))
                if meta["type"] == "int":
                    try:
                        vi = int(raw)
                    except ValueError:
                        vi = meta.get("default", meta["min"])
                    if not (meta["min"] <= vi <= meta["max"]):
                        vi = meta.get("default", meta["min"])
                    self.cache[pid][key] = str(vi)
                else:
                    self.cache[pid][key] = raw

    def sync_widgets_to_cache(self):
        """Pousse l'état des widgets courants dans le cache du profil courant."""
        pid = self.profile_id
        if pid not in self.cache:
            self.cache[pid] = {}
        for key, widget in self.inputs.items():
            if isinstance(widget, QLineEdit):
                self.cache[pid][key] = widget.text().strip()
            elif isinstance(widget, QComboBox):
                self.cache[pid][key] = widget.currentText()

    def update_cache(self, key, value):
        self.cache[self.profile_id][key] = str(value).strip()

    # ----------------------
    # Formulaire
    # ----------------------
    def build_form(self):
        """Construit les onglets sans toucher au cache existant."""
        self.ensure_profile_cache(self.profile_id)
        self.inputs.clear()
        self.tabs.clear()
        pid = self.profile_id

        for section_name, keys in SECTION_TITLES.items():
            group = QWidget()
            form_layout = QFormLayout()

            for key in keys:
                meta = FIELDS[key]
                val = self.cache[pid].get(key, "")

                if meta["type"] == "text":
                    widget = QLineEdit(val)
                    # Placeholder pour heures
                    if key in ["StartTime", "EndTime"]:
                        widget.setPlaceholderText("HH:MM")
                    widget.textChanged.connect(lambda v, k=key: self.update_cache(k, v))

                elif meta["type"] == "combo":
                    widget = QComboBox()
                    widget.addItems(meta["choices"])
                    if val in meta["choices"]:
                        widget.setCurrentText(val)
                    else:
                        # choix par défaut si valeur invalide
                        default_choice = meta.get("default")
                        if default_choice in meta["choices"]:
                            widget.setCurrentText(default_choice)
                            self.cache[pid][key] = default_choice
                        else:
                            widget.setCurrentIndex(0)
                            self.cache[pid][key] = widget.currentText()
                    widget.currentTextChanged.connect(lambda v, k=key: self.update_cache(k, v))

                elif meta["type"] == "int":
                    widget = QLineEdit(val)
                    widget.setValidator(QIntValidator(meta["min"], meta["max"]))
                    widget.setPlaceholderText(f"Entier {meta['min']}–{meta['max']}")
                    widget.textChanged.connect(lambda v, k=key: self.update_cache(k, v))

                self.inputs[key] = widget
                form_layout.addRow(QLabel(key), widget)

            group.setLayout(form_layout)
            self.tabs.addTab(group, section_name)

    def change_profile(self, label):
        # Sauvegarde l'état des widgets du profil courant dans le cache
        self.sync_widgets_to_cache()
        # Bascule de profil et reconstruit l'UI depuis le cache de ce profil
        self.profile_id = PROFILE_LABELS[label]
        self.build_form()

    # ----------------------
    # Sauvegarde
    # ----------------------
    def select_output_dir(self):
        dir_ = QFileDialog.getExistingDirectory(self, "Choisir un dossier")
        if dir_:
            self.out_dir = Path(dir_)
            self.out_dir_label.setText(str(self.out_dir.resolve()))

    def save_profile(self):
        # Toujours s'assurer que les dernières saisies sont poussées dans le cache
        self.sync_widgets_to_cache()

        section = f"Profile_{self.profile_id}"
        pid = self.profile_id

        for key, meta in FIELDS.items():
            val = self.cache[pid].get(key, "")

            # Validation texte
            if meta["type"] == "text":
                if key in ["ProfileName", "WavPrefix"]:
                    limit = meta.get("limit")
                    if limit and len(val) > limit:
                        QMessageBox.warning(self, "Erreur", f"{key} limité à {limit} caractères")
                        return
                    if re.search(r"[^A-Za-z0-9 _-]", val):
                        QMessageBox.warning(self, "Erreur", f"{key} contient des caractères interdits")
                        return
                elif key in ["StartTime", "EndTime"]:
                    if val and not re.match(r"^(?:[01]\d|2[0-3]):[0-5]\d$", val):
                        QMessageBox.warning(self, "Erreur", f"{key} doit être au format HH:MM (ex: 08:30)")
                        return

            # Validation int
            elif meta["type"] == "int":
                try:
                    val_int = int(val)
                except ValueError:
                    val_int = meta.get("default", meta["min"])
                if not (meta["min"] <= val_int <= meta["max"]):
                    QMessageBox.warning(self, "Erreur", f"{key} doit être entre {meta['min']} et {meta['max']}")
                    return
                val = str(val_int)

            # Mise à jour du buffer INI
            self.lines = update_value(self.lines, section, key, val)

        # Met à jour le nom de fichier depuis le champ
        self.out_name = self.out_name_edit.text().strip() or "Profiles_custom.ini"
        out_path = self.out_dir / self.out_name
        save_profiles(self.lines, out_path)
        QMessageBox.information(self, "Succès", f"Profil sauvegardé dans {out_path}")

# ----------------------
# Lancement
# ----------------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ProfileEditor("initial_profile/Profiles.ini", logo_path="img/logo_PR.png")
    window.resize(700, 600)
    window.show()
    sys.exit(app.exec())
