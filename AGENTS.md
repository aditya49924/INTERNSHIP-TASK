# AGENTS.md

## What this repo is

Three standalone interactive Python command-line programs, plus a small Flask
front end (`webapp.py`) that makes them usable in a browser. There is no
application server, database, or external service in this project.

- `Calculator.py`, `PASSWORD GENERATOR`, `Rock Paper Scissors Game` — the
  original tasks. They are stdin-driven and must keep working as CLI programs.
- `webapp.py` + `templates/` — the browser front end.

## Running it

```sh
docker compose -f docker-compose.base44.yml up -d --build
```

The web entry point listens on host port 3000. It is a single `python:3.12-slim`
service with the repo bind-mounted, dependencies (`requirements.txt`) installed
on container start, and Flask in debug mode so code edits are picked up without
a rebuild. Templates are re-read on every request.

## Notes

- `webapp.py` deliberately runs each script as a subprocess and feeds the form
  values to its stdin, so the original files stay untouched; do not port the
  program logic into the web app.
- The two programs with spaces in their filenames (`PASSWORD GENERATOR`,
  `Rock Paper Scissors Game`) must be referenced as single argv entries.
- A program that raises (e.g. a non-numeric length) prints a traceback to
  stderr; the web app appends stderr to the output shown in the browser.
- These programs expect one line per prompt. Because Rock Paper Scissors loops,
  the form covers exactly one round.

## Verifying it works

```sh
docker compose -f docker-compose.base44.yml ps
curl -s http://localhost:3000/ | grep -c Calculator
```

Then submit each program's form; the output shown is the script's own stdout.
