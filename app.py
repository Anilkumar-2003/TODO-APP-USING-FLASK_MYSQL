from flask import Flask, render_template, request, redirect, flash
from flask_mysqldb import MySQL
from config import DB_CONFIG
from datetime import datetime

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Needed for flashing messages

# Configure MySQL
app.config.update(DB_CONFIG)
mysql = MySQL(app)

@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, task, created_at, deadline FROM tasks")
    tasks = cur.fetchall()
    cur.close()

    return render_template('index.html', tasks=tasks, current_time=datetime.now())

@app.route('/add', methods=['POST'])
def add_task():
    task = request.form.get('task')
    deadline = request.form.get('deadline')

    if task and deadline:
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO tasks (task, deadline) VALUES (%s, %s)", (task, deadline))
        mysql.connection.commit()
        cur.close()
    
    return redirect('/')

@app.route('/delete/<int:id>')
def delete_task(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM tasks WHERE id = %s", (id,))
    mysql.connection.commit()
    cur.close()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
