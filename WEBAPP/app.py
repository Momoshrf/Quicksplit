from flask import Flask, render_template, redirect, url_for, session
from database import init_database
from routes.events import events_bp
from auth import auth_bp
from routes.expenses import expenses_bp



app = Flask(__name__)

# Secret Key für Flash Messages - von Flask Tutorial
app.secret_key = '1234567890'

# Event Blueprint registrieren
app.register_blueprint(events_bp)

# Auth Blueprint registrieren
app.register_blueprint(auth_bp)

app.register_blueprint(expenses_bp)


# Datenbank beim Start initialisieren
init_database()

@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    return render_template('index.html', user_name=session.get('user_name'))


# 404 Error Handler für unsere schöne 404-Seite
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == "__main__":
    app.run(debug=True)