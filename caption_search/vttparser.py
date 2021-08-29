import webvtt
from datetime import timedelta
from io import StringIO
import json

class TimedeltaEncoder(json.JSONEncoder):
	"""Have a datetime.timdelta object be encoded to a float representing it's length in seconds. Why did I make this again? SQLite JSON support?"""
	def default(self, obj):
		if isinstance(obj, timedelta):
			return obj.total_seconds()
		# Let the base class default method raise the TypeError
		return json.JSONEncoder.default(self, obj)

def string_to_subs(string: str):
	with StringIO(string) as f:
		return webvtt.read_buffer(f)

def timestamp_to_timedelta(timestamp: str) -> timedelta:
	hours, minutes, seconds = timestamp.split(":", 2)
	hours, minutes, seconds = int(hours), int(minutes), float(seconds)
	return timedelta(hours=hours, minutes=minutes, seconds=seconds)

def caption_to_dict(caption):
	return {
		"text": caption.text,
		"start": timestamp_to_timedelta(caption.start).total_seconds(),
		"end": timestamp_to_timedelta(caption.end).total_seconds(),
		"raw_text": caption.raw_text,
		"identifier": caption.identifier,
	}

def subs_to_dicts(subs):
	return map(caption_to_dict, subs)

if __name__ == "__main__":
	with open("subtitles.vtt") as f:
		subs = webvtt.read_buffer(f)
	converted_subs = subs_to_dicts(subs)
	for sub in converted_subs:
		print(sub)
