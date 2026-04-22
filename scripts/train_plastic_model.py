# Copyright (c) 2024-2026 Atelier Autonome & Jean-Sébastien Niel
# SPDX-License-Identifier: AGPL-3.0-or-later

"""
train_plastic_model.py

But :
  - charger un dataset spectral mesuré par capteur AS7265x
  - entraîner et comparer un RandomForest et un MLP
  - évaluer les performances par validation croisée et sur un split train/test
  - sauvegarder un modèle entraîné dans le dossier models/

Exécution :
  python scripts/train_plastic_model.py --file data/raw/24_11_2025_PLA_PP_HDPE.csv
"""

from pathlib import Path
import argparse

import joblib
import pandas as pd
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.metrics import classification_report, confusion_matrix


def load_dataset(path: Path) -> tuple[pd.DataFrame, pd.Series]:
    """Charge un CSV avec séparateur ';' et décimales ','."""
    df = pd.read_csv(path, sep=";")

    if df.empty:
        raise ValueError("Le fichier CSV est vide.")

    # Supprime les colonnes totalement vides, souvent dues à un ';' final
    df = df.dropna(axis=1, how="all")

    if df.shape[1] < 2:
        raise ValueError(
            "Le dataset doit contenir au moins une colonne de label et une colonne de données."
        )

    # Première colonne = label matière
    label_col = df.columns[0]
    y = df[label_col].astype(str).str.strip()

    # Colonnes suivantes = mesures spectrales
    X = df.drop(columns=[label_col])

    # Convertit "0,82" en 0.82
    X = X.apply(lambda c: c.astype(str).str.replace(",", ".", regex=False).astype(float))

    return X, y


def build_models() -> tuple[RandomForestClassifier, object]:
    """Construit les deux modèles utilisés."""
    rf = RandomForestClassifier(n_estimators=200, random_state=0)

    mlp = make_pipeline(
        StandardScaler(),
        MLPClassifier(
            hidden_layer_sizes=(32, 16),
            activation="relu",
            max_iter=2000,
            random_state=0,
        ),
    )

    return rf, mlp


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Entraînement d'un modèle de classification de plastiques mesurés avec un capteur AS7265x"
    )
    parser.add_argument(
        "--file",
        type=str,
        required=True,
        help="Chemin vers le fichier CSV de données spectrales",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="models/plastics_model.joblib",
        help="Chemin du fichier modèle de sortie (défaut : models/plastics_model.joblib)",
    )
    parser.add_argument(
        "--save-model",
        choices=["rf", "mlp"],
        default="rf",
        help="Modèle à sauvegarder : 'rf' ou 'mlp' (défaut : rf)",
    )

    args = parser.parse_args()

    csv_path = Path(args.file)
    if not csv_path.exists():
        raise FileNotFoundError(f"Fichier introuvable : {csv_path}")

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    print(f"📁 Dataset utilisé : {csv_path}")

    # Chargement des données
    X, y = load_dataset(csv_path)
    feature_names = X.columns.tolist()

    print(f"[i] Nombre d'échantillons : {len(X)}")
    print(f"[i] Nombre de bandes spectrales : {X.shape[1]}")
    print(f"[i] Classes présentes : {sorted(y.unique().tolist())}")

    # Validation croisée
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=0)

    rf_cv, mlp_cv = build_models()

    print("\n=== Validation croisée 5-fold (RandomForest) ===")
    scores_rf = cross_val_score(rf_cv, X, y, cv=cv)
    print("Scores RF par fold :", scores_rf)
    print("Moyenne RF :", scores_rf.mean(), "/ Ecart-type :", scores_rf.std())

    print("\n=== Validation croisée 5-fold (MLP) ===")
    scores_mlp = cross_val_score(mlp_cv, X, y, cv=cv)
    print("Scores MLP par fold :", scores_mlp)
    print("Moyenne MLP :", scores_mlp.mean(), "/ Ecart-type :", scores_mlp.std())

    # Split train/test
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        stratify=y,
        random_state=0,
    )

    rf, mlp = build_models()

    print("\n🔧 Entraînement du RandomForest (train/test)...")
    rf.fit(X_train, y_train)

    print("🔧 Entraînement du MLP (train/test)...")
    mlp.fit(X_train, y_train)

    # Évaluation RF
    print("\n=== Evaluation sur le jeu de test (RandomForest) ===")
    y_pred_rf = rf.predict(X_test)
    print(classification_report(y_test, y_pred_rf))
    print("Matrice de confusion (RF) :")
    print(confusion_matrix(y_test, y_pred_rf))

    # Évaluation MLP
    print("\n=== Evaluation sur le jeu de test (MLP) ===")
    y_pred_mlp = mlp.predict(X_test)
    print(classification_report(y_test, y_pred_mlp))
    print("Matrice de confusion (MLP) :")
    print(confusion_matrix(y_test, y_pred_mlp))

    # --- Construction du nom de base à partir du dataset ---
    dataset_name = csv_path.stem  # ex: 24_11_2025_PLA_PP_HDPE

    # --- Création du dossier models ---
    model_dir = Path("models")
    model_dir.mkdir(parents=True, exist_ok=True)

    # --- Sauvegarde RandomForest ---
    rf_path = model_dir / f"{dataset_name}_RF.joblib"

    model_rf = {
        "model": rf,
        "feature_names": feature_names,
        "classes": sorted(y.unique().tolist()),
        "model_type": "RandomForest",
        "source_dataset": str(csv_path),
    }

    joblib.dump(model_rf, rf_path)
    print(f"💾 RandomForest sauvegardé : {rf_path}")

    # --- Sauvegarde MLP ---
    mlp_path = model_dir / f"{dataset_name}_MLP.joblib"

    model_mlp = {
        "model": mlp,
        "feature_names": feature_names,
        "classes": sorted(y.unique().tolist()),
        "model_type": "MLP",
        "source_dataset": str(csv_path),
    }

    joblib.dump(model_mlp, mlp_path)
    print(f"💾 MLP sauvegardé : {mlp_path}")


if __name__ == "__main__":
    main()