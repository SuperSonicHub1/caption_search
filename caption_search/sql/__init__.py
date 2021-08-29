from importlib.resources import read_text

init = read_text(__package__, "init.sql")
init_fts = read_text(__package__, "init_fts.sql")
insert_video = read_text(__package__, "insert_video.sql")
insert_caption = read_text(__package__, "insert_caption.sql")
search = read_text(__package__, "search.sql")
