---
title: Architecture
parent: Technical Docs
nav_order: 1
---

{: .label }
Arblir Meta, Mohamed Shiref

{: .no_toc }
# Architecture

![Ablaufdiagramm](../assets/images/flowchart.png)

<details open markdown="block">
{: .text-delta }
<summary>Table of contents</summary>
+ ToC
{: toc }
</details>

## Overview

QuickSplit ist eine Flask-basierte Webanwendung zur Verwaltung und fairen Aufteilung von Gruppenausgaben. Die Anwendung ermöglicht es registrierten Benutzern, Events zu erstellen und zu verwalten, lokale Teilnehmer hinzuzufügen und Ausgaben automatisch zu berechnen.

Die Architektur folgt dem Model-View-Controller (MVC) Muster:

- **Model**: SQLite-Datenbank mit sechs Tabellen (users, events, participants, expenses, etc.)
- **View**: Jinja2-Templates mit Bootstrap 5 und eigenen CSS-Anpassungen
- **Controller**: Flask-Blueprints für modulare Routen-Verwaltung

Die Anwendung nutzt Session-basierte Authentifizierung und ist vollständig auf Deutsch lokalisiert.

## Komponenten und Datenfluss

Unsere App besteht aus verschiedenen Komponenten, die zusammenarbeiten:

### 1. Authentifizierung (`auth.py`)
- **Registrierung**: Neue Benutzer können sich anmelden
- **Login/Logout**: Session-basierte Authentifizierung
- **Passwort-Hashing**: Sichere Speicherung mit Werkzeug

### 2. Event-Management (`routes/events.py`)
- **Event-Erstellung**: Benutzer können Events erstellen
- **Teilnehmer-Verwaltung**: Lokale Teilnehmer hinzufügen
- **Ausgaben-Tracking**: Ausgaben innerhalb eines Events
- **Schulden-Berechnung**: Automatische Berechnung wer wem was schuldet

### 3. Ausgaben-Management (`routes/expenses.py`)
- **Ausgaben-Übersicht**: Detaillierte Zusammenfassung aller Ausgaben
- **Bezahl-Status**: Tracking welche Schulden bereits beglichen sind
- **Rückzahlungsvorschläge**: Optimierte Transaktionsvorschläge

### 4. Datenbank (`database.py`)
- **SQLite**: Lokale Datenbankdatei (`quicksplit.db`)
- **Tabellen**: 6 Haupttabellen für Users, Events, Participants, Expenses
- **Automatische Initialisierung**: Tabellen werden beim Start erstellt

### 5. Frontend (`templates/` & `static/`)
- **Base Template**: Gemeinsames Layout mit Navigation
- **Bootstrap**: Responsive Design-Framework
- **Eigene CSS**: Anpassungen für bessere UX (Hover-Effekte, Gradients)
- **Emojis**: Freundliche Icons ohne zusätzliche Ressourcen

## Datenfluss

Der typische Datenfluss sieht so aus:

1. **Benutzer-Aktion**: Login, Event erstellen, Ausgabe hinzufügen
2. **Route-Verarbeitung**: Flask-Blueprint verarbeitet Request
3. **Datenbank-Zugriff**: SQLite-Queries über `get_db_connection()`
4. **Geschäftslogik**: Berechnungen (Schulden, Rückzahlungen)
5. **Template-Rendering**: Jinja2 rendert HTML mit Bootstrap
6. **Response**: Vollständige HTML-Seite mit Flash-Messages

## Codemap

Hier ist ein Überblick über die wichtigsten Dateien und Ordner:

### **Hauptdateien:**
- `app.py`: Flask-App Setup, Blueprint-Registrierung, Startup
- `database.py`: Datenbank-Initialisierung und Verbindung
- `auth.py`: Authentifizierung (Login, Registrierung, Logout)
- `requirements.txt`: Python-Dependencies

### **routes/:** Controller-Logik
- `events.py`: Event-CRUD, Teilnehmer-Verwaltung, Schulden-Berechnung
- `expenses.py`: Ausgaben-Übersicht, Bezahl-Status-Toggle

### **templates/:** HTML-Templates
- `base.html`: Basis-Layout mit Navigation, Flash-Messages
- `index.html`: Dashboard mit Feature-Übersicht
- `404.html`: Eigene Fehlerseite
- `login.html` / `register.html`: Authentifizierung
- `events/`: Event-spezifische Templates
  - `list.html`: Event-Übersicht
  - `create.html`: Event-Erstellung
  - `show.html`: Event-Details
  - `add_expense.html`: Ausgabe hinzufügen
  - `summary.html`: Detaillierte Ausgaben-Übersicht

### **static/:** Frontend-Ressourcen
- `style.css`: Eigene CSS-Anpassungen (Hover-Effekte, Gradients)

### **docs/:** Projektdokumentation
- `technical-docs/`: Technische Dokumentation
- `design-decisions.md`: Begründete Architektur-Entscheidungen
- `Quellen.md`: Verwendete Tutorials und Ressourcen

## Cross-cutting concerns

### **Session-Management**
- Flask-Sessions für Benutzer-Authentifizierung
- Session-Checks in allen geschützten Routen
- Automatische Weiterleitung zu Login bei fehlender Session

### **Flash-Messages**
- Benutzer-Feedback für alle Aktionen
- Erfolgs- und Fehlermeldungen
- Integration in Base-Template

### **Responsive Design**
- Bootstrap 5 Grid-System
- Mobile-first Approach
- Eigene Media-Queries für Feintuning

### **Datenkonsistenz**
- Foreign Key Constraints in SQLite
- Transaktionale Operationen
- Automatische Datenbank-Initialisierung

### **Lokalisierung**
- Vollständig deutsche Benutzeroberfläche
- Deutsche Fehlermeldungen und Flash-Messages
- Kulturspezifische Datumsformate

Die Architektur ist bewusst einfach gehalten, um schnelle Entwicklung zu ermöglichen, während sie gleichzeitig skalierbar und wartbar bleibt. Weitere Details zu spezifischen Designentscheidungen finden sich in den [Design Decisions](../design-decisions.md).
