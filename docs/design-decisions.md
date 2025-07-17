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

## Legende

{: .info }
> **Bewertungssymbole in den Tabellen:**
> - ✔️ = **Vorteil/Gut** - klarer Gewinner bei diesem Kriterium
> - ❌ = **Nachteil/Schlecht** - klarer Verlierer bei diesem Kriterium  
> - ❔ = **Neutral/Abhängig** - kommt auf die Situation an, oder mittleres Niveau

## 01: SQLite vs. andere Datenbanken

### Meta

Status
: Work in progress - **Decided** - Obsolete

Updated
: 26-Jun-2025

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
: 27-Jun-2025

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

## 03: Emojis für bessere User Experience

### Meta

Status
: Work in progress - **Decided** - Obsolete

Updated
: 27-Jun-2025

### Problem statement

Wie können wir unsere App visuell ansprechender machen, ohne aufwendige Icon-Sets zu verwenden? Wir wollen eine freundliche, moderne Benutzeroberfläche, haben aber begrenzte Design-Ressourcen.

### Decision

Wir verwenden **Emojis** durchgehend in der gesamten App.

Emojis sind universell, kostenlos und machen die App sofort freundlicher. Sie funktionieren auf allen Geräten und Browsern ohne zusätzliche Ressourcen.

*Decision was taken by:* Mohamed Shiref, Arblir Meta

### Regarded options

| Criterion | Emojis | Font Awesome | Bootstrap Icons | Custom Icons |
| --- | --- | --- | --- | --- |
| **Kosten** | ✔️ Kostenlos | ❌ Pro kostet | ✔️ Kostenlos | ❌ Design-Aufwand |
| **Ladezeit** | ✔️ Keine extra Files | ❌ CSS/JS laden | ❌ CSS/JS laden | ❔ Abhängig |
| **Konsistenz** | ❔ Platform-abhängig | ✔️ Immer gleich | ✔️ Immer gleich | ✔️ Kontrolle |
| **Freundlichkeit** | ✔️ Sehr freundlich | ❔ Neutral | ❔ Neutral | ❔ Abhängig |

---

## 04: Session-basierte Authentifizierung

### Meta

Status
: Work in progress - **Decided** - Obsolete

Updated
: 06-Jul-2025

### Problem statement

Wie sollen wir User-Authentifizierung implementieren? Wir brauchen eine sichere, aber einfache Lösung für Login/Logout.

### Decision

Wir verwenden **Flask Sessions** mit Passwort-Hashing.

Sessions sind einfach zu implementieren, in Flask integriert und ausreichend sicher für unseren Prototyp. Werkzeug-Hashing schützt die Passwörter.

*Decision was taken by:* Arblir Meta, Mohamed Shiref

### Regarded options

| Criterion | Flask Sessions | JWT Tokens | OAuth | Basic Auth |
| --- | --- | --- | --- | --- |
| **Einfachheit** | ✔️ Built-in | ❌ Extra Library | ❌ Komplex | ✔️ Einfach |
| **Sicherheit** | ✔️ Ausreichend | ✔️ Sehr gut | ✔️ Sehr gut | ❌ Unsicher |
| **Prototyp geeignet** | ✔️ Perfekt | ❌ Overkill | ❌ Overkill | ❌ Zu simpel |
| **Lernaufwand** | ✔️ Minimal | ❌ Hoch | ❌ Sehr hoch | ✔️ Minimal |

---

## 05: Zusätzliche CSS-Anpassungen trotz Bootstrap

### Meta

Status
: Work in progress - **Decided** - Obsolete

Updated
: 06-Jul-2025

### Problem statement

Reicht Bootstrap allein für ein ansprechendes Design, oder brauchen wir zusätzliche CSS-Anpassungen? Bootstrap-Seiten sehen oft "standard" aus.

### Decision

Wir verwenden **zusätzliche CSS-Anpassungen** in `style.css` trotz Bootstrap.

Bootstrap gibt uns die Grundlage, aber eigene CSS-Anpassungen machen die App einzigartiger und polierter. Hover-Effekte, Gradients und runde Buttons verbessern das Nutzererlebnis.

*Decision was taken by:* Mohamed Shiref, Arblir Meta

### Regarded options

| Criterion | Nur Bootstrap | Bootstrap + Custom CSS | Komplett eigenes CSS |
| --- | --- | --- | --- |
| **Entwicklungszeit** | ✔️ Sehr schnell | ❔ Etwas länger | ❌ Sehr aufwendig |
| **Einzigartigkeit** | ❌ Standard-Look | ✔️ Individuelle Note | ✔️ Komplett individuell |
| **Konsistenz** | ✔️ Automatisch | ❔ Manuell sicherstellen | ❌ Schwierig |
| **Wartbarkeit** | ✔️ Einfach | ✔️ Überschaubar | ❌ Komplex |

---

## 06: Lokale Teilnehmer ohne Registrierung

### Meta

Status
: Work in progress - **Decided** - Obsolete

Updated
: 14-Jul-2025

### Problem statement

Sollen alle Teilnehmer einen Account erstellen müssen, oder können auch Nicht-Registrierte an Events teilnehmen?

### Decision

Wir verwenden **Lokale Teilnehmer** zusätzlich zu registrierten Usern.

Nicht jeder will sich registrieren, nur um bei der Reiseabrechnung dabei zu sein. Lokale Teilnehmer senken die Einstiegshürde enorm.

*Decision was taken by:* Arblir Meta, Mohamed Shiref

### Regarded options

| Criterion | Nur Registrierte | Nur Lokale | Gemischtes System |
| --- | --- | --- | --- |
| **Einstiegshürde** | ❌ Hoch | ✔️ Niedrig | ✔️ Flexibel |
| **Persistenz** | ✔️ Dauerhaft | ❌ Event-gebunden | ✔️ Flexibel |
| **Datenmodell** | ✔️ Einfach | ✔️ Einfach | ❌ Komplexer |
| **Realitätsnähe** | ❌ Unrealistisch | ❌ Limitiert | ✔️ Realistisch |

---

## 07: Minimalistisches Design mit Fokus auf Funktionalität

### Meta

Status
: Work in progress - **Decided** - Obsolete

Updated
: 14-Jul-2025

### Problem statement

Sollen wir ein komplexes Dashboard mit vielen Features oder eine einfache, fokussierte Benutzeroberfläche entwickeln?

### Decision

Wir verwenden **Minimalistisches Design** mit klarem Fokus auf Kernfunktionen.

Weniger ist mehr. Benutzer wollen schnell ihre Ausgaben erfassen und nicht durch komplexe UIs navigieren. Klare Buttons, einfache Formen, direkter Workflow.

*Decision was taken by:* Mohamed Shiref, Arblir Meta

### Regarded options

| Criterion | Minimalistisch | Dashboard-Style | Feature-Rich |
| --- | --- | --- | --- |
| **Lernkurve** | ✔️ Sofort nutzbar | ❌ Einarbeitung | ❌ Überfordernd |
| **Mobile Nutzung** | ✔️ Perfekt | ❔ Bedingt | ❌ Schwierig |
| **Entwicklungszeit** | ✔️ Schnell | ❌ Aufwendig | ❌ Sehr aufwendig |
| **User Experience** | ✔️ Klar | ❔ Informativ | ❌ Verwirrend |

---

## 08: Flash Messages für User-Feedback

### Meta

Status
: Work in progress - **Decided** - Obsolete

Updated
: 15-Jul-2025

### Problem statement

Wie sollen wir Users über erfolgreiche Aktionen oder Fehlermeldungen informieren? Users brauchen direktes Feedback, wenn sie etwas gemacht haben.

### Decision

Wir verwenden **Flask Flash Messages** für User-Feedback.

Flash Messages sind einfach zu implementieren, erscheinen nach Aktionen und verschwinden automatisch. Sie geben Users sofortiges Feedback ohne zusätzliche JavaScript-Komplexität.

*Decision was taken by:* Arblir Meta, Mohamed Shiref

### Regarded options

| Criterion | Flash Messages | JavaScript Alerts | Toast Notifications | Keine Feedback |
| --- | --- | --- | --- | --- |
| **Einfachheit** | ✔️ Built-in Flask | ❌ Extra JavaScript | ❌ Zusätzliche Library | ✔️ Kein Code |
| **User Experience** | ✔️ Smooth Integration | ❌ Aufdringlich | ✔️ Modern | ❌ Verwirrend |
| **Entwicklungszeit** | ✔️ Schnell | ❔ Etwas länger | ❌ Setup nötig | ✔️ Keine Zeit |
| **Styling** | ✔️ Mit Bootstrap | ❌ Schwer anpassbar | ❔ Teilweise anpassbar | ❌ Nicht relevant |

---
