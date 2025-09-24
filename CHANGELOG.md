# 📜 Changelog - TeensyRecorders Profiles Editor

Toutes les modifications notables du projet sont documentées ici.

---

## [0.3] - 2025-09-25
### Ajouté
- Support des champs numériques décimaux (float) avec validation (min, max, step).
- Ajout d’un onglet Hétérodyne dédié avec tous les paramètres associés (HeterodyneMode, AutoRecHeter, RefreshGraphe, etc.).
- Nouveaux paramètres pris en charge dans config.py :
  - **Horaires** : `RecTime`, `WaitTime`
  - **Audio** : `SampFreqA`, `LowpassFilter`, `HighpassFilter`, `fHighpassFilter`, `Exp10`
  - **Fréquences** : `MinFreqA`, `MaxFreqA`, `MinDuration`, `MaxDuration`, `ThresholdType`, `RelativeThreshold`, `AbsoluteThreshold`, `NbDetect`
  - **Capteurs** : `TemperaturePeriod`, `ContMesTemp`, `SaveNoise`
  - **Hétérodyne** : tous les champs spécifiques (10 paramètres)
- Validation et affichage améliorés pour tous les champs nouvellement ajoutés.

### Changé
- Réorganisation de config.py :
  - Conservation des sections de base (Profil, Horaires, Audio, Fichiers, Fréquences, Capteurs).
  - Ajout d’une seule section supplémentaire : Hétérodyne.
- Amélioration de la gestion des placeholders (horaires, valeurs numériques).

## Corrigé
- Les onglets très chargés ne débordent plus de la fenêtre grâce au QScrollArea.
- Meilleure robustesse lors de la validation des floats et des bornes numériques.
- Correction d’un problème mineur où certains champs affichaient une valeur vide au lieu de la valeur par défaut.

---

## [0.2] - 2025-09-24
### Changé
- Migration complète de l'interface graphique **DearPyGui → PySide6 (Qt)**.
- Nouvelle organisation du projet :
  - `app/main.py` : point d’entrée
  - `app/ui_editor.py` : interface Qt
  - `app/ini_utils.py` : utilitaires INI
  - `app/config.py` : définitions des champs et sections
- Ajout d’un en-tête avec logo, titre, description et lien cliquable vers la documentation.
- Ajout d’un séparateur sous l’entête et d’un footer `(c) Alexandre LANGLAIS - 2025 - v0.2`.
- Largeur et hauteur de fenêtre désormais bornées (300–1000px).
- Nouveau système de cache pour conserver les modifications entre onglets/profils avant sauvegarde.
- Sélection du dossier de sortie + prévisualisation du chemin choisi.
- Possibilité de renommer le fichier de sortie `.ini` avant sauvegarde.

### Corrigé
- Problèmes d’imports relatifs lors de la compilation PyInstaller → passage aux imports absolus et ajout de `resource_path` pour gérer les ressources embarquées.
- Validation des champs `StartTime` et `EndTime` au format `HH:MM`.
- Sauvegarde plus robuste : respect des bornes min/max et valeurs par défaut cohérentes.

---

## [0.1] - 2025-07-01
### Ajouté
- Première version POC fonctionnelle avec **DearPyGui**.
- Édition et validation des profils 2 à 5.
- Sauvegarde dans un fichier `.ini` prêt à être chargé sur un TeensyRecorders.
- Compilation standalone Windows avec PyInstaller.
