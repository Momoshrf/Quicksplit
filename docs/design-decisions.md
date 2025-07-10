---
title: Design Decisions
nav_order: 3
---

{: .label }
Arblir Meta & Mohamed Shiref

{: .no_toc }
# Design decisions

<details open markdown="block">
{: .text-delta }
<summary>Table of contents</summary>
+ ToC
{: toc }
</details>

## 01: SQLite vs. andere Datenbanken

### Meta

Status
: Work in progress - **Decided** - Obsolete

Updated
: 27-Nov-2024

### Problem statement

Welche Datenbank sollen wir für QuickSplit verwenden? Wir brauchen eine Lösung, die Events, Users und Expenses speichern kann und einfach zu implementieren ist.

Als Studenten haben wir begrenzte Erfahrung mit Datenbanken und wollen uns auf die App-Logik konzentrieren.

### Decision

Wir verwenden **SQLite** mit plain SQL (kein ORM).

SQLite ist perfekt für unseren Prototyp, da es keine Installation erfordert und direkt mit Python funktioniert. Plain SQL gibt uns volle Kontrolle und ist einfacher zu verstehen als SQLAlchemy.

*Decision was taken by:* Arblir Meta, Mohamed Shiref

### Regarded options

| Criterion | SQLite | MySQL | PostgreSQL | SQLAlchemy |
| --- | --- | --- | --- | --- |
| **Setup Aufwand** | ✔️ Keine Installation | ❌ Server Setup | ❌ Server Setup | ❔ Zusätzliche Abstraktionsschicht |
| **Lernkurve** | ✔️ Einfaches SQL | ❌ Komplex | ❌ Komplex | ❌ ORM Konzepte lernen |
| **Prototyp geeignet** | ✔️ Perfekt | ❌ Overkill | ❌ Overkill | ❔ Zu abstrakt |
| **File-basiert** | ✔️ Eine Datei | ❌ Server nötig | ❌ Server nötig | ❔ Abhängig |

---

## 02: Bootstrap vs. eigenes CSS

### Meta

Status
: Work in progress - **Decided** - Obsolete

Updated
: 28-Nov-2024

### Problem statement

Wie sollen wir das Frontend gestalten? Wir wollen ein modernes, responsives Design, haben aber begrenzte CSS-Erfahrung.

### Decision

Wir verwenden **Bootstrap 5** als CSS Framework.

Bootstrap gibt uns sofort ein professionelles Aussehen und responsive Design. Das Grid-System und die vorgefertigten Komponenten sparen uns viel Zeit.

*Decision was taken by:* Mohamed Shiref, Arblir Meta

### Regarded options

| Criterion | Bootstrap 5 | Pure CSS | Tailwind CSS |
| --- | --- | --- | --- |
| **Lernaufwand** | ✔️ Klassen verwenden | ❌ CSS von Grund auf | ❌ Utility-First lernen |
| **Geschwindigkeit** | ✔️ Schnell | ❌ Langsam | ❔ Mittel |
| **Responsive** | ✔️ Automatisch | ❌ Selbst machen | ✔️ Automatisch |
| **Dokumentation** | ✔️ Excellent | ❔ MDN/W3Schools | ✔️ Gut |

---

## 03: Flask Templates vs. Single Page App

### Meta

Status
: Work in progress - **Decided** - Obsolete

Updated
: 28-Nov-2024

### Problem statement

Sollen wir Server-side Rendering mit Flask Templates oder eine Single Page Application (SPA) mit JavaScript Framework bauen?

### Decision

Wir verwenden **Flask Templates mit Jinja2**.

Für unseren Prototyp ist Server-side Rendering einfacher. Wir können uns auf die Backend-Logik konzentrieren und müssen kein zusätzliches JavaScript Framework lernen.

*Decision was taken by:* Arblir Meta, Mohamed Shiref

### Regarded options

| Criterion | Flask Templates | React SPA | Vue.js SPA |
| --- | --- | --- | --- |
| **Komplexität** | ✔️ Einfach | ❌ Zusätzliches Framework | ❌ Zusätzliches Framework |
| **Lernkurve** | ✔️ Jinja2 ähnlich HTML | ❌ React Konzepte | ❌ Vue Konzepte |
| **Prototyp Speed** | ✔️ Schnell | ❌ Mehr Setup | ❌ Mehr Setup |
| **Backend Integration** | ✔️ Direkt | ❌ API nötig | ❌ API nötig |

---
