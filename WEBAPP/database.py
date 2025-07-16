import sqlite3

DATABASE = 'quicksplit.db'

def get_db_connection():
    """Verbindung zur SQLite-Datenbank herstellen."""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_database():
    """Alle benötigten Tabellen erstellen, falls sie noch nicht existieren."""
    conn = get_db_connection()

    # Benutzer (App-User)
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')

    # Events
    conn.execute('''
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            owner_id INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (owner_id) REFERENCES users(id)
        )
    ''')

    # Teilnehmer eines Events (User nimmt an Event teil)
    conn.execute('''
        CREATE TABLE IF NOT EXISTS event_participants (
            event_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            PRIMARY KEY (event_id, user_id),
            FOREIGN KEY (event_id) REFERENCES events(id),
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')

    # Ausgaben in einem Event
    conn.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            amount REAL NOT NULL,
            date DATE DEFAULT CURRENT_DATE,
            payer_id INTEGER NOT NULL,
            event_id INTEGER NOT NULL,
            FOREIGN KEY (payer_id) REFERENCES users(id),
            FOREIGN KEY (event_id) REFERENCES events(id)
        )
    ''')

    # Wer teilt sich die Ausgabe und wie viel?
    conn.execute('''
        CREATE TABLE IF NOT EXISTS expense_participants (
            expense_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            amount_owed REAL NOT NULL,
            PRIMARY KEY (expense_id, user_id),
            FOREIGN KEY (expense_id) REFERENCES expenses(id),
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')

    # Lokale Teilnehmer (nicht registrierte Benutzer)
    conn.execute('''
        CREATE TABLE IF NOT EXISTS participants (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            event_id INTEGER NOT NULL,
            FOREIGN KEY (event_id) REFERENCES events(id)
        )
    ''')

    # Neue Spalte 'paid' zur Tabelle 'expense_participants' hinzufügen (falls noch nicht vorhanden)
    try:
        conn.execute('ALTER TABLE expense_participants ADD COLUMN paid BOOLEAN DEFAULT 0')
        print("Spalte 'paid' zur Tabelle 'expense_participants' hinzugefügt.")
    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e).lower():
            print("Spalte 'paid' existiert bereits.")
        else:
            raise

    conn.commit()
    conn.close()
    print(" Datenbank wurde erfolgreich initialisiert!")

if __name__ == '__main__':
    init_database()
