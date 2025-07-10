---
title: Data Model
parent: Technical Docs
nav_order: 2
---

{: .label }
Arblir Meta

{: .no_toc }
# Data model

<details open markdown="block">
{: .text-delta }
<summary>Table of contents</summary>
+ ToC
{: toc }
</details>

# Übersicht

Für QuickSplit haben wir ein vollständiges Datenmodell entwickelt, das alle Features der finalen App abbildet. Die Struktur unterstützt Admin-Verwaltung, Events, Benutzer und komplexe Ausgaben-Aufteilungen.

Da wir uns für SQLite entschieden haben (siehe [Design Decisions](../design-decisions.md)), war es wichtig, ein Schema zu entwerfen, das auch ohne komplexe Joins funktioniert.

# ER-Diagramm

![ER-Diagramm](../assets/images/datenmodel.png)

# Tabellen im Detail

**Admin**

Die Admin-Tabelle speichert Informationen über Benutzer, die sich anmelden und Events erstellen können:

- `id` (INTEGER PRIMARY KEY) - Eindeutige ID (Primärschlüssel)
- `username` (TEXT NOT NULL) - Benutzername für den Login
- `password_hash` (TEXT NOT NULL) - Gehashtes Passwort für die Sicherheit
- `created_at` (DATETIME DEFAULT CURRENT_TIMESTAMP) - Zeitpunkt der Erstellung des Admin-Accounts

Ein Admin kann mehrere Events erstellen.

**Event**

Events sind die Hauptorganisationseinheiten in unserer App:

- `id` (INTEGER PRIMARY KEY) - Eindeutige ID (Primärschlüssel)
- `name` (TEXT NOT NULL) - Name des Events (z.B. "Urlaub in Italien")
- `created_at` (DATETIME DEFAULT CURRENT_TIMESTAMP) - Zeitpunkt der Erstellung
- `admin_id` (INTEGER NOT NULL) - Fremdschlüssel zum Admin, der das Event erstellt hat

Ein Event kann mehrere Benutzer und Ausgaben haben.

**User**

User sind die Teilnehmer eines Events:

- `id` (INTEGER PRIMARY KEY) - Eindeutige ID (Primärschlüssel)
- `name` (TEXT NOT NULL) - Name des Benutzers
- `event_id` (INTEGER NOT NULL) - Fremdschlüssel zum Event, zu dem der Benutzer gehört

Ein Benutzer gehört zu genau einem Event und kann mehrere Ausgaben bezahlen oder an Ausgaben beteiligt sein.

**Expense**

Expenses sind die Ausgaben innerhalb eines Events:

- `id` (INTEGER PRIMARY KEY) - Eindeutige ID (Primärschlüssel)
- `title` (TEXT NOT NULL) - Titel der Ausgabe (z.B. "Hotelrechnung")
- `amount` (REAL NOT NULL) - Betrag in Euro
- `date` (DATETIME DEFAULT CURRENT_TIMESTAMP) - Datum der Ausgabe
- `payer_id` (INTEGER NOT NULL) - Fremdschlüssel zum Benutzer, der bezahlt hat
- `event_id` (INTEGER NOT NULL) - Fremdschlüssel zum Event, zu dem die Ausgabe gehört

Eine Ausgabe gehört zu genau einem Event, hat genau einen Zahler und kann mehrere beteiligte Personen haben.

**ExpenseParticipant**

Diese Tabelle ist eine Verknüpfungstabelle, die die Viele-zu-viele-Beziehung zwischen Ausgaben und beteiligten Benutzern abbildet:

- `expense_id` (INTEGER NOT NULL) - Teil des zusammengesetzten Primärschlüssels, Fremdschlüssel zur Ausgabe
- `user_id` (INTEGER NOT NULL) - Teil des zusammengesetzten Primärschlüssels, Fremdschlüssel zum Benutzer

PRIMARY KEY (expense_id, user_id)

# Beziehungen

- **Admin erstellt Events** (1:n) - Ein Admin kann mehrere Events erstellen
- **Event hat Users** (1:n) - Ein Event kann mehrere Teilnehmer haben  
- **User zahlt Expenses** (1:n) - Ein User kann mehrere Ausgaben bezahlen
- **Event enthält Expenses** (1:n) - Ein Event kann mehrere Ausgaben haben
- **Users beteiligt an Expenses** (n:m) - Über ExpenseParticipant Tabelle

# Wichtige Queries

**Alle Events eines Admins:**
```sql
SELECT * FROM events WHERE admin_id = ? ORDER BY created_at DESC;
```

**Alle Ausgaben eines Events mit Zahler-Namen:**
```sql
SELECT e.*, u.name as payer_name 
FROM expenses e 
JOIN users u ON e.payer_id = u.id 
WHERE e.event_id = ?
ORDER BY e.date DESC;
```

**Alle Teilnehmer einer Ausgabe:**
```sql
SELECT u.name 
FROM users u 
JOIN expense_participants ep ON u.id = ep.user_id 
WHERE ep.expense_id = ?;
```

**Schulden-Berechnung (vereinfacht):**
```sql
-- Berechnung erfolgt in der Anwendungslogik
-- da komplexe Aufteilungen berücksichtigt werden müssen
```

# Design-Überlegungen

**Warum Admin-Tabelle getrennt von Users?**  
Admins sind registrierte Benutzer mit Login-Berechtigung. Users sind nur Teilnehmer eines Events ohne eigenen Login.

**Warum REAL für amount?**  
SQLite REAL entspricht Python float und reicht für Euro-Beträge aus. Einfacher als Cent-Umrechnung.

**Warum ExpenseParticipant ohne zusätzliche Felder?**  
Erstmal einfache gleichmäßige Aufteilung. Später können Felder für Prozentsätze hinzugefügt werden.

**Warum event_id in users?**  
Ein User gehört immer zu genau einem Event. Das vereinfacht Queries und Berechtigungen.



