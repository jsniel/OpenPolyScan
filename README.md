# OpenPolyScan

OpenPolyScan est un prototype open source de reconnaissance de plastiques à bas coût,
conçu pour des usages en fablabs, ateliers, médiation, recherche-action et expérimentation locale.

Le projet repose sur :
- un capteur multispectral **AS7265x**
- une carte **ESP32** pour l’acquisition et l’export des mesures
- un jeu de données spectral
- des scripts Python de classification par apprentissage automatique

---

## Origine du projet

OpenPolyScan a été initié au sein de **L’Atelier Autonome** dans le cadre d’un projet de
recyclage local du plastique inspiré de Precious Plastic, soutenu par l’ADEME dans l’appel
à projets « Low-tech en territoire normand ».

Il est publié en open source afin d’en assurer la continuité et la diffusion.
Le projet est désormais maintenu par **Jean-Sébastien Niel**.

L’objectif était de développer un appareil simple et accessible d’identification des plastiques
pour des structures comme les fablabs et ateliers citoyens.

---

## Objectifs

- rendre visible et compréhensible l’analyse spectrale des plastiques  
- proposer une base reproductible à faible coût  
- documenter un prototype technique ouvert  
- ouvrir la voie à une base de données collaborative de signatures spectrales  
- permettre à d’autres ateliers, chercheurs ou structures pédagogiques d’améliorer le projet  

---

## Contenu du dépôt

- `firmware/` : code ESP32 pour l’acquisition et l’export CSV  
- `scripts/` : scripts Python d’entraînement et d’évaluation  
- `data/` : jeux de données spectrales d’exemple  
- `hardware/` : fichiers CAO et STL du support / boîtier  
- `docs/` : documentation technique et méthodologique  
- `models/` : emplacement pour les modèles entraînés  
- `examples/` : exemples d’utilisation  

---

## État du projet

OpenPolyScan est un **prototype expérimental**.

Le système permet :
- d’acquérir des mesures spectrales  
- de constituer un jeu de données  
- d’entraîner des modèles de classification  

⚠️ Ce projet **n’est pas un outil industriel**.  
Les performances dépendent fortement :
- du protocole de mesure  
- de la taille du dataset  
- de la diversité des plastiques  
- des conditions d’acquisition  

---

## Matériel principal

- capteur SparkFun Triad / AS7265x  
- carte ESP32  
- support mécanique imprimé en 3D  

---

## Données actuelles

Le dépôt contient un premier jeu de données avec :
- PLA  
- PP  
- HDPE  

Ce dataset est fourni comme base d’expérimentation.

---

## 🚀 Prise en main rapide

### 1. Installation

#### Linux / macOS
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r scripts/requirements.txt
```

#### Windows PowerShell
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r scripts\requirements.txt
```

### 2. Entraîner un modèle

```bash
python scripts/train_plastic_model.py --file data/raw/dataset.csv
```

### 3. Tester différents modèles

```bash
python scripts/classif_spectre.py --file data/raw/dataset.csv
```

---

## Référence scientifique

Ce projet s’inspire notamment de :

Martinez-Hernandez, U.; West, G.; Assaf, T.  
*Low-Cost Recognition of Plastic Waste Using Deep Learning and a Multi-Spectral Near-Infrared Sensor.*  
Sensors 2024, 24, 2821.  
DOI: 10.3390/s24092821  

---

## Licences

Ce dépôt utilise plusieurs licences selon la nature des contenus :

- **Code source** (`firmware/`, `scripts/`) → AGPL-3.0-or-later  
- **Hardware** (`hardware/`) → CERN-OHL-S-2.0  
- **Documentation** → CC BY-SA 4.0  
- **Données** → CC BY-SA 4.0 (sauf mention contraire)  

Voir `LICENSE.md` pour plus de détails.

---

## Auteurs

Voir `AUTHORS.md`.

---

## Contribuer

Les contributions sont bienvenues :

- amélioration du firmware  
- enrichissement du dataset  
- amélioration des modèles  
- ajout de nouveaux plastiques  
- amélioration de la documentation  

---

## Vision

OpenPolyScan vise à devenir une **base ouverte et collaborative**
pour l’analyse spectrale des plastiques à faible coût.

Toute contribution permettant d’améliorer :
- la qualité des données  
- la reproductibilité  
- la compréhension des résultats  

est encouragée.

---

## Dépôt

Projet maintenu sur GitHub :
https://github.com/jsniel/openpolyscan
