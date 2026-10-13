import os
import sqlite3
from flask import Flask, redirect, render_template, request, url_for
from prometheus_client import Counter, Gauge, generate_latest
from myapp.db import get_db_path, init_db

# ИСПРАВЛЕНО: добавлены двойные подчеркивания __file__ и __name__
base_dir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__,
            static_folder=os.path.join(base_dir, 'static'), 
            template_folder=os.path.join(base_dir, 'static'))

REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP Requests', ['method', 'endpoint'])
WORD_COUNT = Gauge('arabic_words_total', 'Total number of Arabic words in database')

@app.before_request
def before_request():
    try:
        conn = sqlite3.connect(get_db_path())
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM words')
        count = cursor.fetchone()[0]
        conn.close()
        WORD_COUNT.set(count)
    except Exception as e:
        print(f"DB Error in before_request: {e}")

@app.route('/')
def index():
    REQUEST_COUNT.labels(method=request.method, endpoint='/').inc()
    try:
        conn = sqlite3.connect(get_db_path())
        cursor = conn.cursor()
        cursor.execute('SELECT id, arabic, translation FROM words')
        words = cursor.fetchall()
        conn.close()
        return render_template('index.html', words=words)
    except Exception as e:
        return f"Database error: {e}", 500

@app.route('/add', methods=['POST'])
def add_word():
    REQUEST_COUNT.labels(method=request.method, endpoint='/add').inc()
    arabic = request.form.get('arabic')
    translation = request.form.get('translation')
    if arabic and translation:
        conn = sqlite3.connect(get_db_path())
        cursor = conn.cursor()
        cursor.execute('INSERT INTO words (arabic, translation) VALUES (?, ?)', (arabic, translation))
        conn.commit()
        conn.close()
    return redirect(url_for('index'))

# ИСПРАВЛЕНО: правильный синтаксис маршрута Flask
@app.route('/delete/<int:word_id>')
def delete_word(word_id):
    REQUEST_COUNT.labels(method=request.method, endpoint='/delete').inc()
    conn = sqlite3.connect(get_db_path())
    cursor = conn.cursor()
    cursor.execute('DELETE FROM words WHERE id = ?', (word_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/health')
def health():
    REQUEST_COUNT.labels(method=request.method, endpoint='/health').inc()
    return {"status": "ok", "app": "arabic-learning-tracker"}, 200

@app.route('/metrics')
def metrics():
    return generate_latest(), 200, {'Content-Type': 'text/plain; charset=utf-8'}

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=8080, threaded=True)