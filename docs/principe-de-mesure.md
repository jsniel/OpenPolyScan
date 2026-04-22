# Principe de mesure

Le système repose sur l’idée que différents plastiques présentent des réponses différentes
lorsqu’ils sont éclairés.

Le capteur AS7265x mesure l’intensité lumineuse réfléchie sur 18 longueurs d’onde,
du visible au proche infrarouge.

Chaque échantillon produit ainsi une signature spectrale.
Ces mesures peuvent ensuite être utilisées comme variables d’entrée pour entraîner
un modèle de classification.

Dans OpenPolyScan, l’acquisition est réalisée via une carte ESP32, puis les données
sont exportées en CSV pour analyse.