# DevOps Assignment 1 — Flask + SQLite Learnings

## Flask basics

- `app = Flask(__name__)` creates the application object. Every route and
  `app.run()` call happens on this object. `__name__` is a built-in Python
  variable Flask uses to locate the project's files on disk (for things like
  `templates/`/`static/` folders later).
- **Routes** are declared with a decorator directly above a function:
  ```python
  @app.route("/tasks", methods=["GET"])
  def read_tasks():
      ...
  ```
  The decorator tells Flask "run this function whenever a request matches
  this URL + method." `methods` defaults to `["GET"]` if omitted.
- **URL path parameters** let you capture part of the URL as a variable:
  ```python
  @app.route("/tasks/<int:task_id>", methods=["DELETE"])
  def delete_task(task_id):
      ...
  ```
  `<int:task_id>` means "this segment of the URL is an integer, call it
  `task_id`." Flask passes it into the function automatically.
- `request` (imported via `from flask import Flask, request`) is a global
  object representing the *current* incoming request — not something you
  pass into your function manually (unlike Java-style parameter passing).
- `request.json` gives you the request body as a Python dict, when the
  client sends JSON.
- A route function must `return` something — Flask errors otherwise. You
  can return a dict (auto-converted to JSON) and optionally a status code:
  `return {"message": "task created"}, 201`.
- `if __name__ == "__main__":` checks whether this file was run directly
  (`python app.py`, sets `__name__ = "__main__"`) vs. imported elsewhere
  (`__name__` = the module name instead). This stops the dev server from
  starting just because another file imported something from `app.py`.
  `app.run(debug=True)` starts the server with auto-reload and detailed
  error pages.

## HTTP methods ↔ CRUD mapping

| CRUD   | HTTP Method |
|--------|-------------|
| Create | POST        |
| Read   | GET         |
| Update | PUT (or PATCH) |
| Delete | DELETE      |

A browser address bar can only send GET requests — that's why only the
Read route is testable by clicking a link. POST/PUT/DELETE need a tool
like curl or Postman.

## SQLite basics

- `sqlite3.connect("tasks.db")` opens a connection — creates the file if
  it doesn't exist yet, opens it if it does.
- A **cursor** (`conn.cursor()`) is what actually runs SQL:
  `cursor.execute("SQL HERE")`.
- `conn.commit()` saves changes — required after INSERT/UPDATE/DELETE, not
  needed after SELECT (reading doesn't change data).
- `conn.close()` closes the connection — always do this, or SQLite can lock up.
- **Never put variable values directly into an SQL string.** Use `?`
  placeholders and pass actual values as a separate tuple — this prevents
  SQL injection:
  ```python
  cursor.execute(
      "INSERT INTO tasks (title, done) VALUES (?, ?)",
      (t, False)
  )
  ```
  Single-value tuples need a trailing comma: `(task_id,)` — without the
  comma it's just a number in parentheses, not a tuple.
- `cursor.fetchall()` retrieves all rows from the last `execute()`'d
  SELECT, as a list of tuples: `[(1, "buy milk", 0), (2, "walk dog", 1)]`.
  Convert to a list of dicts for clean JSON output:
  ```python
  result = [{"id": row[0], "title": row[1], "done": row[2]} for row in rows]
  ```
  (list comprehension — Python's compact "loop that builds a list" syntax)
- `CREATE TABLE IF NOT EXISTS` avoids errors on repeated app startup.
- SQLite types used: `INTEGER PRIMARY KEY` (auto-increments), `TEXT`,
  `BOOLEAN` (stored internally as 0/1).

## Python syntax notes (vs. Java habits)

- Indentation defines code blocks — no curly braces. Every line inside a
  function/if-block must be indented at the *same* level (4 spaces is
  convention). Mismatched indentation = `IndentationError`.
- Triple-quoted strings (`"""..."""`) allow multi-line strings — a single
  `"..."` string can't span multiple lines.
- No need to declare variable types or write getter/setter classes for
  simple data — a SQL table schema can define the "shape" of a record
  instead of a Python class.

## localhost / testing

- Flask's dev server runs at `http://127.0.0.1:5000` by default.
- `/` (root) isn't automatically defined — visiting it gives "page not
  found" unless you explicitly created a route for `/`. That's expected,
  not a bug, if you only defined `/tasks` routes.
- Test GET routes by pasting the URL in a browser (e.g. `/tasks`).
- Test POST/PUT/DELETE with curl:
  ```powershell
  curl.exe -X POST http://127.0.0.1:5000/tasks -H "Content-Type: application/json" -d '{\"title\":\"buy milk\"}'
  ```
  - `-X POST` sets the HTTP method (curl defaults to GET otherwise)
  - `-H "Content-Type: application/json"` tells Flask the body is JSON
  - `-d '...'` is the JSON body being sent
  - **Windows/PowerShell gotcha:** plain `curl` is aliased to
    `Invoke-WebRequest` with different syntax — use `curl.exe` to force
    real curl, and escape inner quotes with `\"` since PowerShell's outer
    single quotes don't protect double quotes like bash does.

## Git / repo setup (Windows/PowerShell)

- `New-Item app.py` — PowerShell's equivalent of Unix `touch`.
- `.gitignore` should include: `__pycache__/`, `*.pyc`, `tasks.db`, `venv/`
  — so you don't commit the actual database file or Python cache junk.
- Standard flow: `git init` → `git add .` → `git commit -m "..."` →
  `git branch -M main` → `git remote add origin <url>` → `git push -u origin main`.