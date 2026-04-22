# Exemples de commandes

### 1. Installation

### Linux / macOS
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r scripts/requirements.txt
```

### Windows PowerShell
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r scripts\requirements.txt
```

### 2. Entraîner un modèle

```bash
python scripts/classif_spectre.py --file data/raw/dataset.csv
```

### 3. Tester différents modèles

```bash
python scripts/classif_spectre.py --file data/raw/dataset.csv
```
