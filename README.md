# Caption Search

Create a personal full-text search SQLite database of YouTube video captions and browse it with a Flask web-app.

Made this to teach myself more SQL, SQLite's FTS functionality, ways to more sustainably develop a Flask app, and how to embed text files as part of a Python module.

## Installation
You already know this: `git clone`, `cd`, and `poetry install`.

## Usage
This application extends the Flask command-line interface to manage the database.
With the environment variable `FLASK_APP=caption_search`:
- `flask db init`: Initialize the database.
- `flask db add-video <video>`: Add a video to the database
- `flask db add-playlist <playlist>`: Add a "playlist" (actual playlist, trending tab, a channel's videos, etc.) to the database.

After that, run the `caption_search` WSGI app as you normally would, whether that be `flask run` or `gunicorn` if you want to deploy this thing. If you just want a server to start, run `python3 main.py`.
