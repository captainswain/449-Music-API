-- :name playlist_by_guid :one
SELECT title, playlist_description, creator FROM playlists
WHERE guid = :guid;