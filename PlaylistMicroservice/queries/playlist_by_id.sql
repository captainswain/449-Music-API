-- :name playlist_by_id :one
SELECT title, playlist_description, creator FROM playlists
WHERE id = :id;