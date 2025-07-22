from flask import Flask
import sqlite3

app = Flask(__name__)

# db setup
def init_db():
    db = sqlite3.connect('chores.db')
    c = db.cursor()
    c.execute(
        '''
        CREATE TABLE IF NOT EXISTS chores(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
            assigned_to TEXT NOT NULL
            is_done INTEGER DEFAULT 0
            )
        '''
    )
    db.commit()
    db.close()

@app.route('/')
def index():
    # need to open new connection (sqlite requires u to open a new connection per request, and close it after request is completed)
    conn = sqlite3.connect('chores.db')
    c = conn.cursor()
    c.execute('SELECT * FROM chores')
    chores = c.fetchall()
    conn.close()
    return render_template('index.html', chores=chores)

@app.route('/add', methods=['POST'])
def add():
    name = request.form['name']
    assigned_to = request.form['assigned_to']
    conn = sqlite3.connect('chores.db')
    c = conn.cursor()
    c.execute('INSERT INTO chores (name, assigned_to) VALUES (?, ?)', (name, assigned_to))
    conn.commit()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)