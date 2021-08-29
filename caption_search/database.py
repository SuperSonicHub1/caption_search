import sqlite3
from . import sql
from .scraper import download_playlist_captions, download_video_captions

import click
from flask import current_app, g
from flask.cli import AppGroup

db_cli = AppGroup('db')

def get_db():
	if 'db' not in g:
		g.db = sqlite3.connect(
			current_app.config['DATABASE'],
			detect_types=sqlite3.PARSE_DECLTYPES
		)
		g.db.row_factory = sqlite3.Row
	return g.db

def close_db(e=None):
	db = g.pop('db', None)

	if db is not None:
		db.close()

def init_db():
	db = get_db()
	db.executescript(sql.init)
	db.executescript(sql.init_fts)	

def init_app(app):
	app.teardown_appcontext(close_db)
	app.cli.add_command(db_cli)

@db_cli.command("init")
def init_db_command():
	init_db()
	click.echo('Database initialized.')

@db_cli.command("add-playlist")
@click.argument("url")
def add_playlist_command(url):
	db = get_db()
	for info, captions in download_playlist_captions(url):
		db.execute(sql.insert_video, list(info.values()))
		db.executemany(
			sql.insert_caption, 
			[[info["id"]] + list(caption.values()) for caption in captions],
		)
	db.commit()

@db_cli.command("add-video")
@click.argument("url")
def add_video_command(url):
	db = get_db()
	info, captions = download_video_captions(url)
	db.execute(sql.insert_video, list(info.values()))
	db.executemany(
		sql.insert_caption, 
		[[info["id"]] + list(caption.values()) for caption in captions],
	)
	db.commit()
