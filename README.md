# Teensy Profiles Configurator

Un petit utilitaire graphique en **Python + DearPyGui** pour éditer et sauvegarder facilement les fichiers `Profiles.ini` utilisés par les enregistreurs [TeensyRecorders](https://framagit.org/PiBatRecorderPojects/TeensyRecorders).

## ✨ Fonctionnalités

- Chargement automatique du fichier `Profiles.ini`
- Modification des **profils 2 à 5** uniquement (le profil 1 reste réservé au firmware)
- Validation en direct des champs :
  - `ProfileName` (≤ 11 caractères, alphanumérique, `_` et `-` autorisés)
  - `WavPrefix` (≤ 5 caractères)
  - `MaxFileLength` (1–999 minutes, par défaut 60)
  - `MinFreqUS` / `MaxFreqUS` (plage de fréquences cohérente)
  - `MinLevel` (0–100 dB, par défaut 15)
  - `PreTrigger` (0–10)
  - `THSensorEnable` et `GPSenable` (0 ou 1)
- Conservation des modifications en mémoire quand on change de profil (avant sauvegarde)
- Sauvegarde dans un nouveau fichier `.ini`
- Interface simple avec thème clair

## 🖥️ Aperçu

- Sélecteur de profil (2 à 5)
- Champs de configuration avec menus déroulants ou saisie directe
- Messages de validation colorés :
  - ✅ `[SUCCESS]` en vert
  - ⚠️ `[WARNING]` en orange
  - ❌ `[ERROR]` en rouge

## 📂 Organisation du projet

```bash
. 
├── configurator.py        # Script principal
├── initial_profile/
│   └── Profiles.ini       # Fichier de configuration d'origine
├── fonts/
│   └── DejaVuSans.ttf     # Police pour l'affichage
├── picture.bmp            # Logo optionnel affiché en haut de l'application
└── README.md
```

## 📦 Installation

### Prérequis

- Python 3.9+
- [DearPyGui](https://github.com/hoffstadt/DearPyGui)
- Pillow (pour le support éventuel d’images/logo)

```bash
pip install dearpygui pillow
```

### Cloner le projet

```bash
git clone https://github.com/USERNAME/TeensyProfilesConfigurator.git
cd TeensyProfilesConfigurator
```

### Utilisation

Lancer l’application avec :

```bash
python configurator.py
```

L’application ouvrira Profiles.ini depuis le dossier initial_profile/. Ce fichier ne doit pas être modifié.

Vous pouvez alors :
* Modifier les paramètres
* Naviguer entre les profils sans perdre vos changements
* Sauvegarder le profil actif dans un nouveau fichier .ini