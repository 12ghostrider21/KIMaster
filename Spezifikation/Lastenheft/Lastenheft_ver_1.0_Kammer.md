# Lastenheft: Plattform zum Vergleich von Spiele-KIs

## 1 Einleitung

In einer Zeit, in der künstliche Intelligenz (KI) zunehmend Einzug in verschiedene Bereiche unserer Gesellschaft hält, ist es entscheidend, das Verständnis und die Anwendung von KI-Konzepten zu fördern. Insbesondere im Bildungsumfeld wird deutlich, wie wichtig es ist, Studierenden praxisnahe Erfahrungen zu ermöglichen, um ihre Fähigkeiten in der KI-Entwicklung zu vertiefen.

> Übergang hier noch "unschön"

Bisher existieren bereits verschiedene Ansätze und Technologien, die den Einsatz von KI in Spielen ermöglichen, darunter auch das bekannte alpha-zero Framework 
> Cite fehlt. 

Jedoch fehlt es bisher an einer benutzerfreundlichen Plattform, die es ermöglicht, verschiedene KIs miteinander zu vergleichen und eigene KIs zu testen. Hier setzt unser Projekt an.

Das Ziel ist es, eine intuitive und zugängliche Plattform zu entwickeln, die es den Benutzern erlaubt, Spiele gegen KIs zu spielen und ihre eigenen KIs zu testen und zu vergleichen. Durch die direkte praktische Anwendung von KI-Konzepten erhalten die Nutzer nicht nur einen tieferen Einblick in die Welt der KI-Entwicklung, sondern können auch ihre Fähigkeiten auf eine unterhaltsame und interaktive Weise verbessern.

Die Plattform soll einen ansprechenden Zugang zur Welt der KI-Entwicklung bieten und ist sowohl für Anfänger als auch für fortgeschrittene Benutzer konzipiert. Sie soll dabei nicht nur Wissen vermitteln, sondern auch als Werkzeug dienen, um praxisnahe Erfahrungen zu sammeln und die Fähigkeiten im Bereich der KI-Entwicklung zu erweitern.

## 2 Konzept

Das Projekt zielt auf die Entwicklung einer benutzerfreundlichen Plattform hin, die es den Nutzern ermöglicht, Spiele gegen KIs zu spielen und eigene KIs zu testen und zu vergleichen. Dabei soll besonderer Wert auf intuitive Bedienbarkeit und hohe Nutzerfreundlichkeit gelegt werden.

Die Plattform bietet Anfängern und fortgeschrittenen Benutzern gleichermaßen die Möglichkeit, praxisnahe Erfahrungen im Bereich der KI-Entwicklung zu sammeln. Durch Spiele gegen KIs und die Möglichkeit, eigene KIs zu testen und zu vergleichen, können die Benutzer ihre Fähigkeiten erweitern und ihr Verständnis für KI-Konzepte vertiefen.

Zudem soll die Plattform sich an Studierende, Entwickler und KI-Enthusiasten, die ihr Wissen und ihre Fähigkeiten im Bereich der KI-Entwicklung erweitern möchten, richten.

## 3 Funktionale Anforderungen

### 3.1 Must-Haves

- Konfiguration von zu spielenden Spielen mit Auswahl des Spiels, der Wahl des Spielmodis (Spieler gegen Spieler, Spieler gegen bereitgestellte KI und Spieler-KI gegen bereitgestellte KI) und bei einfacheren Spielen dynamische Spielfeldoptionen.

- Umgesetzte Spiele:
  - Othello (Reversi)
  - Tic-Tac-Toe
  - Vier gewinnt
  - Nim
  - Dame
  - Go
  - Waldmeister
  
> Ggf. mal ansehen:   
>  Abalone (Spiel): https://www.youtube.com/shorts/5KTdURoUsBQ
>  Dittle - Dice Battle: https://www.youtube.com/watch?v=UPr-CVPPqEg
>  Eternas: https://www.youtube.com/shorts/DRUBPY_YSHk
> Kanallink: https://www.youtube.com/@Games4two_
  

- Möglichkeit zur Erstellung oder Beitritt zu virtuellen identifizierbaren Räumen (Lobby), die noch nicht voll besetzt sind, um einen Mehrspielerbetrieb zu ermöglichen. 

> Mehr Details hierzu, wie die Modi KI<=>KI, etc. realisiert werden: Bereitstellung von generierten Schlüsseln zum KI-Beitritt über ein Application Programming Interface (API).

- Graphische Darstellung aktiver Spiele in den Lobbys mit PyGame.

- Interaktion mit der Spieloberfläche im Spielermodus mit Mauseingabe.

> und Tastatur? Mobile Geräte?

- Möglichkeiten des Spieleabbruchs und des Verlassens einer Lobby mit Rückkehr zur Hauptseite.

- API-Bereitstellung für Spiele mit Spieler-KI-Interaktion, inklusive Anleitung und erforderlichen Dateien zur Verbindung.

- Darstellung von Impressum und Datenschutzerklärung auf der Webseite.

### 3.2 Nice-to-Haves

- Einstellbare Schwierigkeitsgrade für die vorab trainierten bereitgestellten KI-Implementierungen.

- Implementierung einer Benutzeridentifikation (Benutzername) zur Speicherung von Spieler- oder KI-Punkten. Dazu eine Anzeigetafel mit Punktedarstellung.

- Farbmusterauswahl der Webseite (Dark- oder White-Mode).

- Zusätzliche Konfiguration von zu spielenden Spielen mit Wahl des Spielmodis (Spieler-KI gegen Spieler-KI).

- Implementierung weiterer Spiele, z.B.:
  - Schach
  - Mühle
  - Halma

- Möglichkeit zum Abspeichern von Spielen für spätere Analyse oder Fortsetzung des Spiels, sowie Lademöglichkeit abgespeicherter Spiele.

### 3.3 If-Time-Allows

- Für statistische Auswertungen eine Möglichkeit zur Ausführung vieler Spiele ohne graphische Oberfläche für die Spieler-KIs. Einordnungen der Stärke der KI.

- Barrierefreiheit der Webseite ausbauen.
  - Vollständig mausfreie Bedienung.

- Möglichkeit in der Spieleoberfläche einzelne Züge zurückzunehmen.

- Mehrsprachenunterstützung der Webseite und Anleitungen (Englisch, Deutsch).

- Implementierung weiterer Spiele:
  - Spiele mit Zufallskomponente.

- Zur Förderung des Spielespaßes eine Erweiterung der Punkteanzeigen mit Ranglisten und Erfolge.

## 4 Qualitative Anforderungen

### 4.1 Benutzerfreundlichkeit
- Die Benutzeroberfläche soll intuitiv gestaltet sein, um eine einfache Navigation für Benutzer zu ermöglichen.
- Es sollen klare Anleitungen und Hilfestellungen zur Verfügung gestellt werden, um den Einstieg für neue Benutzer zu erleichtern.

### 4.2 Skalierbarkeit
- Die Plattform soll skalierbar sein, um eine steigende Anzahl von Benutzern und Spielen zu unterstützen, ohne dass die Leistung beeinträchtigt wird.
- Die Architektur der Plattform sollte flexibel genug sein, um zukünftige Erweiterungen und Anpassungen problemlos zu ermöglichen.

> Auch eine Anforderung an die Dokumentation

### 4.3 Performance und Stabilität
- Die Plattform sollte eine schnelle Ladezeit und eine reibungslose Benutzererfahrung bieten, auch bei einer hohen Anzahl gleichzeitiger Benutzer.


> Stakeholder und deren Ziele
> Was sind die geplanten Abnahmetests?
> Welche Dokumentation gibt es am Ende?

