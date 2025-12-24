import sqlite3
import os
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

# Veritabanı dosyasını 'data' klasöründe tutacağız.
# Docker Volume ile bu klasörü dışarıya bağlayacağız.
DB_FOLDER = '/app/data'
DB_FILE = os.path.join(DB_FOLDER, 'guestbook.db')

def init_db():
    """Veritabanı yoksa oluşturur ve tabloyu kurar."""
    if not os.path.exists(DB_FOLDER):
        os.makedirs(DB_FOLDER)
    
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS messages 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, content TEXT)''')
    conn.commit()
    conn.close()

# Uygulama başlarken veritabanını kontrol et
init_db()

@app.route('/', methods=['GET', 'POST'])
def index():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    if request.method == 'POST':
        name = request.form['name']
        content = request.form['content']
        c.execute("INSERT INTO messages (name, content) VALUES (?, ?)", (name, content))
        conn.commit()
        return redirect('/')

    c.execute("SELECT name, content FROM messages ORDER BY id DESC")
    messages = c.fetchall()
    conn.close()
    
    return render_template('index.html', messages=messages)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
