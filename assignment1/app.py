#takes request from client is json format
from flask import Flask, request
import sqlite3

#creates actua; Flask application object- knows all the routes and when you call .run()
app = Flask(__name__)

# Opens a connection to the SQLite file (creates it if it doesn't exist yet)
def get_db():
    conn = sqlite3.connect("tasks.db")
    return conn

# Creates the tasks table on startup if it isn't already there
def init_db():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks(
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            done BOOLEAN
        )
    """)
    conn.commit()
    conn.close()

#calls the method
init_db()

#decorator to link url to appropriate function based on method
@app.route("/tasks", methods=["POST"])
def create_task():
    conn = get_db()
    cursor = conn.cursor()
    data = request.json
    t = data["title"]
    cursor.execute(
        "INSERT INTO tasks (title, done) VALUES (?, ?)",
        (t, False)
    )
    conn.commit()
    conn.close()
    return {"message": "task created"}, 201

@app.route("/tasks", methods=["GET"])
def read_tasks():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks")
    rows = cursor.fetchall()
    result = [{"id": row[0], "title": row[1], "done": row[2]} for row in rows]
    conn.close()
    return result

@app.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    conn = get_db()
    cursor = conn.cursor()
    data = request.json
    new_t = data["title"]
    new_d = data["done"]
    cursor.execute(
        "UPDATE tasks SET title = ?, done = ? WHERE id = ?",
        (new_t, new_d, task_id)
    )
    conn.commit()
    conn.close()
    return {"message": "task updated successfully"}, 200

@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    return {"message": "task deleted successfully"}, 200

# Without this line, your file just defines routes and functions but never actually listens for HTTP requests — nothing would happen if you ran it.
# debug=True gives you two conveniences while developing: the server auto-restarts whenever you save a code change, and if something crashes, you get a detailed error page in the browser showing exactly which line failed, instead of a generic server error.
if __name__ == "__main__":
    app.run(debug=True)