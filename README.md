<p align="center">
  <img src="img/logo_PR.png" alt="Logo" width="100"/>
</p>

<h1 align="center">TeensyRecorders Profiles Editor</h1>
<p align="center">
  <a href="https://www.python.org/">
    <img src="https://img.shields.io/badge/Python-3.9+-blue?logo=python&logoColor=white" alt="Python">
  </a>
  <a href="https://pyinstaller.org/">
    <img src="https://img.shields.io/badge/Build-PyInstaller-green" alt="PyInstaller">
  </a>
  <a href="https://github.com/a-langlais/TeensyRecorders_ProfilesEditor/blob/main/LICENSE">
    <img src="https://img.shields.io/badge/License-MIT-lightgrey" alt="License">
  </a>
  <a href="https://github.com/a-langlais/TeensyRecorders_ProfilesEditor/releases">
    <img src="https://img.shields.io/badge/Release-v0.1-orange" alt="Release">
  </a>
</p>

Un petit utilitaire graphique en **Python + DearPyGui** pour éditer et sauvegarder facilement les fichiers `Profiles.ini` utilisés par les enregistreurs [TeensyRecorders](https://framagit.org/PiBatRecorderPojects/TeensyRecorders).
Le dernier executable Windows (`.exe`) est disponible [dans le dossier `dist` du repo](https://github.com/a-langlais/TeensyRecorders_ProfilesEditor/tree/main/dist)

Par défaut, les TeensyRecorders utilise un fichier `Profiles.ini` composé de 5 profils, dont le premier n'est pas éditable par mesure de sécurité.
Le projet est pensé pour fonctionner aussi bien en **mode script** qu’en **standalone compilé**, et est compatible avec `PyInstaller` et `Nuitka`.

<p align="center">
    <img src="img/screenshot.png" alt="Interface du programme" width="90%" />
</p>

## ✨ Fonctionnalités

- ⚙️ Édition des **profils 2 à 5** (le profil 1 reste réservé au firmware)
- 🛡️ Validation en direct des champs :
  - `ProfileName` → ≤ 11 caractères, alphanumérique, `_` et `-` autorisés
  - `WavPrefix` → ≤ 5 caractères
  - `MaxFileLength` → 1–999 minutes (par défaut 60)
  - `MinFreqUS` / `MaxFreqUS` → cohérence des bornes
  - `MinLevel` → 0–100 dB (par défaut 15)
  - `PreTrigger` → 0–10
  - `THSensorEnable` et `GPSenable` → 0 ou 1
- 💾 Sauvegarde dans un nouveau fichier `.ini` directement chargeable sur le TeensyRecorders
- 🎨 Messages de validation colorés :
  - ✅ `[SUCCESS]` en vert
  - ⚠️ `[WARNING]` en orange
  - ❌ `[ERROR]` en rouge

## 📂 Organisation du projet

```bash
TeensyRecorders_ProfilesEditor/
├── app/                   
│   └── TR_configurator.py # Application principale (DearPyGui)
├── dist/                  # Dernière distribution
├── compiler/              # Script de build
├── fonts/                 # Polices utilisées
├── img/                   # Ressources graphiques
├── initial_profile/       # Fichiers de configuration par défaut
│
├── .gitignore            
└── README.md              
```

## 📦 Installation

### ⚡ Application standalone

Lancer directement l'application compilée (Windows, `*.exe`), disponible dans le dossier `dist/`.
Dernière version : 0.1 (2025-09)

✨ Fonctionnalités :
✅ Interface graphique avec DearPyGui
✅ Sélection et édition des profils 2 à 5
✅ Validation automatique des champs (tailles, formats, bornes min/max)
✅ Sauvegarde dans un fichier `.ini` prêt à être chargé sur un TeensyRecorders
✅ Support des chemins relatifs et compilation standalone

### 🛠️ Mode développement

Cloner le projet :

```bash
git clone https://github.com/a-langlais/TeensyRecorders_ProfilesEditor.git
cd TeensyRecorders_ProfilesEditor
```

Utiliser le `requirements.txt`pour installer les dépendances de développement :

```bash
pip install -r requirements.txt
```

Et lancer en mode développement :

```bash
python app/TR_configurator.py
```

Compiler directement l'application en `*.exe` avec :

```bash
python compiler/compiler.py
```

## 📜 Licence

Projet distribué sous licence MIT.
