// Copyright (c) 2024-2026 Atelier Autonome & Jean-Sébastien Niel
// SPDX-License-Identifier: AGPL-3.0-or-later

#include "SparkFun_AS7265X.h"
#include "SPIFFS.h"
#include <WiFi.h>
#include <WebServer.h>

AS7265X sensor;
WebServer server(80);

const char *ssid = "OpenPolyScan";
const char *password = "atelierautonome";

String fileName = "/default.csv";
String lastLabel = "";  
bool acquisitionRequested = false;  

void writeToCSV(String label, float values[]) {
  File file = SPIFFS.open(fileName, FILE_APPEND);
  if (!file) {
    Serial.println("Erreur d'ouverture du fichier CSV !");
    return;
  }

  for (int i = 0; i < 18; i++) {
    file.print(values[i]);
    file.print(",");
  }
  file.println(label);  
  file.close();
  Serial.println("Données enregistrées !");
}

void takeMeasurement() {
  Serial.println("Acquisition en cours...");
  sensor.takeMeasurements();  

  float values[18] = {
    sensor.getCalibratedA(), sensor.getCalibratedB(), sensor.getCalibratedC(),
    sensor.getCalibratedD(), sensor.getCalibratedE(), sensor.getCalibratedF(),
    sensor.getCalibratedG(), sensor.getCalibratedH(), sensor.getCalibratedR(),
    sensor.getCalibratedI(), sensor.getCalibratedS(), sensor.getCalibratedJ(),
    sensor.getCalibratedT(), sensor.getCalibratedU(), sensor.getCalibratedV(),
    sensor.getCalibratedW(), sensor.getCalibratedK(), sensor.getCalibratedL()
  };

  writeToCSV(lastLabel, values);
  Serial.println("Acquisition terminée !");
}

void handleDownload() {
  Serial.println("Requête de téléchargement reçue !");
  
  File file = SPIFFS.open(fileName, FILE_READ);
  if (!file) {
    server.send(404, "text/plain", "Fichier non trouvé");
    return;
  }

  Serial.println("Envoi du fichier CSV...");
  server.sendHeader("Content-Type", "text/csv");
  server.sendHeader("Content-Disposition", "attachment; filename=" + fileName);
  server.sendHeader("Connection", "close");
  server.streamFile(file, "text/csv");
  
  file.close();
  Serial.println("Fichier envoyé !");
}

void handleRoot() {
  String html = "<html><head><title>ESP32 Spectral Scanner</title>";
  html += "<style>";
  html += "body { font-family: Arial, sans-serif; text-align: center; background-color: #f4f4f4; }";
  html += "h2 { color: #333; }";
  html += "a, input[type=submit] { display: inline-block; padding: 10px 20px; margin: 10px; text-decoration: none; color: white; background: #007BFF; border-radius: 5px; border: none; }";
  html += "a:hover, input[type=submit]:hover { background: #0056b3; }";
  html += "form { margin-top: 20px; }";
  html += "input[type=text] { padding: 8px; width: 200px; margin-right: 10px; }";
  html += "</style></head><body>";
  html += "<h2>ESP32 Spectral Scanner</h2>";

  html += "<form action='/setfile' method='GET'>";
  html += "<input type='text' name='filename' placeholder='Nom du fichier CSV'>";
  html += "<input type='submit' value='Définir'>";
  html += "</form>";

  html += "<a href='/download'>Télécharger le fichier CSV</a>";

  html += "<form action='/acquire' method='GET'>";
  html += "<input type='text' name='label' placeholder='Entrez un label'>";
  html += "<input type='submit' value='Lancer Acquisition'>";
  html += "</form></body></html>";

  server.send(200, "text/html", html);
}

void handleSetFile() {
  if (server.hasArg("filename")) {
    fileName = "/" + server.arg("filename") + ".csv";
    Serial.println("Fichier CSV défini via Web : " + fileName);

    File file = SPIFFS.open(fileName, FILE_WRITE);
    if (!file) {
      Serial.println("Erreur création fichier !");
    } else {
      file.println("410nm,435nm,460nm,485nm,510nm,535nm,560nm,585nm,610nm,645nm,680nm,705nm,730nm,760nm,810nm,860nm,900nm,940nm,Label");
      file.close();
      Serial.println("Fichier CSV initialisé !");
    }

    server.send(200, "text/plain", "Fichier défini : " + fileName);
  } else {
    server.send(400, "text/plain", "Nom de fichier non fourni !");
  }
}

void handleAcquire() {
  if (server.hasArg("label")) {
    lastLabel = server.arg("label");
    acquisitionRequested = true;  
    Serial.println("Acquisition demandée pour : " + lastLabel);
    server.send(200, "text/plain", "Acquisition en cours...");
  } else {
    server.send(400, "text/plain", "Label non fourni !");
  }
}

void setup() {
  Serial.begin(115200);
  Serial.println("Démarrage...");

  if (!SPIFFS.begin(true)) {
    Serial.println("Erreur SPIFFS !");
    return;
  }

  if (sensor.begin() == false) {
    Serial.println("Capteur non détecté !");
    while (1);
  }

  WiFi.softAP(ssid, password);
  Serial.print("AP démarré : ");
  Serial.println(ssid);
  Serial.println("Accédez à http://192.168.4.1/");

  server.on("/", handleRoot);
  server.on("/download", handleDownload);
  server.on("/setfile", handleSetFile);
  server.on("/acquire", handleAcquire);
  server.begin();
  Serial.println("Serveur Web actif !");

  Serial.println("Entrez le nom du fichier CSV à créer (optionnel) :");
}

void loop() {
  server.handleClient();  

  if (Serial.available()) {
    String input = Serial.readStringUntil('\n');
    input.trim();

    if (fileName == "/default.csv") {  
      fileName = "/" + input + ".csv";
      Serial.println("Fichier CSV défini via Série : " + fileName);

      File file = SPIFFS.open(fileName, FILE_WRITE);
      if (!file) {
        Serial.println("Erreur création fichier !");
      } else {
        file.println("410nm,435nm,460nm,485nm,510nm,535nm,560nm,585nm,610nm,645nm,680nm,705nm,730nm,760nm,810nm,860nm,900nm,940nm,Label");
        file.close();
        Serial.println("Fichier CSV initialisé !");
      }
    } else {  
      lastLabel = input;
      Serial.println("Acquisition demandée via Série pour : " + lastLabel);
      acquisitionRequested = true;
    }
  }

  if (acquisitionRequested) {
    acquisitionRequested = false;  
    takeMeasurement();
  }
}
