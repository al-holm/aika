# Nicht-funktionale Anforderungen für das Projekt AIKA

## 1. Einleitung
**Ziel des Dokuments:** Dieses Dokument definiert die nicht-funktionalen Anforderungen für die AIKA-App, die zur Unterstützung der frühen Phasen des Integrationskurses für Migranten dient.

**Anwendungsbereich:** Diese Anforderungen gelten für alle Komponenten des Systems und müssen in allen Entwicklungsphasen eingehalten werden.

## 2. Qualität des Systems/Codes
### Performanz:
- **Antwortzeit:** Die Antwortzeit des Systems sollte unter 2 Sekunden bei einer gleichzeitigen Nutzung von 1000 Benutzern liegen. Studien zeigen, dass Benutzer bei Antwortzeiten über 2 Sekunden die Anwendung als langsam empfinden und ihre Zufriedenheit sinkt. 

### Skalierbarkeit:
- **Horizontale Skalierung:** Das System muss horizontales Skalieren auf bis zu 10 Server unterstützen. Diese Zahl basiert auf einer Schätzung des möglichen Wachstums und der erwarteten Benutzerbasis für die ersten Jahre nach dem Start.

### Zuverlässigkeit:
- **Betriebszeit:** Die Betriebszeit des Systems sollte mindestens 99,9% pro Jahr betragen, was einem maximalen Ausfall von etwa 8,76 Stunden pro Jahr entspricht. Dies ist ein gängiger Standard für hochverfügbare Systeme und wird durch Redundanz, Monitoring und schnelle Fehlerbehebung erreicht. 
- **Mittlere Zeit zwischen Ausfällen (MTBF):** sollte mindestens 1000 Stunden betragen. Dieser Wert stellt sicher, dass das System stabil und zuverlässig bleibt. Er wird durch robuste Hardware, präventive Wartung und umfassende Tests erreicht.

### Erweiterbarkeit:
- **Integration neuer Module:** Neue Module sollten in das System integriert werden können, ohne dass bestehender Code signifikant verändert werden muss. Dies wird durch eine modulare Architektur und die Einhaltung des DRY-Prinzips erreicht, die es ermöglichen, neue Funktionalitäten hinzuzufügen, ohne den bestehenden Code zu beeinträchtigen. 

**Wie dies erreicht wird:**
1. **Modulare Architektur:** Das System sollte in klar abgegrenzte Module unterteilt werden, die unabhängig voneinander entwickelt und gewartet werden können.
2. **Interfacing und Abstraktionen:** Definierte Schnittstellen und Abstraktionen für die Interaktion zwischen Modulen.
3. **Inversion of Control (IoC) und Dependency Injection (DI):** Einsatz von DI-Containern zur Verwaltung von Abhängigkeiten.
4. **DRY Prinzip:** Gemeinsame Funktionalitäten sollten in wiederverwendbare Dienste ausgelagert werden.
5. **Kontraktbasiertes Programmieren:** Festlegung von Verträgen, die Module implementieren müssen.

## 3. Ziele für Code-Metriken
- **Testabdeckung des Codes:** mindestens 80%. 
- **Anzahl der Fehler pro 1000 Zeilen Code (KLOC):** nicht mehr als 0,5. 
- **Durchschnittliche Zeit zur Fehlerbehebung:** nicht mehr als 24 Stunden. 
- **Commits:** sollten gemäß dem Commit-Message-Standard erfolgen. 

## 4. Ziele für Code-Konventionen
- **Einhaltung des PEP 8 Standards für Python-Code.** 
- **Obligatorische Nutzung von Lintern (z.B. pylint).** 
- **Durchführung von Code-Reviews vor dem Merge von Pull-Requests.** 

## 5. Benutzbarkeit (Usability)
### Zielgruppe:
- **Benutzer mit grundlegenden Computerkenntnissen.**

### Ergonomie:
- **Benutzeroberfläche:** Die Benutzeroberfläche muss intuitiv verständlich sein. 
- **Barrierefreiheit:** Barrierefreiheit für Menschen mit Behinderungen muss durch Nutzung von Standards wie WCAG und ARIA gewährleistet sein. Diese Standards bieten Richtlinien zur Gestaltung von Webinhalten, die für Menschen mit Behinderungen zugänglich sind, einschließlich Personen mit Seh-, Hör-, Mobilitäts- und kognitiven Einschränkungen. 

## 6. Technische Anforderungen
### Zu nutzende Technologien:
- **Betriebssysteme:** Android, iOS; 

### Werkzeuge und Software:
- **Versionskontrollsystem:** Git
- **Automatisierte Testsysteme:** Jenkins oder Alternativen wie Travis CI, CircleCI 

## 7. Anforderungen an Dokumentation
- **Benutzerdokumentation:** muss Anleitungen zur Installation, Nutzung und Problembehebung enthalten.
- **Technische Dokumentation:** muss die Systemarchitektur, API-Beschreibungen und Datenbankschemata umfassen. 
- **Aktualisierungen:** Die Dokumentation sollte regelmäßig aktualisiert werden, um mit den neuesten Änderungen und Funktionen des Systems Schritt zu halten.

## Motivation
Die durchschnittliche Wartezeit für einen Integrationskurs betrug im Jahr 2023 mehr als 5 Monate (laut Bundesrechnungshof). Dies ist eine Zeitspanne, in der Flüchtlinge und andere Migrantengruppen auf ein Kursangebot warten müssen. Es fehlt auch an Personal und zugänglichen Angeboten im Bereich Recht & politische Bildung, was das Leben in Deutschland für viele Menschen erschwert und die Arbeit von Sozialarbeitern ineffizient macht.

## Umsetzung
Der Benutzer interagiert hauptsächlich über einen Chat mit AIKA, in dem er mit einem Bot kommuniziert, dessen Antworten mithilfe von auf dem Server laufenden LLMs generiert werden.

## Curriculum von AIKA
### Sprache:
Das Curriculum entspricht dem Sprachniveau A2.1 und zielt darauf ab, die Schreib-, Hör- und Lesefähigkeiten zu verbessern. Das Sprechen wird in einer späteren Phase integriert.

Das intelligente Tutorensystem von AIKA hilft dem Benutzer, das Curriculum zu beherrschen, indem es den Lernprozess an die Bedürfnisse des Benutzers anpasst, den aktuellen Fortschritt bewertet und geeignete Aufgaben generiert.
