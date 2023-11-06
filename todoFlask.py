from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
from mysql.connector import Error

# app = Flask(__name__)
app = Flask(__name__, static_folder='path/to/static')



# Database Configurations
config = {
    'user': 'springadmin',
    'password': 'able22661069HKBU',  # Replace with your password
    'host': 'hdds2401-t05-able2.mysql.database.azure.com',  # Replace with your host
    'database': 'todo_list_db',
}

def connect_to_database(config):
    """ Connect to the MySQL database server """
    connection = mysql.connector.connect(**config)
    return connection

@app.route('/')
def index():
    conn = connect_to_database(config)
    cursor = conn.cursor()
    cursor.execute("SELECT id, task FROM tasks")
    tasks = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('index.html', tasks=tasks)



@app.route('/add', methods=['POST'])
def add():
    description = request.form['description']
    conn = connect_to_database(config)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tasks (task) VALUES (%s)", (description,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('index'))

@app.route('/remove', methods=['POST'])
def remove():
    task_id = request.form['task_id']
    conn = connect_to_database(config)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('index'))

@app.route('/modify', methods=['POST'])
def modify():
    task_id = request.form['task_id']
    new_description = request.form['new_description']
    conn = connect_to_database(config)
    cursor = conn.cursor()
    cursor.execute("UPDATE tasks SET task = %s WHERE id = %s", (new_description, task_id))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('index'))

@app.errorhandler(500)
def internal_error(exception):
    app.logger.error(exception)
    return "Internal server error", 500


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001)




