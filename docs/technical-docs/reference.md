---
title: Reference
parent: Technical Docs
nav_order: 3
---

{: .label }
[Jane Dane]

{: .no_toc }
# Reference documentation

{: .attention }
> This page collects internal functions, routes with their functions, and APIs (if any).
> 
> See [Uber](https://developer.uber.com/docs/drivers/references/api) or [PayPal](https://developer.paypal.com/api/rest/) for exemplary high-quality API reference documentation.
>
> You may delete this `attention` box.

<details open markdown="block">
{: .text-delta }
<summary>Table of contents</summary>
+ ToC
{: toc }
</details>

## events.py

### create_event()

**Route:** `/events/create`

**Methods:** `GET`,`POST`

**Purpose:** Erstellt ein neues Event. Bei `GET` wird das Formular angezeigt, bei `POST` werden die Eventdaten in die Datenbank geschrieben und der Benutzer weitergeleitet.

**Sample output:**

c:\Users\User\Pictures\Screenshots\create.html.png

---

## Eventübersicht

### `show_event(event_id)`

**Route:** `/events/<int:event_id>`

**Methods:** `GET`

**Purpose:** Zeigt alle Ausgaben eines bestimmten Events. Dient als zentrale Übersicht pro Event mit Option zur weiteren Bearbeitung.

**Sample output:**

c:\Users\User\Pictures\Screenshots\show.html.png
---
## Ausgaben hinzufügen

### `add_expense(event_id)`

**Route:** `/events/<int:event_id>/expenses/add`

**Methods:** `GET`,`POST`

**Purpose:** Zeigt das Formular zur Hinzufügung neuer Ausgaben (`GET`) oder fügt eine neue Ausgabe in die Datenbank ein (`POST`).

**Sample output:**

c:\Users\User\Pictures\Screenshots\add_expense.html.png
---

## Schuldenübersicht

### `summary(event_id)`

**Route:** `/events/<int:event_id>/summary`

**Methods:** `GET`

**Purpose:** Diese Route berechnet, wie viel jeder Teilnehmer eines Events im Verhältnis zu den anderen bezahlt hat und erstellt eine kompakte Schuldenübersicht. Dabei wird so optimiert, dass möglichst wenige Transaktionen notwendig sind. Die Informationen werden als Übersicht aufbereitet und im Template `summary.html` angezeigt.

**Sample output:**

![alt text](<summary.html [1].png>)

![alt text](<summary.html [2].png>)