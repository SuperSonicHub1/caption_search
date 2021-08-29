-- https://medium.com/hackernoon/sqlite-the-unknown-feature-edfa73a6f022
-- https://www.sqlite.org/fts5.html

CREATE VIRTUAL TABLE captions_index USING fts5(
	text,
	tokenize=porter
);

-- Triggers

CREATE TRIGGER after_captions_insert AFTER INSERT ON captions BEGIN
  INSERT INTO captions_index (
    rowid,
    text
  )
  VALUES(
    new.id,
    new.text
  );
END;

CREATE TRIGGER after_captions_update UPDATE OF review ON captions BEGIN
  UPDATE captions_index SET text = new.text WHERE rowid = old.id;
END;

CREATE TRIGGER after_captions_delete AFTER DELETE ON captions BEGIN
    DELETE FROM captions_index WHERE rowid = old.id;
END;
