import sqlite3

DATABASE = 'quicksplit.db'

def get_db_connection():
    """Create a connection to the SQLite database."""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_database():
    """Create all necessary tables if they don't exist."""
    conn = get_db_connection()

    # Users table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')

    # Events table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            owner_id INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (owner_id) REFERENCES users (id)
        )
    ''')

    # Event participants (many-to-many)
    conn.execute('''
        CREATE TABLE IF NOT EXISTS event_participants (
            event_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            PRIMARY KEY (event_id, user_id),
            FOREIGN KEY (event_id) REFERENCES events (id),
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')

    # Expenses table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            amount REAL NOT NULL,
            date DATE DEFAULT CURRENT_DATE,
            payer_id INTEGER NOT NULL,
            event_id INTEGER NOT NULL,
            FOREIGN KEY (payer_id) REFERENCES users (id),
            FOREIGN KEY (event_id) REFERENCES events (id)
        )
    ''')

    # Expense participants (split per person)
    conn.execute('''
        CREATE TABLE IF NOT EXISTS expense_participants (
            expense_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            amount_owed REAL NOT NULL,
            PRIMARY KEY (expense_id, user_id),
            FOREIGN KEY (expense_id) REFERENCES expenses (id),
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')

    conn.commit()
    conn.close()
    print(" Datenbank wurde initialisiert!")

if __name__ == '__main__':
    init_database()
