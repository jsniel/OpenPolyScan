# Entraînement du modèle

## Pré-requis

- Python 3
- environnement virtuel recommandé
- dépendances listées dans `scripts/requirements.txt`

## Script principal

Le script `train_plastic_model.py` :
- charge un CSV
- effectue une validation croisée
- entraîne un RandomForest et un MLP
- affiche les rapports de classification
- sauvegarde un modèle au format `joblib`

## Script complémentaire

Le script `classif_spectre.py` :
- compare plusieurs classifieurs
- affiche une matrice de confusion
- propose une visualisation PCA

## Remarque importante

Les résultats obtenus dans OpenPolyScan sont directement liés :
- à la taille du jeu de données
- au choix des classes
- à la stabilité du protocole
- au nettoyage du dataset