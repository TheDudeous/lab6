import sqlite3
from flask import Flask, request, redirect, url_for, render_template_string

app = Flask(__name__)
DATABASE = 'tasks.db'

def init_db():
    """Инициализация базы данных"""
    with sqlite3.connect(DATABASE) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                completed BOOLEAN NOT NULL DEFAULT 0
            )
        ''')
        conn.commit()

# Встроенный HTML шаблон
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>CRUD Задачи</title>
    <style>body { font-family: sans-serif; margin: 40px; }</style>
</head>
<body>
    <h1>Список задач (SQLite)</h1>
    <form action="/add" method="POST">
        <input type="text" name="title" placeholder="Новая задача" required>
        <button type="submit">Добавить</button>
    </form>
    <ul>
    {% for task in tasks %}
        <li>
            <form action="{{ url_for('toggle', task_id=task[0]) }}" method="POST" style="display:inline;">
                <button type="submit" style="background:none; border:none; cursor:pointer;">
                    {% if task[2] %} ✅ {% else %} ⬜ {% endif %}
                </button>
            </form>
            {{ task[1] }}
            <form action="{{ url_for('delete', task_id=task[0]) }}" method="POST" style="display:inline; margin-left: 10px;">
                <button type="submit" style="color: red; background: none; border: none; cursor: pointer;">Удалить</button>
            </form>
        </li>
    {% endfor %}
    </ul>
</body>
</html>
'''

@app.route('/')
def index():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM tasks')
        tasks = cursor.fetchall()
    return render_template_string(HTML_TEMPLATE, tasks=tasks)

@app.route('/add', methods=['POST'])
def add():
    title = request.form.get('title')
    if title:
        with sqlite3.connect(DATABASE) as conn:
            conn.execute('INSERT INTO tasks (title) VALUES (?)', (title,))
            conn.commit()
    return redirect(url_for('index'))

@app.route('/toggle/<int:task_id>', methods=['POST'])
def toggle(task_id):
    with sqlite3.connect(DATABASE) as conn:
        conn.execute('UPDATE tasks SET completed = NOT completed WHERE id = ?', (task_id,))
        conn.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:task_id>', methods=['POST'])
def delete(task_id):
    with sqlite3.connect(DATABASE) as conn:
        conn.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
        conn.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db() # Создаем таблицу при запуске
    app.run(debug=True)