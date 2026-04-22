# Copyright (c) 2024-2026 Atelier Autonome & Jean-Sébastien Niel
# SPDX-License-Identifier: AGPL-3.0-or-later

#!/usr/bin/env python3
"""
classif_spectre.py

But :
  - charger un dataset spectral mesuré par capteur AS7265x
  - entraîner plusieurs classifieurs (LogReg, KNN, RandomForest, SVM)
  - évaluer les performances sur un jeu de test
  - afficher et sauvegarder la matrice de confusion
  - afficher et sauvegarder une visualisation PCA

Exécution :
  python scripts/classif_spectre.py --file data/raw/24_11_2025_PLA_PP_HDPE.csv
"""

import argparse
from pathlib import Path

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.metrics import classification_report, ConfusionMatrixDisplay

from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC


# --------------------------
# 1. Lecture des arguments
# --------------------------
parser = argparse.ArgumentParser(
    description="Classification de spectres de plastiques mesurés avec un capteur AS7265x"
)
parser.add_argument(
    "--file",
    type=str,
    required=True,
    help="Chemin du fichier CSV contenant les données spectrales"
)
parser.add_argument(
    "--sep",
    type=str,
    default=";",
    help="Séparateur du fichier CSV (défaut: ';')"
)
parser.add_argument(
    "--decimal",
    type=str,
    default=",",
    help="Symbole décimal utilisé dans le fichier (défaut: ',')"
)
args = parser.parse_args()

data_path = Path(args.file)
if not data_path.exists():
    raise FileNotFoundError(f"Fichier introuvable : {data_path.resolve()}")

# Dossier de sortie pour les figures
output_dir = Path("models/figures")
output_dir.mkdir(parents=True, exist_ok=True)


# --------------------------
# 2. Chargement du dataset
# --------------------------
print(f"[i] Chargement du dataset : {data_path}")

df = pd.read_csv(data_path, sep=args.sep, decimal=args.decimal, engine="python")

# Supprime les colonnes vides accidentelles
df = df.dropna(axis=1, how="all")

# Vérifie que les colonnes numériques sont bien converties
for c in df.columns[1:]:
    df[c] = pd.to_numeric(df[c], errors="coerce")

print("[i] Aperçu des données :")
print(df.head(), "\n")

y = df.iloc[:, 0]    # labels matière
X = df.iloc[:, 1:]   # intensités spectrales

print(f"[i] Nombre d’échantillons : {len(df)}")
print(f"[i] Nombre de bandes spectrales : {X.shape[1]}\n")


# --------------------------
# 3. Prétraitement
# --------------------------
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Séparation train/test (80/20, stratifié)
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, stratify=y, random_state=42
)


# --------------------------
# 4. Définition des modèles
# --------------------------
models = {
    "LogReg": LogisticRegression(max_iter=2000),
    "KNN": KNeighborsClassifier(n_neighbors=3),
    "RandomForest": RandomForestClassifier(n_estimators=200, random_state=42),
    "SVM": SVC(kernel="rbf", C=10, gamma="scale")
}


# --------------------------
# 5. Entraînement et évaluation
# --------------------------
results = {}

for name, model in models.items():
    print(f"\n=== {name} ===")
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    report = classification_report(y_test, y_pred, output_dict=True)
    acc = report["accuracy"]
    print(classification_report(y_test, y_pred, digits=3))

    results[name] = acc


# --------------------------
# 6. Résumé des précisions
# --------------------------
print("\n=== RÉSUMÉ DES PRÉCISIONS ===")
for name, acc in results.items():
    print(f"{name:<15} {acc:.3f}")

best_model_name = max(results, key=results.get)
print(f"\n[i] Meilleur modèle : {best_model_name}")

best_model = models[best_model_name]


# --------------------------
# 7. Matrice de confusion
# --------------------------
fig_cm, ax_cm = plt.subplots(figsize=(10, 8))
ConfusionMatrixDisplay.from_estimator(
    best_model, X_test, y_test, cmap="viridis", xticks_rotation=90, ax=ax_cm
)
ax_cm.set_title(f"Matrice de confusion ({best_model_name})")
fig_cm.tight_layout()

cm_path = output_dir / f"confusion_matrix_{best_model_name}.png"
fig_cm.savefig(cm_path, dpi=300)
print(f"[i] Matrice de confusion sauvegardée : {cm_path}")

plt.show()


# --------------------------
# 8. Visualisation PCA (2D)
# --------------------------
pca = PCA(n_components=2)
proj = pca.fit_transform(X_scaled)

fig_pca, ax_pca = plt.subplots(figsize=(8, 6))
unique_labels = np.unique(y)

for label in unique_labels:
    mask = y == label
    ax_pca.scatter(proj[mask, 0], proj[mask, 1], label=label, s=50, alpha=0.7)

ax_pca.legend(bbox_to_anchor=(1.05, 1), loc="upper left")
ax_pca.set_title("Projection PCA des spectres plastiques")
ax_pca.set_xlabel("Composante principale 1")
ax_pca.set_ylabel("Composante principale 2")
fig_pca.tight_layout()

pca_path = output_dir / "pca_projection.png"
fig_pca.savefig(pca_path, dpi=300)
print(f"[i] Projection PCA sauvegardée : {pca_path}")

plt.show()