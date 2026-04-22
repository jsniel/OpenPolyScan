# OpenPolyScan — Firmware ESP32

Ce dossier contient le firmware utilisé pour l’acquisition des données spectrales
dans le projet OpenPolyScan.

Le firmware permet :
- de piloter un capteur multispectral **AS7265x (SparkFun Triad)**
- de mesurer des signatures spectrales
- d’exposer une interface web locale
- d’exporter les données au format CSV

---

## ⚙️ Matériel nécessaire

- ESP32 (type DevKit)
- Capteur **SparkFun Triad AS7265x**
- Connexion I2C (SDA / SCL)
- Alimentation USB

---

## 🔌 Connexions

| ESP32 | AS7265x |
|------|--------|
| 3.3V | VCC |
| GND  | GND |
| SDA  | SDA |
| SCL  | SCL |

⚠️ Vérifier que le capteur fonctionne en **3.3V**

---

## 🧠 Principe de fonctionnement

Le firmware :

1. Initialise le capteur AS7265x
2. Crée un point d’accès WiFi local (ESP32)
3. Lance un serveur web embarqué
4. Permet :
   - de déclencher des mesures
   - de visualiser les données
   - de télécharger un fichier CSV

---

## 📡 Connexion au système

1. Allumer l’ESP32
2. Se connecter au WiFi créé par l’ESP32

Exemple :
SSID : OpenPolyScan

3. Ouvrir un navigateur
4. Aller à l’adresse :

http://192.168.4.1

---

## 🌐 Interface Web

L’interface permet :

- de lancer des mesures
- de visualiser les valeurs spectrales
- de générer un fichier CSV
- de télécharger les données

---

## 📊 Format des données

Les données sont exportées sous forme de CSV :

- première colonne : label (matière)
- colonnes suivantes : intensités spectrales

Exemple :

PLA;0,82;0,76;0,65;...
PP;0,45;0,50;0,60;...

---

## ▶️ Installation du firmware

### 1. Installer Arduino IDE

https://www.arduino.cc/en/software

---

### 2. Ajouter le support ESP32

Dans Arduino IDE :

- Fichier → Préférences
- Ajouter dans “URL de gestionnaire de cartes” :

https://dl.espressif.com/dl/package_esp32_index.json

Puis :

- Outils → Type de carte → Gestionnaire de cartes
- Installer **ESP32**

---

### 3. Installer les bibliothèques nécessaires

Dans le gestionnaire de bibliothèques :

- SparkFun AS7265x
- WiFi
- WebServer (inclus avec ESP32)

---

### 4. Charger le firmware

1. Ouvrir :
ESP32LocalCSVWebGenerator.ino

2. Sélectionner la carte ESP32
3. Sélectionner le port série
4. Cliquer sur Upload

---

## 🔧 Configuration (optionnelle)

Dans le code, tu peux modifier :

- le nom du réseau WiFi
- les paramètres d’acquisition
- le format CSV

---

## 🧪 Acquisition de données

### Étapes recommandées

1. Préparer un échantillon de plastique
2. Placer le capteur à distance constante
3. Limiter la lumière ambiante
4. Lancer plusieurs mesures
5. Télécharger le CSV
6. Ajouter le label (PLA, PP, etc.)

---

## ⚠️ Bonnes pratiques

- Toujours garder la même géométrie de mesure
- Nettoyer les échantillons
- Éviter les surfaces trop réfléchissantes
- Répéter les mesures

---

## 🐞 Dépannage

### Le WiFi n’apparaît pas
- Vérifier que l’ESP32 est alimenté
- Redémarrer la carte

### Impossible d’accéder à la page web
- Vérifier que tu es connecté au bon WiFi
- Utiliser l’adresse 192.168.4.1

### Pas de données du capteur
- Vérifier les connexions I2C
- Vérifier l’alimentation
- Tester avec un exemple SparkFun

---

## 📜 Licence

Le firmware est publié sous licence :

AGPL-3.0-or-later

Voir le fichier LICENSE.md à la racine du projet.

---

## 🤝 Contribution

Les contributions sont bienvenues :

- amélioration de l’interface web
- optimisation des mesures
- amélioration du format de données
- ajout de nouvelles fonctionnalités

---

## 🔬 Contexte

Ce firmware fait partie du projet OpenPolyScan,
un système open source d’identification de plastiques à bas coût.

Projet initié par L’Atelier Autonome  
Maintenu par Jean-Sébastien Niel
