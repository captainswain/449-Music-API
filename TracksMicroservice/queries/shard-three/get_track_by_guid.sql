-- :name get_track_by_guid :one
SELECT title, album_title, artist, track_length, media_url, album_art_url FROM tracks
WHERE guid = :guid;