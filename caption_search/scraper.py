from . import vttparser
from requests import Session
from youtube_dl import YoutubeDL

TEST_CHANNEL = "https://www.youtube.com/c/suckerpinch/videos"
TEST_VIDEO = "https://www.youtube.com/watch?v=HLRdruqQfRk"
TYPE = "_type"

ytdl_opts = {
	"quiet": True,
	"dump_single_json": True,
}

ytdl = YoutubeDL(ytdl_opts)
session = Session()


def extract_info(url: str):
	return ytdl.extract_info(url, download=False)

def multiget(dictionary: dict, keys: list, default=None):
	for key in keys:
		value = dictionary.get(key)
		if value:
			return value
	return default

def extract_captions_url(info: dict):
	captions = multiget(info, ["subtitles", "automatic_captions"])
	if captions == None:
		return
	formats = multiget(captions, ["en", "en-US", "en-GB"])
	if formats == None:
		return
	for format in formats:
		if format.get("ext") == "vtt":			
			return format.get("url")

def download_video_captions(url: str):
	info = extract_info(url)
	assert TYPE not in info
	captions_url = extract_captions_url(info)
	if not captions_url:
		return None, None

	simple_info = {"id": info["id"], "title": info["title"],}
	
	res = session.get(captions_url)
	res.raise_for_status()
	subs = vttparser.string_to_subs(res.text)
	return simple_info, vttparser.subs_to_dicts(subs)

def download_playlist_captions(url: str):
	info = extract_info(url)
	assert TYPE in info and info.get(TYPE) == "playlist"
	mapped_captions = map(lambda x: download_video_captions(x["id"]), info["entries"])
	return filter(
		lambda x: x[0] and x[1],
		mapped_captions
	)

if __name__ == "main":
	for info, captions in download_playlist_captions(TEST_CHANNEL):
		if info and captions:
			print(info)
			print(list(captions))
			print("_______________")
