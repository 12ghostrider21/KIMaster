
# KIMaster - Plattform zum Vergleich von Spiele-KIs

## Projektbeschreibung

KIMaster ist eine benutzerfreundliche Plattform, die es Nutzern ermöglicht, praxisnahe Erfahrungen mit künstlicher Intelligenz (KI) zu sammeln. Die Plattform bietet eine interaktive Umgebung, in der verschiedene KIs gegeneinander antreten können und Nutzer die Möglichkeit haben, eigene KI-Entwicklungen zu testen.

## Inhaltsverzeichnis

- [KIMaster - Plattform zum Vergleich von Spiele-KIs](#kimaster---plattform-zum-vergleich-von-spiele-kis)
  - [Projektbeschreibung](#projektbeschreibung)
  - [Inhaltsverzeichnis](#inhaltsverzeichnis)
  - [Funktionen](#funktionen)
  - [Technologiestack](#technologiestack)
  - [Installationsanweisungen](#installationsanweisungen)
    - [Voraussetzungen](#voraussetzungen)
    - [Schritte](#schritte)
    - [Hinweise zum Build Prozess](#hinweise-zum-build-prozess)
  - [Systemanforderungen](#systemanforderungen)
  - [Nutzung der Plattform](#nutzung-der-plattform)
  - [Dokumentation](#dokumentation)
  - [Team](#team)
  - [Externe Repositories](#externe-repositories)
  - [Lizenz](#lizenz)

## Funktionen

- Spielen gegen andere Spieler in verschiedenen Spielen
- Spielen gegen vortrainierte KI-Modelle (KIM)
- Anbinden eigener KI-Implementierungen über API
- Vergleich von verschiedenen Spiele-KIs
- Interaktive Benutzeroberfläche mit Webseite
- Automatisierte Tests zur Qualitätssicherung
- Unterstützung für Docker und Docker-Compose

## Technologiestack

- **Backend**: Python 3.11, FastAPI, PyTorch, TensorFlow, Docker
- **Frontend**: Vue.js, Vuex, Vue Router, JavaScript/TypeScript
- **Datenbank**: Keine direkte Datenbank, Speicherung erfolgt in Docker-Volumes
- **Infrastruktur**: Docker, Docker-Compose

## Installationsanweisungen

### Voraussetzungen

- Docker Desktop
- Git
- Optional: CUDA-fähige GPU für schnelleres Training von KI-Modellen

### Schritte

1. **Docker installieren**
   - Besuche die [Docker Desktop Webseite](https://www.docker.com/products/docker-desktop) und lade Docker Desktop herunter.
   - Folge den Installationsanweisungen für dein Betriebssystem (Windows, macOS, Linux).
   - Nach der Installation starte Docker Desktop und stelle sicher, dass es läuft.

2. **Repository klonen**

   ```sh
   git clone https://github.com/12ghostrider21/KIMaster.git
   cd KIMaster
   ```

3. **Docker-Container starten**

   Für Windows:
   ```sh
   ./start.cmd
   ```

   Für Unix (Linux, macOS):
   ```sh
   chmod +x start.sh
   ./start.sh
   ```

### Hinweise zum Build Prozess

Beim ersten Mal kann der Build-Prozess je nach Internetverbindung sehr lange dauern. Bei einer Download-Geschwindigkeit von 50 Mbit/s dauert der Prozess etwa 30 Minuten. Nach Abschluss des Prozesses werden automatisch alle notwendigen Container in Docker gestartet.

## Systemanforderungen

- **Prozessor (CPU)**: 64-Bit mit Second Level Address Translation (SLAT)
- **Arbeitsspeicher (RAM)**: 4 GB
- **Festplattenspeicher**: min. 20 GB
- **Internetverbindung**: zum Herunterladen von Paketen
- **Optional**: Eine CUDA (12) fähige GPU

## Nutzung der Plattform

- **Weboberfläche**: Lokal erreichbar unter [http://localhost:8086/](http://localhost:8086/). Im THM-Netz ist die Webseite unter [https://kimaster.mni.thm.de](https://kimaster.mni.thm.de) erreichbar.
- **Debug-Webseite**: Lokal erreichbar unter [http://localhost:8087/](http://localhost:8087/). Die Debug-Webseite wird nicht im THM-Netz bereitgestellt.
- **API**: Lokal erreichbar unter [ws://localhost:8010/ws](ws://localhost:8010/ws). Im THM-Netz ist die API unter [wss://kimaster.mni.thm.de/ws](wss://kimaster.mni.thm.de/ws) erreichbar.

## Dokumentation

Alle relevanten Dokumentationsinhalte sind im Verzeichnis `spezifikation` im Hauptbranch (`main`) des Repositories verfügbar. Dort findet sich die umfassende Spezifikationen und Anleitungen, die helfen sollen, das Projekt besser zu verstehen und effektiv zu nutzen. ZU finde unter folgendem Direkt-Link: [Spezifikation](https://github.com/12ghostrider21/KIMaster/tree/main/Spezifikation).

## Team

[ThorbenJones](https://github.com/ThorbenJones): Projektleitung, Frontend-Entwicklung

[12ghostrider21](https://github.com/12ghostrider21): Stellvertretende Projektleitung, Dokumentationsspezialist 

[Flying-Suricate](https://github.com/Flying-Suricate): Technischer Architekt, Backend-Entwicklung

[maximilianlbachmann](https://github.com/maximilianlbachmann): Backend-Entwicklung, Spiele-Entwicklung

[S-Reinhard](https://github.com/S-Reinhard): Dockerspezialist, QA-Ingenieur

[PascalWaldschmidt](https://github.com/PascalWaldschmidt): Frontend-Entwicklung, UI/UX-Designer

[OmarKarkotli](https://github.com/OmarKarkotli): UI/UX-Designer, Technischer Architekt

## Externe Repositories

Für die Basisimplementierung der KI-Trainierung wurden Teile aus [suragnair/alpha-zero-general](https://github.com/suragnair/alpha-zero-general) verwendet.

## Lizenz

Dieses Projekt steht unter der [MIT Lizenz](LICENSE).
