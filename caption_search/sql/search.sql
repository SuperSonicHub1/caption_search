WITH rankings (id, rank, text) AS (
	SELECT rowid, rank, highlight(captions_index, 0, '<b>', '</b>')
	FROM captions_index
	WHERE captions_index MATCH ?
)

SELECT captions.id, captions.video_id, rankings.text, captions.start, captions.end, rankings.rank, videos.id, videos.title
FROM captions, rankings
LEFT JOIN videos
ON captions.video_id = videos.id
WHERE captions.id = rankings.id
ORDER BY rankings.rank, captions.video_id;

-- if SELECT *:
-- (captions.id, captions.video_id, captions.text, captions.start, captions.end, captions.raw_text, captions.identifier, rankings.id, rankings.rank, videos.id, videos.title)
