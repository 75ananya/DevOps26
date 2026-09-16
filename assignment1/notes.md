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

# Docker Learnings

## What a Dockerfile actually is

A Dockerfile is a **recipe** — a sequence of steps Docker follows to build
an **image** (a snapshot containing your app + everything it needs to run:
Python, Flask, your code, all bundled together). Once built, that image
can be turned into a running **container** anywhere, without needing
Python/Flask installed on the host machine at all — it's all bundled in.

**Image vs. container:** the image is the blueprint/snapshot (built once);
a container is a running instance of that image (you can start/stop/remove
many containers from the same image).

## The 6 things a Python Dockerfile needs (conceptually)

1. Base image — a starting point that already has Python installed
2. Working directory — a folder *inside* the container for your app's files
3. Copy in the dependency list (`requirements.txt`)
4. Install those dependencies
5. Copy in the rest of the code
6. Tell Docker how to start the app + which port it uses

## Full Dockerfile, line by line

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]
```

- **`FROM python:3.11-slim`** — starts the image from an official Python
  base image instead of building an OS from scratch. `slim` is a smaller,
  stripped-down variant (fewer unnecessary OS packages) → smaller image,
  faster builds. Match the version (`3.11`) to your local Python version
  (check with `python --version`). There's also a full `python:3.11` image
  if `slim` ever causes missing-system-library issues.

- **`WORKDIR /app`** — creates `/app` inside the container and makes it
  the "current directory" for every instruction that follows — similar to
  `cd /app` before running anything else. All later relative paths
  (`COPY`, etc.) are relative to this.

- **`COPY requirements.txt .`** — `COPY <source> <destination>`. Source is
  relative to wherever the Dockerfile sits (here, `assignment1/`);
  destination `.` means "into the current WORKDIR" (`/app`). This copies
  just `requirements.txt` in first — **not the whole codebase yet**.

- **`RUN pip install -r requirements.txt`** — `RUN` executes a command
  **during the build**, and its effects get baked into the image. This
  installs Flask (and anything else listed) inside the image.

  **Why `requirements.txt` is copied and installed *before* the rest of
  the code (not all at once):** Docker caches each build step. If you
  copied all your code first, then every code change would force
  `pip install` to re-run from scratch on the next build. By copying
  `requirements.txt` first and installing before copying the rest, Docker
  only re-runs the install step when dependencies actually change — editing
  `app.py` later won't trigger a reinstall. This is a standard optimization
  pattern, not something required for it to *work*, but very common.

- **`COPY . .`** — copies everything else from your local folder into the
  container's `/app`. First `.` = your local `assignment1/` folder
  (Docker's "build context"), second `.` = `/app` (current WORKDIR).

- **`EXPOSE 5000`** — mostly **documentation**: tells anyone reading the
  Dockerfile "this container listens on port 5000" (Flask's default).
  Does **not** by itself make the port reachable from your host machine —
  that happens at `docker run` time via `-p`.

- **`CMD ["python", "app.py"]`** — specifies the command that runs
  **when a container starts** from this image (not during build).
  Equivalent to typing `python app.py`, but written as a list of the
  command + its arguments (Docker's required syntax for `CMD`).

  **`RUN` vs `CMD` — the key distinction:**
  - `RUN` → executes at **build** time, baked into the image (e.g. installing packages)
  - `CMD` → executes at **container start** time, defines the default running process

## Creating the Dockerfile file itself

```powershell
New-Item Dockerfile
```
Run this **inside `assignment1/`**, next to `app.py` and `requirements.txt`.
- No file extension — exactly `Dockerfile`, not `Dockerfile.txt`.
- Capital `D`, lowercase rest — Docker is case-sensitive about this on
  some systems.
- Watch out for Windows File Explorer silently appending `.txt` if
  creating via right-click → New Text Document — `New-Item` avoids this.

## requirements.txt

- Plain text file, one package per line, lets anyone install every
  dependency at once: `pip install -r requirements.txt`.
- **Only list what your code actually `import`s** — don't blindly copy
  `pip freeze` output, since that dumps *every* package installed
  globally on your system (across all projects), not just what this app
  needs. A bloated `requirements.txt` means slower Docker builds and a
  larger, messier image.
- Standard-library modules (like `sqlite3`) never need to be listed —
  they ship with Python itself.
- Pin exact versions (`Flask==3.1.2`) rather than leaving them unpinned,
  so Docker installs the *same* version every build, not whichever is
  newest that day. Check your installed version with `pip show flask`.
- Lives at the **repo-subfolder level** matching your Dockerfile —
  i.e. inside `assignment1/`, next to `app.py`, since the Dockerfile's
  `COPY requirements.txt .` step assumes they're in the same folder.

## Build & run commands

```powershell
cd path\to\devops-repo\assignment1
docker build -t task-app .
docker run -p 5000:5000 task-app
```

- **Must run from inside `assignment1/`** — `docker build`'s trailing `.`
  means "use the current directory as the build context," and Docker
  looks for a file literally named `Dockerfile` there, along with
  everything `COPY` instructions reference by relative path.
- `docker build -t task-app .` — `-t task-app` names/tags the built image
  `task-app` (so you can reference it later instead of a random hash).
- `docker run -p 5000:5000 task-app` — starts a container from the
  `task-app` image. `-p 5000:5000` maps **host port : container port** —
  this is what actually makes the app reachable at
  `http://127.0.0.1:5000` from your machine; `EXPOSE` in the Dockerfile
  alone does not do this.
- **Docker Desktop must be running** (whale icon in the system tray) for
  any `docker` command to work at all — otherwise you get a "cannot
  connect to the Docker daemon" error.
- First build is slower (has to download the `python:3.11-slim` base
  image); later builds are much faster due to layer caching.
- A container gets a random auto-generated name (e.g. `laughing_einstein`)
  if you don't pass `--name` — cosmetic only, not an error.
- Check a container's status/logs in Docker Desktop: click the container
  → **Logs** tab shows Python/Flask errors if it crashed instead of
  staying "Running."

## Testing the containerized app (Windows/PowerShell specifics)

- Once running, hit the **host** port you mapped, same as testing locally:
  ```powershell
  curl.exe http://127.0.0.1:5000/tasks
  ```
- **PowerShell quoting gotcha (important):** PowerShell single quotes
  `'...'` are **literal** — they do NOT need (and will break with)
  backslash-escaped inner double quotes like `\"`. So:
  ```powershell
  # WRONG — backslashes get sent literally, breaks the JSON:
  curl.exe -X POST http://127.0.0.1:5000/tasks -H "Content-Type: application/json" -d '{\"title\":\"buy milk\"}'

  # RIGHT — plain double quotes inside single quotes, no escaping:
  curl.exe -X POST http://127.0.0.1:5000/tasks -H "Content-Type: application/json" -d '{"title":"buy milk"}'
  ```
- **More reliable alternative — skip curl's quoting issues entirely** with
  PowerShell's native cmdlet:
  ```powershell
  Invoke-RestMethod -Uri http://127.0.0.1:5000/tasks -Method Post -ContentType "application/json" -Body '{"title":"buy milk"}'
  ```
  This is what ended up working cleanly.

## Persistence — flagged for next session

Right now, `tasks.db` lives **inside the container's filesystem**. If the
container is stopped and removed, that data is gone — this is exactly the
problem **Docker volumes** solve (assignment requirement #2). Still to
cover: how to mount a volume so the SQLite file survives container
restarts/removal.

## Still ahead (per assignment requirements)

- Docker volumes for persistence
- A second container for the database (if splitting Flask/DB into
  separate containers rather than SQLite-in-the-same-container)
- Docker SDK for Python (`docker-py`) — scripted network creation +
  inspection between containers
- Python script for container management: list active containers, health
  check, auto-restart if unhealthy