-- :name get_track_by_id :one
SELECT title, album_title, artist, track_length, media_url, album_art_url FROM tracks
WHERE id = :id;