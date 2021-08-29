CREATE TABLE videos (
	id TEXT PRIMARY KEY,
	title TEXT
);

CREATE TABLE captions (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	video_id TEXT,
	text TEXT,
	start FLOAT,
	end FLOAT,
	raw_text TEXT,
	identifier TEXT,
	FOREIGN KEY (video_id) REFERENCES videos(id)	
);

